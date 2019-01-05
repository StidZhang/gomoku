import functools
from flask import request
from flask_login import current_user
from flask_socketio import (
    Namespace, disconnect, join_room, leave_room
)
from ..db import close_db
from .helper import (
    get_game_status, create_game, join_game, get_gomoku_status,
    session_connected, session_disconnected, get_user_session,
    GomokuStatus, get_game_by_id, surrender, cancel_game
)
from ..user import (
    get_user_by_name
)
from .logic import (
    GomokuLogic, InvalidOperationException
)


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
    @auth_only
    def on_connect(self):
        status = get_game_status(current_user.get_id())
        self.emit('gomoku_status', status, room=request.sid)
        session_connected(current_user.get_id(), request.sid)

    @nonauth
    def on_disconnect(self):
        if current_user.is_authenticated:
            session_disconnected(current_user.get_id(), request.sid)

    @auth_only
    def on_gomoku_create(self, config):
        gid = create_game(current_user.get_id(), config)
        join_room(gid)

        guest = get_user_by_name(config['invite'])
        ss = get_user_session(guest['_id'])
        for s in ss:
            self.emit('gomoku_invite', {
                'host': current_user.username,
                'gameid': gid
            }, room=s)

    @auth_only
    def on_gomoku_join(self, gid):
        g = join_game(current_user.get_id(), gid)
        if g['status'] == GomokuStatus.New:
            hostid = g['game_host']
            ss = get_user_session(hostid)
            for s in ss:
                self.emit('gomoku_invite_success', {
                    'gameid': gid
                }, room=s)

        join_room(gid)
        self.emit('gomoku_board', get_gomoku_status(gid), room=request.sid)

    @auth_only
    def on_gomoku_fail(self, gid):
        g = get_game_by_id(gid)
        if g['status'] == GomokuStatus.New:
            cancel_game(current_user.get_id(), g)
            hostid = g['game_host']
            if current_user.get_id() == str(hostid):
                ss = get_user_session(hostid)
                for s in ss:
                    self.emit('gomoku_invite_failed', room=s)
        else:
            w = surrender(current_user.get_id(), g)
            self.emit('gomoku_end', {
                'win': w
            }, room=str(g['_id']))

    @auth_only
    def on_gomoku_move(self, move):
        try:
            g = GomokuLogic(current_user.get_id())
            data = g.move(move)
            self.emit('gomoku_board_update', data, room=g.gid)
        except InvalidOperationException:
            pass
