from enum import Enum
from typing import TypedDict


class EquipmentAttributes(TypedDict):
    id: int
    volumes: list[int]
    weight: int


class Weapons(Enum):
    _value_: EquipmentAttributes
    # Twin Blades - Infection
    AmateurBlades = {"id": 0x00000000, "volumes": [1], "weight": 57}
    SteelBlades = {"id": 0x00000001, "volumes": [1], "weight": 59}
    Phantom = {"id": 0x00000002, "volumes": [1], "weight": 61}
    Assassin = {"id": 0x00000003, "volumes": [1], "weight": 63}
    SparkBlades = {"id": 0x00000004, "volumes": [1], "weight": 65}
    LathBlades = {"id": 0x00000005, "volumes": [1], "weight": 67}
    FuseBlades = {"id": 0x00000006, "volumes": [1], "weight": 69}
    ShadowBlades = {"id": 0x00000007, "volumes": [1], "weight": 71}
    CatsBlades = {"id": 0x00000008, "volumes": [1], "weight": 73}
    RoninBlades = {"id": 0x00000009, "volumes": [1], "weight": 75}
    SpellBlades = {"id": 0x0000000A, "volumes": [1], "weight": 77}
    BloodyBlades = {"id": 0x0000000B, "volumes": [1], "weight": 79}
    Sotetsu = {"id": 0x0000000C, "volumes": [1], "weight": 81}
    Enou = {"id": 0x0000000D, "volumes": [1], "weight": 83}
    Ryoguken = {"id": 0x0000000E, "volumes": [1], "weight": 85}
    Raitei = {"id": 0x0000000F, "volumes": [1], "weight": 87}
    Anshou = {"id": 0x00000010, "volumes": [1], "weight": 89}
    MasterBlades = {"id": 0x00000011, "volumes": [1], "weight": 91}
    HellsGate = {"id": 0x00000012, "volumes": [1], "weight": 93}
    DantesBlades = {"id": 0x00000013, "volumes": [1], "weight": 95}
    # Rare Twin Blades - Infection
    SpiralEdge = {"id": 0x0000003C, "volumes": [1], "weight": 87}
    TimeBlades = {"id": 0x00000040, "volumes": [1], "weight": 97}
    RustyNails = {"id": 0x00000041, "volumes": [1], "weight": 92}
    SoulBlades = {"id": 0x00000042, "volumes": [1], "weight": 94}
    BomBaYe = {"id": 0x00000048, "volumes": [1], "weight": 96}
    Hyakkidouran = {"id": 0x00000049, "volumes": [1], "weight": 97}

    # Blades - Infection
    BasicSword = {"id": 0x00010000, "volumes": [1], "weight": 57}
    BraveSword = {"id": 0x00010001, "volumes": [1], "weight": 59}
    Rondo = {"id": 0x00010002, "volumes": [1], "weight": 61}
    Mizuchi = {"id": 0x00010003, "volumes": [1], "weight": 63}
    Gakaku = {"id": 0x00010004, "volumes": [1], "weight": 65}
    StrangeBlade = {"id": 0x00010005, "volumes": [1], "weight": 67}
    Executioner = {"id": 0x00010006, "volumes": [1], "weight": 69}
    UnicornBlade = {"id": 0x00010007, "volumes": [1], "weight": 71}
    Corpseblade = {"id": 0x00010008, "volumes": [1], "weight": 73}
    OvalSword = {"id": 0x00010009, "volumes": [1], "weight": 75}
    GruntysSword = {"id": 0x0001000A, "volumes": [1], "weight": 77}
    Fugaku = {"id": 0x0001000B, "volumes": [1], "weight": 79}
    Ensui = {"id": 0x0001000C, "volumes": [1], "weight": 81}
    Komura = {"id": 0x0001000D, "volumes": [1], "weight": 83}
    Souleater = {"id": 0x0001000E, "volumes": [1], "weight": 85}
    SingingBlade = {"id": 0x0001000F, "volumes": [1], "weight": 87}
    DogmansSword = {"id": 0x00010010, "volumes": [1], "weight": 89}
    Steelblade = {"id": 0x00010011, "volumes": [1], "weight": 91}
    Glitter = {"id": 0x00010012, "volumes": [1], "weight": 93}
    SealSword = {"id": 0x00010013, "volumes": [1], "weight": 95}
    # Rare Blades - Infection
    Jinsaran = {"id": 0x00010041, "volumes": [1], "weight": 96}
    PhoenixsWing = {"id": 0x00010043, "volumes": [1], "weight": 96}
    # Heavy Blades - Infection
    Adventurer = {"id": 0x00020000, "volumes": [1], "weight": 55}
    Kikuichimonji = {"id": 0x00020001, "volumes": [1], "weight": 56}
    EarthSword = {"id": 0x00020002, "volumes": [1], "weight": 57}
    CuringSword = {"id": 0x00020003, "volumes": [1], "weight": 58}
    Flamberge = {"id": 0x00020004, "volumes": [1], "weight": 59}
    GreenSword = {"id": 0x00020005, "volumes": [1], "weight": 60}
    StunSword = {"id": 0x00020006, "volumes": [1], "weight": 61}
    Slayer = {"id": 0x00020007, "volumes": [1], "weight": 62}
    Nodachi = {"id": 0x00020008, "volumes": [1], "weight": 63}
    DefenseSword = {"id": 0x00020009, "volumes": [1], "weight": 64}
    Magnifier = {"id": 0x0002000A, "volumes": [1], "weight": 65}
    Shanato = {"id": 0x0002000B, "volumes": [1], "weight": 67}
    Absorber = {"id": 0x0002000C, "volumes": [1], "weight": 69}
    Byakuen = {"id": 0x0002000D, "volumes": [1], "weight": 71}
    Shidan = {"id": 0x0002000E, "volumes": [1], "weight": 73}
    Raijin = {"id": 0x0002000F, "volumes": [1], "weight": 75}
    SharpBlade = {"id": 0x00020010, "volumes": [1], "weight": 77}
    Spiderblade = {"id": 0x00020011, "volumes": [1], "weight": 79}
    SunFangOne = {"id": 0x00020012, "volumes": [1], "weight": 81}
    DevilBlade = {"id": 0x00020013, "volumes": [1], "weight": 83}
    Claymore = {"id": 0x00020014, "volumes": [1], "weight": 85}
    Kikujyumonji = {"id": 0x00020015, "volumes": [1], "weight": 87}
    EarthianSword = {"id": 0x00020016, "volumes": [1], "weight": 89}
    LifeSword = {"id": 0x00020017, "volumes": [1], "weight": 91}
    FlameSword = {"id": 0x00020018, "volumes": [1], "weight": 93}
    DryadsSword = {"id": 0x00020019, "volumes": [1], "weight": 95}
    # Rare Heavy Blades - Infection
    KotetsuSword = {"id": 0x00020050, "volumes": [1], "weight": 87}
    Sakabatou = {"id": 0x00020056, "volumes": [1], "weight": 96}
    Shikisokuzeku = {"id": 0x00020058, "volumes": [1], "weight": 96}
    # Heavy Axes - Infection
    Hatchet = {"id": 0x00030000, "volumes": [1], "weight": 55}
    ShortSwing = {"id": 0x00030001, "volumes": [1], "weight": 57}
    BattleAxe = {"id": 0x00030002, "volumes": [1], "weight": 59}
    WaterAxe = {"id": 0x00030003, "volumes": [1], "weight": 61}
    FlameAxe = {"id": 0x00030004, "volumes": [1], "weight": 63}
    WindAxe = {"id": 0x00030005, "volumes": [1], "weight": 65}
    ThunderAxe = {"id": 0x00030006, "volumes": [1], "weight": 67}
    MidnightAxe = {"id": 0x00030007, "volumes": [1], "weight": 69}
    RazorAxe = {"id": 0x00030008, "volumes": [1], "weight": 71}
    BronzeAxe = {"id": 0x00030009, "volumes": [1], "weight": 73}
    CursedAxe = {"id": 0x0003000A, "volumes": [1], "weight": 75}
    EarthAxe = {"id": 0x0003000B, "volumes": [1], "weight": 77}
    WaterGodAxe = {"id": 0x0003000C, "volumes": [1], "weight": 79}
    BloodyAxe = {"id": 0x0003000D, "volumes": [1], "weight": 81}
    BanditsAxe = {"id": 0x0003000E, "volumes": [1], "weight": 83}
    ChargedAxe = {"id": 0x0003000F, "volumes": [1], "weight": 85}
    DarknessAxe = {"id": 0x00030010, "volumes": [1], "weight": 87}
    MastersAxe = {"id": 0x00030011, "volumes": [1], "weight": 89}
    PapillonAxe = {"id": 0x00030012, "volumes": [1], "weight": 92}
    DevilsAxe = {"id": 0x00030013, "volumes": [1], "weight": 95}
    # Rare Heavy Axes - Infection
    GiantHill = {"id": 0x00030040, "volumes": [1], "weight": 95}
    AxeBomber = {"id": 0x00030042, "volumes": [1], "weight": 95}
    # Spears - Infection
    BronzeSpear = {"id": 0x00040000, "volumes": [1], "weight": 55}
    IronSpear = {"id": 0x00040001, "volumes": [1], "weight": 57}
    ReliefLance = {"id": 0x00040002, "volumes": [1], "weight": 59}
    WaterSpear = {"id": 0x00040003, "volumes": [1], "weight": 61}
    FireSpear = {"id": 0x00040004, "volumes": [1], "weight": 63}
    WoodenSpear = {"id": 0x00040005, "volumes": [1], "weight": 65}
    ElectricSpear = {"id": 0x00040006, "volumes": [1], "weight": 67}
    Glaive = {"id": 0x00040007, "volumes": [1], "weight": 69}
    GoldSpear = {"id": 0x00040008, "volumes": [1], "weight": 71}
    Nihonmaru = {"id": 0x00040009, "volumes": [1], "weight": 73}
    SpearOfSpell = {"id": 0x0004000A, "volumes": [1], "weight": 75}
    BloodyLance = {"id": 0x0004000B, "volumes": [1], "weight": 77}
    MermanSpear = {"id": 0x0004000C, "volumes": [1], "weight": 79}
    LavamanSpear = {"id": 0x0004000D, "volumes": [1], "weight": 81}
    TreemanSpear = {"id": 0x0004000E, "volumes": [1], "weight": 83}
    StrormerSpear = {"id": 0x0004000F, "volumes": [1], "weight": 85}
    BerserkSpear = {"id": 0x00040010, "volumes": [1], "weight": 87}
    Sleipner = {"id": 0x00040011, "volumes": [1], "weight": 89}
    FairySpear = {"id": 0x00040012, "volumes": [1], "weight": 92}
    FiendSpear = {"id": 0x00040013, "volumes": [1], "weight": 95}
    # Rare Spears - Infection
    MilliondollarSpear = {"id": 0x0004003F, "volumes": [1], "weight": 96}
    ScarletAutumn = {"id": 0x00040041, "volumes": [1], "weight": 96}
    # Wands
    CypressWand = {"id": 0x00050000, "volumes": [1], "weight": 55}
    IronRod = {"id": 0x00050001, "volumes": [1], "weight": 57}
    EarthWand = {"id": 0x00050002, "volumes": [1], "weight": 59}
    WaterWand = {"id": 0x00050003, "volumes": [1], "weight": 61}
    FireWand = {"id": 0x00050004, "volumes": [1], "weight": 63}
    AirWand = {"id": 0x00050005, "volumes": [1], "weight": 65}
    ElectricWand = {"id": 0x00050006, "volumes": [1], "weight": 67}
    EbonyWand = {"id": 0x00050007, "volumes": [1], "weight": 69}
    WandOfWisdom = {"id": 0x00050008, "volumes": [1], "weight": 71}
    BashoWand = {"id": 0x00050009, "volumes": [1], "weight": 73}
    DiabolicWand = {"id": 0x0005000A, "volumes": [1], "weight": 75}
    EarthRod = {"id": 0x0005000B, "volumes": [1], "weight": 77}
    RodOfTheSea = {"id": 0x0005000C, "volumes": [1], "weight": 79}
    InfernoWand = {"id": 0x0005000D, "volumes": [1], "weight": 81}
    CedarWand = {"id": 0x0005000E, "volumes": [1], "weight": 83}
    WandOfStorms = {"id": 0x0005000F, "volumes": [1], "weight": 85}
    AdiansRod = {"id": 0x00050010, "volumes": [1], "weight": 87}
    AlmightyWand = {"id": 0x00050011, "volumes": [1], "weight": 90}
    GroovyStick = {"id": 0x000500012, "volumes": [1], "weight": 93}
    StarStormWand = {"id": 0x000500013, "volumes": [1], "weight": 95}
    # Rare Wands - Infection
    JestersWand = {"id": 0x000500040, "volumes": [1], "weight": 96}
    DarkHistory = {"id": 0x000500042, "volumes": [1], "weight": 96}
class Armors(Enum):
    _value_: EquipmentAttributes
    # Light Headgear - Infection
    Bandana = {"id": 0x00060000, "volumes": [1], "weight": 65}
    SteelCap = {"id": 0x00060001, "volumes": [1], "weight": 67}
    CougarBandana = {"id": 0x00060002, "volumes": [1], "weight": 70}
    RaccoonEarcap = {"id": 0x00060003, "volumes": [1], "weight": 74}
    NewtNecklace = {"id": 0x00060004, "volumes": [1], "weight": 79}
    ScarabEarring = {"id": 0x00060005, "volumes": [1], "weight": 85}
    ThunderTorque = {"id": 0x00060006, "volumes": [1], "weight": 92}
    # Rare Light Headgear - Infection
    TimeHeadband = {"id": 0x00060043, "volumes": [1], "weight": 95}
    # Medium Headgear - Infection
    NomadsHood = {"id": 0x00060014, "volumes": [1], "weight": 65}
    GuardCap = {"id": 0x00060015, "volumes": [1], "weight": 67}
    HuntersHood = {"id": 0x00060016, "volumes": [1], "weight": 70}
    IceHunterCap = {"id": 0x00060017, "volumes": [1], "weight": 74}
    FireDanceHat = {"id": 0x00060018, "volumes": [1], "weight": 79}
    PeasantsCap = {"id": 0x00060019, "volumes": [1], "weight": 85}
    LightningCap = {"id": 0x0006001A, "volumes": [1], "weight": 92}
    # Rare Medium Headgear - Infection
    GoblinCap = {"id": 0x0006003C, "volumes": [1], "weight": 80}
    # Heavy Headgear - Infection
    HeadGear = {"id": 0x00060028, "volumes": [1], "weight": 65}
    FaceGuard = {"id": 0x00060029, "volumes": [1], "weight": 67}
    MountainHelm = {"id": 0x0006002A, "volumes": [1], "weight": 70}
    IceHelm = {"id": 0x0006002B, "volumes": [1], "weight": 74}
    FireHelm = {"id": 0x0006002C, "volumes": [1], "weight": 79}
    ForesterHelm = {"id": 0x0006002D, "volumes": [1], "weight": 85}
    StormlordHelm = {"id": 0x0006002E, "volumes": [1], "weight": 92}
    # Rare Heavy Headgear - Infection
    CeramicHelm = {"id": 0x00060040, "volumes": [1], "weight": 97}
    # Light Body Armor - Infection
    LeatherCoat = {"id": 0x00070000, "volumes": [1], "weight": 65}
    NobleCloak = {"id": 0x00070001, "volumes": [1], "weight": 67}
    HikingGear = {"id": 0x00070002, "volumes": [1], "weight": 70}
    WinterCoat = {"id": 0x00070003, "volumes": [1], "weight": 74}
    FiremansCoat = {"id": 0x00070004, "volumes": [1], "weight": 79}
    LincolnGreen = {"id": 0x00070005, "volumes": [1], "weight": 85}
    ThunderCloak = {"id": 0x00070006, "volumes": [1], "weight": 92}
    # Rare Light Body Armor - Infection
    Kagayuzen = {"id": 0x00070040, "volumes": [1], "weight": 97}
    TimeSash = {"id": 0x00070042, "volumes": [1], "weight": 95}
    # Medium Body Armor - Infection
    LeatherArmor = {"id": 0x00070014, "volumes": [1], "weight": 65}
    RingMail = {"id": 0x00070015, "volumes": [1], "weight": 67}
    WyrmHide = {"id": 0x00070016, "volumes": [1], "weight": 70}
    WyrmScale = {"id": 0x00070017, "volumes": [1], "weight": 74}
    FiredrakeMail = {"id": 0x00070018, "volumes": [1], "weight": 79}
    HolyTreeMail = {"id": 0x00070019, "volumes": [1], "weight": 85}
    QuakebeastFur = {"id": 0x0007001A, "volumes": [1], "weight": 92}
    # Rare Medium Body Armor - Infection
    GoblinMail = {"id": 0x0007003C, "volumes": [1], "weight": 80}
    # Heavy Body Armor - Infection
    Brigandine = {"id": 0x00070028, "volumes": [1], "weight": 65}
    PlateArmor = {"id": 0x00070029, "volumes": [1], "weight": 67}
    GrandArmor = {"id": 0x0007002A, "volumes": [1], "weight": 70}
    FrostArmor = {"id": 0x0007002B, "volumes": [1], "weight": 74}
    BlazeArmor = {"id": 0x0007002C, "volumes": [1], "weight": 79}
    SpiritArmor = {"id": 0x0007002D, "volumes": [1], "weight": 85}
    ThunderArmor = {"id": 0x0007002E, "volumes": [1], "weight": 92}
    # Light Hand Armor - Infection
    WristBand = {"id": 0x00080000, "volumes": [1], "weight": 65}
    SilverBracer = {"id": 0x00080001, "volumes": [1], "weight": 67}
    FossilBracer = {"id": 0x00080002, "volumes": [1], "weight": 70}
    FrostBracer = {"id": 0x00080003, "volumes": [1], "weight": 74}
    FireBracer = {"id": 0x00080004, "volumes": [1], "weight": 79}
    AirBracer = {"id": 0x00080005, "volumes": [1], "weight": 85}
    StormBracer = {"id": 0x00080006, "volumes": [1], "weight": 92}
    # Rare Light Hand Armor - Infection
    TimeBracer = {"id": 0x00080041, "volumes": [1], "weight": 95}
    # Medium Hand Armor - Infection
    LeatherGloves = {"id": 0x00080014, "volumes": [1], "weight": 65}
    SilverGloves = {"id": 0x00080015, "volumes": [1], "weight": 67}
    MinersGloves = {"id": 0x00080016, "volumes": [1], "weight": 70}
    FishingGloves = {"id": 0x00080017, "volumes": [1], "weight": 74}
    SmithsGloves = {"id": 0x00080018, "volumes": [1], "weight": 79}
    ForestGloves = {"id": 0x00080019, "volumes": [1], "weight": 85}
    ThunderGloves = {"id": 0x0008001A, "volumes": [1], "weight": 92}
    # Rare Medium Hand Armor - Infection
    GoblinGloves = {"id": 0x0008003C, "volumes": [1], "weight": 80}
    # Heavy Hand Armor - Infection
    RustedHands = {"id": 0x00080028, "volumes": [1], "weight": 65}
    SilverHands = {"id": 0x00080029, "volumes": [1], "weight": 67}
    HandsOfEarth = {"id": 0x0008002A, "volumes": [1], "weight": 70}
    HandsOfWater = {"id": 0x0008002B, "volumes": [1], "weight": 74}
    HandsOfFire = {"id": 0x0008002C, "volumes": [1], "weight": 79}
    HandsOfWood = {"id": 0x0008002D, "volumes": [1], "weight": 85}
    HandsOfStorm = {"id": 0x0008002E, "volumes": [1], "weight": 92}
    # Light Leg Armor - Infection
    Sandals = {"id": 0x00090000, "volumes": [1], "weight": 65}
    LegMail = {"id": 0x00090001, "volumes": [1], "weight": 67}
    CeramicAnklet = {"id": 0x00090002, "volumes": [1], "weight": 70}
    FrostAnklet = {"id": 0x00090003, "volumes": [1], "weight": 74}
    IronAnklet = {"id": 0x00090004, "volumes": [1], "weight": 79}
    OakAnklet = {"id": 0x00090005, "volumes": [1], "weight": 85}
    ThunderAnklet = {"id": 0x00090006, "volumes": [1], "weight": 92}
    # Rare Light Leg Armor - Infection
    TimeSandals = {"id": 0x00090042, "volumes": [1], "weight": 95}
    # Medium Leg Armor - Infection
    SafetyShoes = {"id": 0x00090014, "volumes": [1], "weight": 65}
    JungleBoots = {"id": 0x00090015, "volumes": [1], "weight": 67}
    MountainBoots = {"id": 0x00090016, "volumes": [1], "weight": 70}
    SnowPanther = {"id": 0x00090017, "volumes": [1], "weight": 74}
    FireLizard = {"id": 0x00090018, "volumes": [1], "weight": 79}
    RangersBoots = {"id": 0x00090019, "volumes": [1], "weight": 85}
    ThunderBoots = {"id": 0x0009001A, "volumes": [1], "weight": 92}
    # Rare Medium Leg Armor - Infection
    GoblinBoots = {"id": 0x0009003C, "volumes": [1], "weight": 84}
    # Heavy Leg Armor - Infection
    UsedGreaves = {"id": 0x00090028, "volumes": [1], "weight": 65}
    LeatherLegs = {"id": 0x00090029, "volumes": [1], "weight": 67}
    MountainGuard = {"id": 0x0009002A, "volumes": [1], "weight": 70}
    AquaGuard = {"id": 0x0009002B, "volumes": [1], "weight": 74}
    FlareGuard = {"id": 0x0009002C, "volumes": [1], "weight": 79}
    GreenGuard = {"id": 0x0009002D, "volumes": [1], "weight": 85}
    ElectricGuard = {"id": 0x0009002E, "volumes": [1], "weight": 92}