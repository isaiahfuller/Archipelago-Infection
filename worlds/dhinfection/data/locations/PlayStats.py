from enum import Enum


class PlayStats(Enum):
    _value_: any


# 16 bit
class RyuBookI(PlayStats):
    _value_: int
    AreasVisited = {"addr": 0xa46232, "scale": "list", "values": [1, 5, 10, 15, 20, 25, 30]}

# 16 bit


class RyuBookII(PlayStats):
    _value_: int
    AllFieldPortalsOpened = {"addr": 0xa46236, "scale": "range", "values": (1, 31)}
    AllDungeonPortalsOpened = {"addr": 0xa46238, "scale": "range", "values": (1, 31)}
    PortalsOpened = {"addr": 0xa46234, "scale": "list", "values": [5, 10, 25, 50, 75, 100]}


# 16 bit
class RyuBookVI(PlayStats):
    _value_: int
    ChestsOpened = {"addr": 0xa46e10, "scale": "list", "values": [5, 10, 25, 50, 75, 100, 150, 200, 300, 400]}
    BreakablesBroken = {"addr": 0xa46e12, "scale": "list", "values": [5, 10, 25, 50, 75, 100, 150, 200, 300, 400]}
    GottOpened = {"addr": 0xa46e3e, "scale": "range", "values": (1, 31)}

# 16 bit


class RyuBookVII(PlayStats):
    _value_: int
    SymbolsActivated = {"addr": 0xa46e14, "scale": "list", "values": [1, 5, 10, 15, 20, 25, 30]}


# 16 bit
class Affection(PlayStats):
    _value_: int
    Orca = 0xa470ea
    Sanjuro = 0xa472a2
    Piros = 0xa47612
    Natsume = 0xa478a6
    Gardenia = 0xa47a5e
    BlackRose = 0xa47c16
    Mistral = 0xa47cf2


class OtherStats(PlayStats):
    _value_: int
    TotalDataDrains = {"addr": 0xa4622e, "scale": "list", "values": [5, 10, 25, 50, 75, 100]}


class CharacterLevels(PlayStats):
    _value_: int
    KiteLevel = {"addr": 0xa46e66, "scale": "range", "values": (1, 31)}
