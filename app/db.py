import functools
from flask import g, current_app
from pymongo import MongoClient
from pymongo.collation import Collation, CollationStrength


def run_once(f):
    @functools.wraps(f)
    def wraps(*args, **kwargs):
        if not wraps.has_run:
            wraps.has_run = True
            return f(*args, **kwargs)
    wraps.has_run = False
    return wraps


def get_uri():
    return current_app.config['MONGODB_URI']


@run_once
def init_db(db):
    user = db.user
    user.create_index(
        'username',
        unique=True,
        collation=Collation(
            locale='en',
            strength=CollationStrength.SECONDARY
        )
    )
    user_gomoku = db.user_gomoku
    user_gomoku.create_index(
        'userid',
        unique=True,
    )
    gomoku = db.gomoku
    gomoku.create_index(
        'status'
    )
    gomoku.create_index(
        'game_host'
    )
    gomoku.create_index(
        'game_guest'
    )


def get_db():
    if 'db' not in g:
        g.mc = MongoClient(get_uri())
        try:
            g.db = g.mc.get_database()
        except Exception:
            g.db = g.mc.get_database('dev')

        init_db(g.db)

    return g.db


def close_db(e=None):
    mc = g.pop('mc', None)
    if mc is not None:
        mc.close()


def init_app(app):
    app.teardown_appcontext(close_db)
