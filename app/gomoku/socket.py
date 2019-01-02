import functools
from flask_login import current_user
from flask_socketio import Namespace, disconnect
from ..db import close_db


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
        pass

    @nonauth
    def on_disconnect(self):
        pass

    @auth_only
    def on_gomoku_create(self):
        pass

    @auth_only
    def on_gomoku_join(self):
        pass

    @auth_only
    def on_gomoku_fail(self):
        pass

    @auth_only
    def on_gomoku_move(self):
        pass
