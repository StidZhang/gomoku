import functools
from logging import getLogger
from flask import request
from flask_login import current_user
from flask_socketio import (
    Namespace, disconnect, join_room, leave_room
)
from ..db import close_db
from .helper import (
    get_game_status, create_game, join_game, get_board_status, fail_game
)
from .db_helper import (
    get_game_by_id, get_user_name
)
from .model import GomokuStatus
from ..user import (
    get_user_by_name
)
from .logic import (
    GomokuLogic, InvalidOperationException
)


logger = getLogger(__name__)


def auth_only(f):
    @functools.wraps(f)
    def wraps(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            try:
                return f(*args, **kwargs)
            finally:
                close_db()
    return wraps


def nonauth(f):
    @functools.wraps(f)
    def wraps(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        finally:
            close_db()
    return wraps


class GomokuSocket(Namespace):
    def emit_to_user(self, uid, message, data):
        self.emit(message, data, room=str(uid))

    def emit_to_game(self, gid, message, data):
        self.emit(message, data, room=str(gid))

    def emit_back(self, message, data):
        self.emit(message, data, room=request.sid)

    @auth_only
    def on_connect(self):
        self.emit_back('gomoku_status', get_game_status(current_user.get_id()))
        join_room(current_user.get_id())

    @nonauth
    def on_disconnect(self):
        pass

    @auth_only
    def on_gomoku_create(self, config):
        try:
            gid = create_game(current_user.get_id(), config)
            join_room(gid)

            # send invite to guest
            guest = get_user_by_name(config['invite'])
            self.emit_to_user(guest['_id'], 'gomoku_invite', {
                'host': current_user.username,
                'gameid': gid
            })
            # send status to host
            self.emit_to_user(
                current_user.get_id(),
                'gomoku_status',
                get_game_status(current_user.get_id())
            )
        except Exception as e:
            logger.exception(e)
            self.emit_back(
                'gomoku_status',
                get_game_status(current_user.get_id(), str(e), 40)
            )

    @auth_only
    def on_gomoku_join(self, gid):
        try:
            ret = join_game(current_user.get_id(), gid)
            join_room(gid)
            if ret:
                self.emit_to_game(gid, 'gomoku_board', get_board_status(gid))
            else:
                self.emit_back('gomoku_board', get_board_status(gid))
        except Exception as e:
            logger.exception(e)
            self.emit_back(
                'gomoku_status',
                get_game_status(current_user.get_id(), str(e), 40)
            )

    @auth_only
    def on_gomoku_fail(self, gid):
        try:
            s, h, g = fail_game(current_user.get_id(), gid)
            if s == GomokuStatus.HostCancelled:
                self.emit_to_user(h, 'gomoku_status', get_game_status(h))
            elif s == GomokuStatus.GuestRefused:
                self.emit_to_user(h, 'gomoku_status',
                    get_game_status(h, 'guest cancelled invite', 20))
            else:
                w = h if s == GomokuStatus.HostWon else g
                self.emit_to_game(gid, 'gomoku_end', {
                    'win': get_user_name(w)
                })
        except Exception as e:
            logger.exception(e)
            self.emit_back(
                'gomoku_status',
                get_game_status(current_user.get_id(), str(e), 40)
            )

    @auth_only
    def on_gomoku_move(self, move):
        try:
            g = GomokuLogic(current_user.get_id())
            data = g.move(move)
            self.emit_to_game(g.gid, 'gomoku_board_update', data)
            if data['won']:
                self.emit_to_game(g.gid, 'gomoku_end', {
                    'win': data['username']
                })
        except InvalidOperationException:
            pass
