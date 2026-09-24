from enum import Enum
from typing import TypedDict


# These are bitflags that trigger when certain treasure chests are open.
class InfectionSetTreasuresAttributes(TypedDict):
    address: int
    bits: int
    volumes: list[int]


class InfectionSetTreasuresBase(Enum):
    _value_: InfectionSetTreasuresAttributes


class InfectionSetTreasures(InfectionSetTreasuresBase):
    # Bursting Passed Over Aqua Field
    SpeedCharmT = {"address": 0xA43BEC, "bits": 0b11111110, "volumes": [1]}
    ResurrectTB1 = {"address": 0xA43BEC, "bits": 0b11111101, "volumes": [1]}
    ResurrectTB2 = {"address": 0xA43BEC, "bits": 0b11111011, "volumes": [1]}
    HealingPotionT = {"address": 0xA43BEC, "bits": 0b11101111, "volumes": [1]}
    GottTreasure1 = {"address": 0xA43BEC, "bits": 0b01111111, "volumes": [1]}
    # Expansive Haunted Sea of Sand
    GottTreasure2 = {"address": 0xA43C34, "bits": 0b11101111, "volumes": [1]}
    # Boundless Corrupted Fort Walls
    GottTreasure3 = {"address": 0xA43C4C, "bits": 0b11011111, "volumes": [1]}
    # Closed Oblivious Twin Hills
    GottTreasure4 = {"address": 0xA43C64, "bits": 0b11111101, "volumes": [1]}
    # Plenteous Smiling Hypha
    GottTreasure5 = {"address": 0xA43C94, "bits": 0b11110111, "volumes": [1]}
    # Collapsed Momentary Spiral
    GottTreasure6 = {"address": 0xA43CAC, "bits": 0b11111101, "volumes": [1]}
    # Buried Pagan Fiery Sands
    GottTreasure7 = {"address": 0xA43CDC, "bits": 0b11101111, "volumes": [1]}
    # Great Distant Fertile Land
    GottTreasure8 = {"address": 0xA43D0C, "bits": 0b11111011, "volumes": [1]}
    # Discovered Primitive Touchstone
    SpriteOcarinaT = {"address": 0xA43D54, "bits": 0b11101111, "volumes": [1]}
    GottTreasure9 = {"address": 0xA43D54, "bits": 0b11011111, "volumes": [1]}
    # Indiscreet Gluttonous Pilgrimage
    GottTreasure10 = {"address": 0xA43D6C, "bits": 0b11111101, "volumes": [1]}
    # Putrid Hot-Blooded Scaffold
    FirstRemedy = {"address": 0xA43D84, "bits": 0b11111011, "volumes": [1]}
    Remedy = {"address": 0xA43D84, "bits": 0b11110111, "volumes": [1]}
    CustomRemedy = {"address": 0xA43D84, "bits": 0b11101111, "volumes": [1]}
    TrueRemedy = {"address": 0xA43D85, "bits": 0b11111101, "volumes": [1]}
    GottTreasure11 = {"address": 0xA43D85, "bits": 0b11111011, "volumes": [1]}
    # Hideous Destroyer's Far Thunder
    KotetsuSwordT = {"address": 0xA43D9C, "bits": 0b11111011, "volumes": [1]}
    # Soft Solitary Tri-Pansy
    GottTreasure12 = {"address": 0xA43DB4, "bits": 0b11111100, "volumes": [1]}
    # Beautiful Someone's Treasure Gem
    GracefulBookT = {"address": 0xA43DCC, "bits": 0b11111011, "volumes": [1]}
    # Raging Passionate Melody
    SpiralEdgeT = {"address": 0xA43DE4, "bits": 0b11101111, "volumes": [1]}
    # Voluptuous Her Remnant
    AmateurBladesT = {"address": 0xA43DFC, "bits": 0b11111110, "volumes": [1]}
    RustyNailsT = {"address": 0xA43DFC, "bits": 0b11111101, "volumes": [1]}
    KagayuzenT = {"address": 0xA43DFC, "bits": 0b10111111, "volumes": [1]}
    # Hideous Organ Market Scaffold
    IceBarT = {"address": 0xA43E14, "bits": 0b11111011, "volumes": [1]}
    # Dog Dancing Passionate Tri-Pansy
    SoulBladesT = {"address": 0xA43E2C, "bits": 0b11111101, "volumes": [1]}
    GottTreasure13 = {"address": 0xA43E2C, "bits": 0b11101111, "volumes": [1]}