from enum import Enum
from typing import TypedDict


class WeaponAttributes(TypedDict):
    id: int
    volumes: list[int]


class Weapons(Enum):
    _value_: WeaponAttributes
    # Twin Blades - Infection
    AmateurBlades = {"id": 0x00000000, "volumes": [1]}
    SteelBlades = {"id": 0x00000001, "volumes": [1]}
    Phantom = {"id": 0x00000002, "volumes": [1]}
    Assassin = {"id": 0x00000003, "volumes": [1]}
    SparkBlades = {"id": 0x00000004, "volumes": [1]}
    LathBlades = {"id": 0x00000005, "volumes": [1]}
    FuseBlades = {"id": 0x0000006, "volumes": [1]}
    ShadowBlades = {"id": 0x00000007, "volumes": [1]}
    CatsBlades = {"id": 0x00000008, "volumes": [1]}
    RoninBlades = {"id": 0x00000009, "volumes": [1]}
    SpellBlades = {"id": 0x0000000A, "volumes": [1]}
    BloodyBlades = {"id": 0x0000000B, "volumes": [1]}
    Sotetsu = {"id": 0x0000000C, "volumes": [1]}
    Enou = {"id": 0x0000000D, "volumes": [1]}
    Ryoguken = {"id": 0x0000000E, "volumes": [1]}
    Raitei = {"id": 0x0000000F, "volumes": [1]}
    Anshou = {"id": 0x00000010, "volumes": [1]}
    MasterBlades = {"id": 0x00000011, "volumes": [1]}
    HellsGate = {"id": 0x00000012, "volumes": [1]}
    DantesBlades = {"id": 0x00000013, "volumes": [1]}
    # Blades - Infection
    BasicSword = {"id": 0x00010000, "volumes": [1]}
    BraveSword = {"id": 0x00010001, "volumes": [1]}
    Rondo = {"id": 0x00010002, "volumes": [1]}
    Mizuchi = {"id": 0x00010003, "volumes": [1]}
    Gakaku = {"id": 0x00010004, "volumes": [1]}
    StrangeBlade = {"id": 0x00010005, "volumes": [1]}
    Executioner = {"id": 0x00010006, "volumes": [1]}
    UnicornBlade = {"id": 0x00010007, "volumes": [1]}
    Corpseblade = {"id": 0x00010008, "volumes": [1]}
    OvalSword = {"id": 0x00010009, "volumes": [1]}
    GruntysSword = {"id": 0x0001000A, "volumes": [1]}
    Fugaku = {"id": 0x0001000B, "volumes": [1]}
    Ensui = {"id": 0x0001000C, "volumes": [1]}
    Komura = {"id": 0x0001000D, "volumes": [1]}
    Souleater = {"id": 0x0001000E, "volumes": [1]}
    SingingBlade = {"id": 0x0001000F, "volumes": [1]}
    DogmansSword = {"id": 0x00010010, "volumes": [1]}
    Steelblade = {"id": 0x00010011, "volumes": [1]}
    Glitter = {"id": 0x00010012, "volumes": [1]}
    SealSword = {"id": 0x00010013, "volumes": [1]}
    # Heavy Blades - Infection
    Adventurer = {"id": 0x00020000, "volumes": [1]}
    Kikuichimonji = {"id": 0x00020001, "volumes": [1]}
    EarthSword = {"id": 0x00020002, "volumes": [1]}
    CuringSword = {"id": 0x00020003, "volumes": [1]}
    Flamberge = {"id": 0x00020004, "volumes": [1]}
    GreenSword = {"id": 0x00020005, "volumes": [1]}
    StunSword = {"id": 0x00020006, "volumes": [1]}
    Slayer = {"id": 0x00020007, "volumes": [1]}
    Nodachi = {"id": 0x00020008, "volumes": [1]}
    DefenseSword = {"id": 0x00020009, "volumes": [1]}
    Magnifier = {"id": 0x0002000A, "volumes": [1]}
    Shanato = {"id": 0x0002000B, "volumes": [1]}
    Absorber = {"id": 0x0002000C, "volumes": [1]}
    Byakuen = {"id": 0x0002000D, "volumes": [1]}
    Shidan = {"id": 0x0002000E, "volumes": [1]}
    Raijin = {"id": 0x0002000F, "volumes": [1]}
    SharpBlade = {"id": 0x00020010, "volumes": [1]}
    Spiderblade = {"id": 0x00020011, "volumes": [1]}
    SunFangOne = {"id": 0x00020012, "volumes": [1]}
    DevilBlade = {"id": 0x00020013, "volumes": [1]}
    Claymore = {"id": 0x00020014, "volumes": [1]}
    Kikujyumonji = {"id": 0x00020015, "volumes": [1]}
    EarthianSword = {"id": 0x00020016, "volumes": [1]}
    LifeSword = {"id": 0x00020017, "volumes": [1]}
    FlameSword = {"id": 0x00020018, "volumes": [1]}
    DryadsSword = {"id": 0x00020019, "volumes": [1]}
    # Heavy Axes - Infection
    Hatchet = {"id": 0x00030000, "volumes": [1]}
    ShortSwing = {"id": 0x00030001, "volumes": [1]}
    BattleAxe = {"id": 0x00030002, "volumes": [1]}
    WaterAxe = {"id": 0x00030003, "volumes": [1]}
    FlameAxe = {"id": 0x00030004, "volumes": [1]}
    WindAxe = {"id": 0x00030005, "volumes": [1]}
    ThunderAxe = {"id": 0x00030006, "volumes": [1]}
    MidnightAxe = {"id": 0x00030007, "volumes": [1]}
    RazorAxe = {"id": 0x00030008, "volumes": [1]}
    BronzeAxe = {"id": 0x00030009, "volumes": [1]}
    CursedAxe = {"id": 0x0003000A, "volumes": [1]}
    EarthAxe = {"id": 0x0003000B, "volumes": [1]}
    WaterGodAxe = {"id": 0x0003000C, "volumes": [1]}
    BloodyAxe = {"id": 0x0003000D, "volumes": [1]}
    BanditsAxe = {"id": 0x0003000E, "volumes": [1]}
    ChargedAxe = {"id": 0x0003000F, "volumes": [1]}
    DarknessAxe = {"id": 0x00030010, "volumes": [1]}
    MastersAxe = {"id": 0x00030011, "volumes": [1]}
    PapillonAxe = {"id": 0x00030012, "volumes": [1]}
    DevilsAxe = {"id": 0x00030013, "volumes": [1]}
    # Spears - Infection
    BronzeSpear = {"id": 0x00040000, "volumes": [1]}
    IronSpear = {"id": 0x00040001, "volumes": [1]}
    ReliefLance = {"id": 0x00040002, "volumes": [1]}
    WaterSpear = {"id": 0x00040003, "volumes": [1]}
    FireSpear = {"id": 0x00040004, "volumes": [1]}
    WoodenSpear = {"id": 0x00040005, "volumes": [1]}
    ElectricSpear = {"id": 0x00040006, "volumes": [1]}
    Glaive = {"id": 0x00040007, "volumes": [1]}
    GoldSpear = {"id": 0x00040008, "volumes": [1]}
    Nihonmaru = {"id": 0x00040009, "volumes": [1]}
    SpearOfSpell = {"id": 0x0004000A, "volumes": [1]}
    BloodyLance = {"id": 0x0004000B, "volumes": [1]}
    MermanSpear = {"id": 0x0004000C, "volumes": [1]}
    LavamanSpear = {"id": 0x0004000D, "volumes": [1]}
    TreemanSpear = {"id": 0x0004000E, "volumes": [1]}
    StrormerSpear = {"id": 0x0004000F, "volumes": [1]}
    BerserkSpear = {"id": 0x00040010, "volumes": [1]}
    Sleipner = {"id": 0x00040011, "volumes": [1]}
    FairySpear = {"id": 0x00040012, "volumes": [1]}
    FiendSpear = {"id": 0x00040013, "volumes": [1]}
    # Wands
    CypressWand = {"id": 0x00050000, "volumes": [1]}
    IronRod = {"id": 0x00050001, "volumes": [1]}
    EarthWand = {"id": 0x00050002, "volumes": [1]}
    WaterWand = {"id": 0x00050003, "volumes": [1]}
    FireWand = {"id": 0x00050004, "volumes": [1]}
    AirWand = {"id": 0x00050005, "volumes": [1]}
    ElectricWand = {"id": 0x00050006, "volumes": [1]}
    EbonyWand = {"id": 0x00050007, "volumes": [1]}
    WandOfWisdom = {"id": 0x00050008, "volumes": [1]}
    BashoWand = {"id": 0x00050009, "volumes": [1]}
    DiabolicWand = {"id": 0x0005000A, "volumes": [1]}
    EarthRod = {"id": 0x0005000B, "volumes": [1]}
    RodOfTheSea = {"id": 0x0005000C, "volumes": [1]}
    InfernoWand = {"id": 0x0005000D, "volumes": [1]}
    CedarWand = {"id": 0x0005000E, "volumes": [1]}
    WandOfStorms = {"id": 0x0005000F, "volumes": [1]}
    AdiansRod = {"id": 0x00050010, "volumes": [1]}
    AlmightyWand = {"id": 0x00050011, "volumes": [1]}
    GroovyStick = {"id": 0x000500012, "volumes": [1]}
    StarStormWand = {"id": 0x000500013, "volumes": [1]}
    # Rings
