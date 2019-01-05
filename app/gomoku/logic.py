from enum import IntEnum
from datetime import datetime
from bson import ObjectId
from .helper import (
    get_game_by_id, get_gomoku_collection, GomokuStatus,
    get_user_gomoku_by_uid, get_user_gomoku_collection,
    remove_current_game
)
from ..user import get_user_by_id


class GomokuColor(IntEnum):
    Empty = 0
    Black = 1
    White = 2


class InvalidOperationException(Exception):
    def __init__(self, message=None):
        if message is None:
            self.message = 'invalid operation'
        else:
            self.message = message


class GomokuLogic(object):
    def __init__(self, uid):
        ug = get_user_gomoku_by_uid(uid)
        if ug['current_game'] is None:
            raise InvalidOperationException()
        g = get_game_by_id(ug['current_game'])
        if g is None:
            raise InvalidOperationException()
        self.g = g
        self.uid = uid
        self.gid = str(g['_id'])
        self.config = g.get('config')
        self.host = g.get('game_host')
        self.guest = g.get('game_guest')
        self.rule = self.config.get('rule')
        self.size = self.config.get('size')
        self.board = g.get('board')
        self.history = g.get('history')
        self.status = g.get('status')

        if self.rule == 'swap2':
            raise InvalidOperationException('not supported yet')

        if str(uid) != str(self.host) and str(uid) != str(self.guest):
            raise InvalidOperationException()

        if self.status != GomokuStatus.Host and self.status != GomokuStatus.Guest:
            raise InvalidOperationException()

        if self.status == GomokuStatus.Host and str(uid) != str(self.host):
            raise InvalidOperationException()

        if self.status == GomokuStatus.Guest and str(uid) != str(self.guest):
            raise InvalidOperationException()

    def _swap2_move(self, m):
        pass

    def check_pos(self, x, y):
        if x < 0 or x >= self.size:
            return False
        if y < 0 or y >= self.size:
            return False
        return True

    def calc_pos(self, x, y):
        return y * self.size + x

    def get_pos(self, x, y):
        if not self.check_pos(x, y):
            raise InvalidOperationException('pos not in range')
        return self.calc_pos(x, y)

    def check_win(self, x, y, c):
        # start north cw
        direction = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        dl = []
        for dx, dy in direction:
            nr = 0
            cx, cy = x, y
            while True:
                nx, ny = cx + dx, cy + dy
                if not self.check_pos(nx, ny):
                    break
                pos = self.calc_pos(nx, ny)
                if self.board[pos] != c:
                    break
                cx, cy = nx, ny
                nr += 1
            dl.append(nr)
        for i in range(4):
            if dl[i] + dl[i + 4] >= 4:
                return True
        return False

    def _regular_move(self, m):
        color = GomokuColor.Black if str(self.host) == str(self.uid) else GomokuColor.White
        x = m.get('x')
        y = m.get('y')
        pos = self.get_pos(x, y)
        if self.board[pos] != GomokuColor.Empty:
            raise InvalidOperationException('position occupied')

        self.board[pos] = color
        is_won = self.check_win(x, y, color)
        status = GomokuStatus.Guest if str(self.host) == str(self.uid) else GomokuStatus.Host
        if is_won:
            status = GomokuStatus.HostWon if str(self.host) == str(self.uid) else GomokuStatus.GuestWon

        gc = get_gomoku_collection()
        gc.find_one_and_update({
            '_id': self.g['_id']
        }, {
            '$push': {'history': {
                'user': ObjectId(self.uid),
                'time': datetime.utcnow(),
                'move': {
                    'x': x,
                    'y': y
                }
            }},
            '$set': {
                'board': self.board,
                'status': int(status)
            }
        })
        if is_won:
            remove_current_game(self.host)
            remove_current_game(self.guest)

        u = get_user_by_id(self.uid)
        return {
            'x': x,
            'y': y,
            'username': u['username'],
            'won': is_won
        }

    def move(self, m):
        if self.rule == 'swap2':
            return self._swap2_move(m)
        else:
            return self._regular_move(m)
