from datetime import datetime
from .db import get_db
from pymongo.collation import Collation, CollationStrength
from bson import ObjectId


def get_user_collection():
    db = get_db()
    return db.user


def get_user_by_name(name):
    user = get_user_collection()
    return user.find_one({
        "username": name
    }, collation=Collation(locale='en', strength=CollationStrength.SECONDARY))


def get_user_by_id(id):
    user = get_user_collection()
    oid = ObjectId(id)
    return user.find_one({"_id": oid})


def create_user(username, password):
    u = {
        "username": username,
        "password": password,
        "created": datetime.utcnow()
    }
    user = get_user_collection()
    user.insert_one(u)
    return u


def change_user_password(userid, password):
    user = get_user_collection()
    return user.find_one_and_update({
        "_id": userid
    }, {
        "$set": {"password": password}
    })


class User(object):
    def __init__(self, user):
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
        self.user = user
        self.username = user['username']
        self.oid = user['_id']

    def get_id(self):
        return str(self.oid)
