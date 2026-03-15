from enum import IntEnum, auto, Enum
from BaseClasses import Item, ItemClassification

STORAGE_ADDRESS = 0xa40543


class Consumables(Enum):
    HealthDrink = {"id": 0x000a0000}
    HealthPotion = {"id": 0x000a0001}
    HealingElixer = {"id": 0x000a0002}


class VirusCores(Enum):
    VirusCoreA = {"id": 0xa406cc}
    VirusCoreB = {"id": 0xa406cd}
