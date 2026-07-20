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
    GoldenEgg = {"addr": 0xa46e16, "scale": "list", "values": [5, 10, 20]}
    GruntMints = {"addr": 0xa46e18, "scale": "list", "values": [5, 10, 20]}
    TwilightOnion = {"addr": 0xa46e1a, "scale": "list", "values": [5, 10, 20]}
    SnakyCactus = {"addr": 0xa46e1c, "scale": "list", "values": [5, 10, 20]}
    OhNoMelon = {"addr": 0xa46e1e, "scale": "list", "values": [5, 10, 20]}
    Cordyceps = {"addr": 0xa46e20, "scale": "list", "values": [5, 10, 20]}
    WhiteCherry = {"addr": 0xa46e22, "scale": "list", "values": [5, 10, 20]}
    RootVegetable = {"addr": 0xa46e24, "scale": "list", "values": [5, 10, 20]}
    LaPumpkin = {"addr": 0xa46e26, "scale": "list", "values": [5, 10, 20]}
    Mushroom = {"addr": 0xa46e28, "scale": "list", "values": [5, 10, 20]}
    Mandragora = {"addr": 0xa46e2a, "scale": "list", "values": [5, 10, 20]}
    PineyApple = {"addr": 0xa46e2c, "scale": "list", "values": [5, 10, 20]}
    ImmatureEgg = {"addr": 0xa46e2e, "scale": "list", "values": [5, 10, 20]}
    BearCatEgg = {"addr": 0xa46e30, "scale": "list", "values": [5, 10, 20]}
    InvisibleEgg = {"addr": 0xa46e32, "scale": "list", "values": [5, 10, 20]}
    BloodyEgg = {"addr": 0xa46e34, "scale": "list", "values": [5, 10, 20]}
    KiteLevel = {"addr": 0xa46e66, "scale": "range", "values": (1, 31)}



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
