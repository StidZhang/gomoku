from enum import IntEnum


class GomokuStatus(IntEnum):
    New = 1
    Host = 2
    Guest = 3
    HostWon = 4
    GuestWon = 5
    HostCancelled = 6
    GuestRefused = 7


class GomokuColor(IntEnum):
    Empty = 0
    Black = 1
    White = 2
