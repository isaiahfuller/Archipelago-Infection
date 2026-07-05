from enum import Enum
from typing import TypedDict


class PlayStatAttributes(TypedDict):
    addr: int
    scale: str
    values: list[int] | tuple[int, int]


class PlayStats(Enum):
    _value_: PlayStatAttributes
    AreasVisited = {"addr": 0xa46232, "scale": "list", "values": [1, 5, 10, 15, 20, 25, 30]}
    AllFieldPortalsOpened = {"addr": 0xa46236, "scale": "range", "values": (1, 31)}
    AllDungeonPortalsOpened = {"addr": 0xa46238, "scale": "range", "values": (1, 31)}
    PortalsOpened = {"addr": 0xa46234, "scale": "list", "values": [5, 10, 25, 50, 75, 100]}
    ChestsOpened = {"addr": 0xa46e10, "scale": "list", "values": [5, 10, 25, 50, 75, 100, 150, 200, 300, 400]}
    BreakablesBroken = {"addr": 0xa46e12, "scale": "list", "values": [5, 10, 25, 50, 75, 100, 150, 200, 300, 400]}
    GottOpened = {"addr": 0xa46e3e, "scale": "range", "values": (1, 31)}
    SymbolsActivated = {"addr": 0xa46e14, "scale": "list", "values": [1, 5, 10, 15, 20, 25, 30]}
    TotalDataDrains = {"addr": 0xa4622e, "scale": "list", "values": [5, 10, 25, 50, 75, 100]}
    KiteLevel = {"addr": 0xa46e66, "scale": "range", "values": (1, 31)}

class MonsterHuntInfection(Enum):
    Razine1 = {"addr": 0xa46287, "values": [1]}
    Swordmanoid2 = {"addr": 0xa46288, "values": [1]}
    Gladiator3 = {"addr": 0xa46289, "values": [1]}
    Ochimusha4 = {"addr": 0xa4628a, "values": [1]}
    HeavyMetal6 = {"addr": 0xa4628c, "values": [1]}
    DarkRider8 = {"addr": 0xa46288, "values": [1]}


# 16 bit
class Affection(Enum):
    _value_: int
    Orca = 0xa470ea
    Sanjuro = 0xa472a2
    Piros = 0xa47612
    Natsume = 0xa478a6
    Gardenia = 0xa47a5e
    BlackRose = 0xa47c16
    Mistral = 0xa47cf2
