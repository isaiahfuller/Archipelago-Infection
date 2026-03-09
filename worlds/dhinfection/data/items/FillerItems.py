from enum import IntEnum, auto, Enum
from BaseClasses import Item, ItemClassification

STORAGE_ADDRESS = 0xa40543

class Consumables(Enum):
    HealthDrink = {"id": 0x0a0000}
    HealthPotion = {"id": 0x0a0001}
    HealingElixer = {"id": 0x0a0002}