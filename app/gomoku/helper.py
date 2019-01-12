from bson import ObjectId
from .db_helper import (
    get_gomoku_collection, get_user_by_name, get_users_by_ids,
    get_user_gomoku_by_uid, get_user_gomoku_collection,
    get_game_by_id, get_user_name
)
from .model import GomokuStatus


def get_gomoku_invite(id):
    gc = get_gomoku_collection()
    q = gc.find({
        'status': int(GomokuStatus.New),
        'game_guest': ObjectId(id),
    }, {
        '_id': True,
        'game_host': True,
    })
    ret = [e for e in q]
    userids = [e['game_host'] for e in ret]
    u = get_users_by_ids(userids)
    return [{
        'host': u[str(x['game_host'])],
        'gameid': str(x['_id']),
    } for x in ret]


def set_user_current_game(uid, gameid):
    ugid = get_user_gomoku_by_uid(uid).get('_id')
    ugc = get_user_gomoku_collection()
    ugc.find_one_and_update({
        '_id': ugid
    }, {
        '$set': {'current_game': ObjectId(gameid)}
    })


def reset_user_current_game(uid):
    ugc = get_user_gomoku_collection()
    ugc.find_one_and_update({
        'userid': ObjectId(uid)
    }, {
        '$set': {'current_game': None}
    })


def get_game_status(uid, message=None, msg_type=None):
    ug = get_user_gomoku_by_uid(uid)
    current_game = ug.get('current_game', None)
    return {
        'current_game': str(current_game) if current_game is not None else None,
        'invites': get_gomoku_invite(uid),
        'message': {
            'content': message,
            'type': msg_type,
        } if message is not None else None,
    }


def create_game(uid, config):
    size = config.get('size', 17)
    if size > 19 or size < 5:
        raise Exception('invalid size')

    guest = config.get('invite', None)
    u = get_user_by_name(guest)
    if u is None:
        raise Exception('guest user does not exists')

    h = get_user_gomoku_by_uid(uid)
    if h['current_game'] is not None:
        raise Exception('current in another game')

    gomoku = get_gomoku_collection()
    g = {
        'status': int(GomokuStatus.New),
        'board': [0 for _ in range(size * size)],
        'history': [],
        'game_host': ObjectId(uid),
        'game_guest': u['_id'],
        'config': {
            'rule': config.get('rule', ''),
            'size': size
        },
    }
    gid = gomoku.insert_one(g).inserted_id
    set_user_current_game(uid, gid)
    return str(gid)


def join_game(uid, gid):
    g = get_game_by_id(gid)
    if g is None:
        raise Exception('game does not exists')

    hostid = str(g['game_host'])
    guestid = str(g['game_guest'])

    if uid != hostid and uid != guestid:
        raise Exception('not in this game')

    status = g['status']
    if status == GomokuStatus.New:
        if uid == guestid:
            gc = get_gomoku_collection()
            gc.find_one_and_update({
                '_id': g['_id'],
            }, {
                '$set': {'status': int(GomokuStatus.Host)}
            })
            set_user_current_game(uid, gid)
            return True
    elif status == GomokuStatus.HostCancelled or status == GomokuStatus.GuestRefused:
        raise Exception('game cancelled')
    elif status == GomokuStatus.HostWon or status == GomokuStatus.GuestWon:
        raise Exception('game ended')
    return False


def get_board_status(gid):
    gc = get_gomoku_collection()
    g = gc.find_one({
        '_id': ObjectId(gid),
    })
    if g is None:
        raise Exception('game does not exists')

    return {
        'gid': str(g['_id']),
        'board': g['board'],
        'history': g['history'],
        'host': {
            'username': get_user_name(g['game_host']),
        },
        'guest': {
            'username': get_user_name(g['game_guest']),
        },
    }


def fail_game(uid, gid):
    gc = get_gomoku_collection()
    g = get_game_by_id(gid)
    if g is None:
        raise Exception('game does not exists')

    status = g['status']
    host = str(g['game_host'])
    guest = str(g['game_guest'])
    if uid != host and uid != guest:
        raise Exception('not in the game')

    fstatus = GomokuStatus.New
    if status == GomokuStatus.New:
        fstatus = GomokuStatus.HostCancelled if uid == host else GomokuStatus.GuestRefused
        reset_user_current_game(host)
    elif status == GomokuStatus.Host or status == GomokuStatus.Guest:
        fstatus = GomokuStatus.HostWon if uid == guest else GomokuStatus.GuestWon
        reset_user_current_game(host)
        reset_user_current_game(guest)
    else:
        raise Exception('invalid operation')

    gc.find_one_and_update({
        '_id': g['_id']
    }, {
        '$set': {'status': int(status)}
    })
    return fstatus, host, guest
