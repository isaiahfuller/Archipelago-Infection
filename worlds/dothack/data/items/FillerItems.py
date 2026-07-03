from enum import Enum
from typing import TypedDict


class ItemDict(TypedDict):
    id: int
    weight: int


class Consumables(Enum):
    _value_: ItemDict
    HealthDrink = {"id": 0x000a0000, "weight": 20}
    HealthPotion = {"id": 0x000a0001, "weight": 35}
    HealingElixer = {"id": 0x000a0002, "weight": 50}
    Antidote = {"id": 0x000a0003, "weight": 50}
    Restorative = {"id": 0x000a0004, "weight": 50}
    Resurrect = {"id": 0x000a0005, "weight": 50}
    WarriorBlood = {"id": 0x000a0006, "weight": 35}
    KnightBlood = {"id": 0x000a0007, "weight": 35}
    HunterBlood = {"id": 0x000a0008, "weight": 35}
    HermitBlood = {"id": 0x000a0009, "weight": 35}
    BeastBlood = {"id": 0x000a000A, "weight": 35}
    WizardBlood = {"id": 0x000a000B, "weight": 35}
    WellWater = {"id": 0x000a000C, "weight": 35}
    PureWater = {"id": 0x000a000D, "weight": 35}
    BurningOil = {"id": 0x000a000E, "weight": 35}
    HolySap = {"id": 0x000a000F, "weight": 35}
    SportsDrink = {"id": 0x000a0010, "weight": 35}
    CookedBile = {"id": 0x000a0011, "weight": 35}
    MagesSoul = {"id": 0x000a0012, "weight": 35}
    ArtisansSoul = {"id": 0x000a0013, "weight": 35}
    EmperorsSoul = {"id": 0x000a0014, "weight": 35}
    NobleWine = {"id": 0x000a0015, "weight": 35}
    RiskyCoffee = {"id": 0x000a0016, "weight": 35}
    RecoveryDrink = {"id": 0x000a0017, "weight": 100}
    FortuneWire = {"id": 0x000d0000, "weight": 35}
    SpriteOcarina = {"id": 0x000d0001, "weight": 35}
    FairysOrb = {"id": 0x000d0002, "weight": 35}


class VirusCores(Enum):
    _value_: ItemDict
    VirusCoreA = {"id": 0xa406cc, "weight": 50}
    VirusCoreB = {"id": 0xa406cd, "weight": 50}
    VirusCoreC = {"id": 0xa406ce, "weight": 50}


class GruntyFood(Enum):
    _value_: ItemDict
    GoldenEgg = {"id": 0xA406E6, "weight": 25}
    GruntMints = {"id": 0xA406E7, "weight": 25}
    TwilightOnion = {"id": 0xA406E8, "weight": 25}
    SnakyCactus = {"id": 0xA406E9, "weight": 25}
    OhNoMelon = {"id": 0xA406EA, "weight": 25}
    Cordyceps = {"id": 0xA406EB, "weight": 25}
    WhiteCherry = {"id": 0xA406EC, "weight": 25}
    RootVegetable = {"id": 0xA406ED, "weight": 25}
    LaPumpkin = {"id": 0xA406EE, "weight": 25}
    Mushroom = {"id": 0xA406EF, "weight": 25}
    Mandragora = {"id": 0xA406F0, "weight": 25}
    PineyApple = {"id": 0xA406F1, "weight": 25}
    ImmatureEgg = {"id": 0xA406F2, "weight": 25}
    BearCatEgg = {"id": 0xA406F3, "weight": 25}
    InvisibleEgg = {"id": 0xA406F4, "weight": 25}
    BloodyEgg = {"id": 0xA406F5, "weight": 25}
