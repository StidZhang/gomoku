import functools
from flask_login import current_user
from flask_socketio import (
    Namespace, disconnect, join_room, leave_room
)
from ..db import close_db
from .helper import (
    get_game_status, create_game, join_game, get_gomoku_status
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
        self.emit('gomoku_status', status)

    @nonauth
    def on_disconnect(self):
        pass

    @auth_only
    def on_gomoku_create(self, config):
        gid = create_game(current_user.get_id(), config)
        join_room(gid)

    @auth_only
    def on_gomoku_join(self, gid):
        join_game(current_user.get_id(), gid)
        join_room(gid)
        self.emit('gomoku_board', get_gomoku_status(gid))

    @auth_only
    def on_gomoku_fail(self, gid):
        pass

    @auth_only
    def on_gomoku_move(self):
        pass
