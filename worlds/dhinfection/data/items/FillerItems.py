from enum import IntEnum, auto, Enum
from BaseClasses import Item, ItemClassification

STORAGE_ADDRESS = 0xa40543


class Consumables(Enum):
    HealthDrink = {"id": 0x000a0000}
    HealthPotion = {"id": 0x000a0001}
    HealingElixer = {"id": 0x000a0002}
    Antidote = {"id": 0x000a0003}
    Restorative = {"id": 0x000a0004}
    Resurrect = {"id": 0x000a0005}
    WarriorBlood = {"id": 0x000a0006}
    KnightBlood = {"id": 0x000a0007}
    HunterBlood = {"id": 0x000a0008}
    HermitBlood = {"id": 0x000a0009}
    BeastBlood = {"id": 0x000a000A}
    WizardBlood = {"id": 0x000a000B}
    WellWater = {"id": 0x000a000C}
    PureWater = {"id": 0x000a000D}
    BurningOil = {"id": 0x000a000E}
    HolySap = {"id": 0x000a000F}
    SportsDrink = {"id": 0x000a0010}
    CookedBile = {"id": 0x000a0011}
    MagesSoul = {"id": 0x000a0012}
    ArtisansSoul = {"id": 0x000a0013}
    EmperorsSoul = {"id": 0x000a0014}
    NobleWine = {"id": 0x000a0015}
    RiskyCoffee = {"id": 0x000a0016}
    RecoveryDrink = {"id": 0x000a0017}


class VirusCores(Enum):
    VirusCoreA = {"id": 0xa406cc}
    VirusCoreB = {"id": 0xa406cd}
