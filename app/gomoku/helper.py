from bson import ObjectId
from ..db import get_db
from ..user import get_user_by_id, get_user_by_name
from enum import IntEnum


class GomokuStatus(IntEnum):
    New = 1
    Host = 2
    Guest = 3
    HostWon = 4
    GuestWon = 5
    HostCancelled = 6
    GuestRefused = 7


def get_gomoku_collection():
    db = get_db()
    return db.gomoku


def get_user_gomoku_collection():
    db = get_db()
    return db.user_gomoku


def get_game_by_id(id):
    gomoku = get_gomoku_collection()
    oid = ObjectId(id)
    return gomoku.find_one({"_id": oid})


def get_user_gomoku_by_uid(id):
    ug = get_user_gomoku_collection()
    oid = ObjectId(id)
    return ug.find_one({"userid": oid})


def get_gomoku_invite(id):
    gomoku = get_gomoku_collection()
    oid = ObjectId(id)
    q = gomoku.find({
        'status': int(GomokuStatus.New),
        'game_guest': oid,
    }, {
        '_id': True,
    })
    return [str(e['_id']) for e in q]


def get_user_gomoku_id(uid):
    ug = get_user_gomoku_by_uid(uid)
    ugc = get_user_gomoku_collection()
    if ug is None:
        return ugc.insert_one({
            'userid': ObjectId(uid),
            'current_game': None,
            'session': [],
            'total_won': 0,
            'total_game': 0,
        }).inserted_id
    else:
        return ug['_id']


def set_user_current_game(uid, gameid):
    ugid = get_user_gomoku_id(uid)
    ugc = get_user_gomoku_collection()
    ugc.find_one_and_update({
        '_id': ugid
    }, {
        '$set': {'current_game': ObjectId(gameid)}
    })


def session_connected(uid, sid):
    ugid = get_user_gomoku_id(uid)
    ugc = get_user_gomoku_collection()
    ugc.find_one_and_update({
        '_id': ugid
    }, {
        '$addToSet': {'session': sid}
    })


def session_disconnected(uid, sid):
    ugid = get_user_gomoku_id(uid)
    ugc = get_user_gomoku_collection()
    ugc.find_one_and_update({
        '_id': ugid
    }, {
        '$pull': {'session': sid}
    })


def get_user_session(uid):
    ug = get_user_gomoku_by_uid(uid)
    return ug.get('session') if ug is not None else None


def get_game_status(uid):
    ug = get_user_gomoku_by_uid(uid)
    current_game = ug.get('current_game', None) if ug is not None else None
    invites = get_gomoku_invite(uid)
    return {
        'current_game': str(current_game) if current_game is not None else None,
        'invites': invites
    }


def create_game(uid, config):
    size = config.get('size', 17)
    if size > 19 or size < 5:
        raise Exception()

    guest = config.get('invite', None)
    u = get_user_by_name(guest)
    if u is None:
        raise Exception()

    c = {
        'rule': config.get('rule', ''),
        'size': size
    }

    gomoku = get_gomoku_collection()
    g = {
        'status': int(GomokuStatus.New),
        'board': [0 for _ in range(size * size)],
        'history': [],
        'game_host': ObjectId(uid),
        'game_guest': u['_id'],
        'config': c,
    }
    gid = gomoku.insert_one(g).inserted_id
    set_user_current_game(uid, gid)
    return str(gid)


def join_game(uid, gid):
    g = get_game_by_id(gid)
    if g is None:
        raise Exception()

    status = g['status']
    if status == GomokuStatus.New:
        gc = get_gomoku_collection()
        gc.find_one_and_update({
            '_id': g['_id'],
        }, {
            '$set': {'status': int(GomokuStatus.Host)}
        })
    return g


def get_gomoku_status(gid):
    gc = get_gomoku_collection()
    g = gc.find_one({
        '_id': ObjectId(gid),
    })
    if g is None:
        raise Exception()

    host_id = g.get('game_host')
    host = get_user_by_id(host_id) if host_id is not None else None

    guest_id = g.get('game_guest')
    guest = get_user_by_id(guest_id) if guest_id is not None else None

    return {
        'gid': str(g['_id']),
        'board': g['board'],
        'history': g['history'],
        'host': {
            'username': host['username'],
        } if host is not None else None,
        'guest': {
            'username': guest['username'],
        } if guest is not None else None,
    }


def cancel_game(uid, g):
    host = g.get('game_host')
    gc = get_gomoku_collection()
    ugc = get_user_gomoku_collection()
    status = GomokuStatus.HostCancelled
    if str(uid) == str(host):
        ugc.find_one_and_update({
            'userid': host
        }, {
            '$set': {'current_game': None}
        })
    else:
        status = GomokuStatus.GuestRefused

    gc.find_one_and_update({
        '_id': g['_id']
    }, {
        '$set': {'status': int(status)}
    })


def surrender(uid, g):
    host = g.get('game_host')
    guest = g.get('game_guest')
    if str(uid) != str(host) and str(uid) != str(guest):
        return
    status = GomokuStatus.HostWon if str(uid) == str(guest) else GomokuStatus.GuestWon
    gc = get_gomoku_collection()
    ugc = get_user_gomoku_collection()
    gc.find_one_and_update({
        '_id': g['_id']
    }, {
        '$set': {'status': int(status)}
    })
    ugc.find_one_and_update({
        'userid': host
    }, {
        '$set': {'current_game': None}
    })
    ugc.find_one_and_update({
        'userid': guest
    }, {
        '$set': {'current_game': None}
    })
    win = get_user_by_id(host if status == GomokuStatus.HostWon else guest)
    return win['username']
