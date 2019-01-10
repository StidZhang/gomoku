from bson import ObjectId
from ..db import get_db
from ..user import get_user_by_id, get_users_by_ids, get_user_by_name


def get_gomoku_collection():
    db = get_db()
    return db.gomoku


def get_user_gomoku_collection():
    db = get_db()
    return db.user_gomoku


def get_game_by_id(id):
    gomoku = get_gomoku_collection()
    return gomoku.find_one({"_id": ObjectId(id)})


def get_user_gomoku_by_uid(id):
    ugc = get_user_gomoku_collection()
    ug = ugc.find_one({"userid": ObjectId(id)})
    if ug is None:
        ugc.insert_one({
            'userid': ObjectId(uid),
            'current_game': None,
            'total_won': 0,
            'total_game': 0,
        })
        ug = ugc.find_one({"userid": ObjectId(id)})
    return ug


def get_user_name(uid):
    u = get_user_by_id(uid)
    return u['username']
