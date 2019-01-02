from flask import g
from pymongo import MongoClient
from pymongo.collation import Collation, CollationStrength
from .config import Config


def get_uri():
    return Config.MONGODB_URI


def init_db(db):
    user = db.user
    user.create_index('username',
                      unique=True,
                      collation=Collation(locale='en', strength=CollationStrength.SECONDARY))


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
