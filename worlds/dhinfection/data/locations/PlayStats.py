from enum import IntEnum, IntFlag

class PlayStats(IntEnum):
    _value_: int
    

# 16 bit
class RyuBookI(PlayStats):
    _value_: int
    AreasVisited = 0xa46232

# 16 bit
class RyuBookII(PlayStats):
    _value_: int
    AllFieldPortalsOpened = 0xa46236
    AllDungeonPortalsOpened = 0xa46238

# 16 bit
class RyuBookVI(PlayStats):
    _value_: int
    ChestsOpened = 0xa46e10
    BreakablesBroken = 0xa46e12
    PortalsOpened = 0xa46234

# 16 bit
class RyuBookVII(PlayStats):
    _value_: int
    SymbolsActivated = 0xa46e14
    

#16 bit
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
    TotalDataDrains = 0xa4622e

class CharacterLevels(PlayStats):
    _value_: int
    KiteLevel = 0xa46e66
    GottOpened = 0xa46e3e