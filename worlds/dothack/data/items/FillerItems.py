from enum import Enum
from typing import TypedDict


class ItemDict(TypedDict):
    id: int
    weight: int


class Consumables(Enum):
    _value_: ItemDict
    HealthDrink = {"id": 0x000a0000, "weight": 45}
    HealthPotion = {"id": 0x000a0001, "weight": 60}
    HealingElixer = {"id": 0x000a0002, "weight": 85}
    Antidote = {"id": 0x000a0003, "weight": 45}
    Restorative = {"id": 0x000a0004, "weight": 45}
    Resurrect = {"id": 0x000a0005, "weight": 80}
    WarriorBlood = {"id": 0x000a0006, "weight": 35}
    KnightBlood = {"id": 0x000a0007, "weight": 35}
    HunterBlood = {"id": 0x000a0008, "weight": 35}
    HermitBlood = {"id": 0x000a0009, "weight": 35}
    BeastBlood = {"id": 0x000a000A, "weight": 35}
    WizardBlood = {"id": 0x000a000B, "weight": 35}
    WellWater = {"id": 0x000a000C, "weight": 25}
    PureWater = {"id": 0x000a000D, "weight": 25}
    BurningOil = {"id": 0x000a000E, "weight": 25}
    HolySap = {"id": 0x000a000F, "weight": 25}
    SportsDrink = {"id": 0x000a0010, "weight": 25}
    CookedBile = {"id": 0x000a0011, "weight": 25}
    MagesSoul = {"id": 0x000a0012, "weight": 80}
    ArtisansSoul = {"id": 0x000a0013, "weight": 85}
    EmperorsSoul = {"id": 0x000a0014, "weight": 90}
    NobleWine = {"id": 0x000a0015, "weight": 95}
    RiskyCoffee = {"id": 0x000a0016, "weight": 95}
    RecoveryDrink = {"id": 0x000a0017, "weight": 85}
    ##Spell Scrolls
    RainingRocks = {"id": 0x000B000, "weight": 35}
    RagingEarth = {"id": 0x000B001, "weight": 35}
    StoneStorm = {"id": 0x000B0002, "weight": 45}
    GaiasSpell = {"id": 0x000B0003, "weight": 45}
    MeteorStrike = {"id": 0x000B0004, "weight": 65}
    CosmicTruth = {"id": 0x000B0005, "weight": 65}
    IceStorm = {"id": 0x000B0006, "weight": 35}
    IceFloe = {"id": 0x000B0007, "weight": 35}
    IceStrike = {"id": 0x000B0008, "weight": 45}
    Cygnus = {"id": 0x000B0009, "weight": 45}
    AbsoluteZero = {"id": 0x000B000A, "weight": 65}
    Permafrost = {"id": 0x000B000B, "weight": 65}
    FireTempest = {"id": 0x000B000C, "weight": 35}
    MeteorSwarm = {"id": 0x000B000D, "weight": 35}
    FlameBlast = {"id": 0x000B000E, "weight": 45}
    FireballStorm = {"id": 0x000B000F, "weight": 45}
    Hellstorm = {"id": 0x000B0010, "weight": 65}
    InfernoStrike = {"id": 0x000B0011, "weight": 65}
    GreenGale = {"id": 0x000B0012, "weight": 35}
    GaleBreath = {"id": 0x000B0013, "weight": 35}
    Leafblight = {"id": 0x000B0014, "weight": 45}
    WoodSprite = {"id": 0x000B0015, "weight": 45}
    JungleRage = {"id": 0x000B0016, "weight": 65}
    ForestOfFear = {"id": 0x000B0017, "weight": 65}
    LightningBolt = {"id": 0x000B0018, "weight": 35}
    PlasmaStorm = {"id": 0x000B0019, "weight": 35}
    IonStrike = {"id": 0x000B001A, "weight": 45}
    RagingPlasma = {"id": 0x000B001B, "weight": 45}
    Thunderbolt = {"id": 0x000B001C, "weight": 65}
    PlasmaGale = {"id": 0x000B001D, "weight": 65}
    Nightblight = {"id": 0x000B001E, "weight": 35}
    DarkNight = {"id": 0x000B001F, "weight": 35}
    DarkTraitor = {"id": 0x000B0020, "weight": 45}
    ChaosSpell = {"id": 0x000B0021, "weight": 45}
    Nightfear = {"id": 0x000B0022, "weight": 65}
    Nightshade = {"id": 0x000B0023, "weight": 65}
    TheDeath = {"id": 0x000B0024, "weight": 35}
    TheHangedMan = {"id": 0x000B0025, "weight": 35}
    TheLovers = {"id": 0x000B0026, "weight": 35}
    TheMoon = {"id": 0x000B0027, "weight": 35}
    TheFool = {"id": 0x000B0028, "weight": 35}
    TheDevil = {"id": 0x000B0029, "weight": 35}
    WarriorsBane = {"id": 0x000B002A, "weight": 40}
    KnightsBane = {"id": 0x000B002B, "weight": 40}
    HuntersBane = {"id": 0x000B002C, "weight": 40}
    HermitsBane = {"id": 0x000B002D, "weight": 40}
    BeastsBane = {"id": 0x000B002E, "weight": 40}
    WizardsBane = {"id": 0x000B002F, "weight": 40}
    Stonebane = {"id": 0x000B0030, "weight": 30}
    Waterbane = {"id": 0x000B0031, "weight": 30}
    Firebane = {"id": 0x000B0032, "weight": 30}
    Treebane = {"id": 0x000B0033, "weight": 30}
    Lightbane = {"id": 0x000B0034, "weight": 30}
    Nightbane = {"id": 0x000B0035, "weight": 30}
    HealthCharm = {"id": 0x000B0036, "weight": 55}
    SoulCharm = {"id": 0x000B0037, "weight": 70}
    SpeedCharm = {"id": 0x000B0038, "weight": 50}
    LightCross = {"id": 0x000B0039, "weight": 60}
    HaleCross = {"id": 0x000B003A, "weight": 70}
    DivineCross = {"id": 0x000B003B, "weight": 85}
    SummonEarth = {"id": 0x000B003C, "weight": 70}
    SummonWater = {"id": 0x000B003D, "weight": 70}
    SummonFire = {"id": 0x000B003E, "weight": 70}
    SummonWood = {"id": 0x000B003F, "weight": 70}
    SummonThunder = {"id": 0x000B0040, "weight": 70}
    SummonNight = {"id": 0x000B0041, "weight": 70}
    Stonecall = {"id": 0x000B0042, "weight": 85}
    Aquacall = {"id": 0x000B0043, "weight": 85}
    Infernocall = {"id": 0x000B0044, "weight": 85}
    Greencall = {"id": 0x000B0045, "weight": 85}
    Thundercall = {"id": 0x000B0046, "weight": 85}
    Nightcall = {"id": 0x000B0047, "weight": 85}
    ##Miscellaneous Items
    FortuneWire = {"id": 0x000d0000, "weight": 35}
    SpriteOcarina = {"id": 0x000d0001, "weight": 35}
    FairysOrb = {"id": 0x000d0002, "weight": 35}
    ##Gott Treasures - Infection
    GruntDoll = {"id": 0x000E0000, "weight": 40}
    RainbowCard = {"id": 0x000E0001, "weight": 45}
    YellowCandy = {"id": 0x000E0002, "weight": 60}
    SilverScarab = {"id": 0x000E0003, "weight": 75}
    ## Rare Items
    PowerBook = {"id": 0x000C0000, "weight": 90}
    ToleranceBook = {"id": 0x000C0001, "weight": 90}
    InsightBook = {"id": 0x000C0002, "weight": 90}
    SpiritualBook = {"id": 0x000C0003, "weight": 90}
    GracefulBook = {"id": 0x000C0004, "weight": 90}
    SwiftBook = {"id": 0x000C0005, "weight": 90}
    FengShui = {"id": 0x000C0006, "weight": 90}
    WaterMagic = {"id": 0x000C0007, "weight": 85}
    FireMagic = {"id": 0x000C0008, "weight": 85}
    WoodMagic = {"id": 0x000C0009, "weight": 85}
    ThunderMagic = {"id": 0x000C000A, "weight": 85}
    BlackMagic = {"id": 0x000C000B, "weight": 85}
    SecretMight = {"id": 0x000C000C, "weight": 95}
    SecretRigid = {"id": 0x000C000D, "weight": 95}
    SecretAwaken = {"id": 0x000C000E, "weight": 95}
    SecretReason = {"id": 0x000C000F, "weight": 95}
    SecretDivine = {"id": 0x000C0010, "weight": 95}
    SecretThief = {"id": 0x000C0011, "weight": 95}
    Earthlore = {"id": 0x000C0012, "weight": 90}
    Sealore = {"id": 0x000C0013, "weight": 90}
    Firelore = {"id": 0x000C0014, "weight": 90}
    Forestlore = {"id": 0x000C0015, "weight": 90}
    Stormlore = {"id": 0x000C0016, "weight": 90}
    Darklore = {"id": 0x000C0017, "weight": 90}
    PirosDiary = {"id": 0x000C0018, "weight": 55}
    BLYokohama = {"id": 0x000C0019, "weight": 90}
    BookOfIdeals = {"id": 0x000C001A, "weight": 97}
    BookOfIdeas = {"id": 0x000C001B, "weight": 97}
    SecretSage = {"id": 0x000C001C, "weight": 97}
    SecretDreams = {"id": 0x000C001D, "weight": 97}
    GoldenGrunty = {"id": 0x000C001E, "weight": 98}
    SilverGrunty = {"id": 0x000C001F, "weight": 98}
    EnergySutras = {"id": 0x000C0020, "weight": 96}
    SpiritSutras = {"id": 0x000C0021, "weight": 96}

class VirusCores(Enum):
    _value_: ItemDict
    VirusCoreA = {"id": 0xa406cc, "weight": 40}
    VirusCoreB = {"id": 0xa406cd, "weight": 40}
    VirusCoreC = {"id": 0xa406ce, "weight": 40}


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

class InfectionLevel(Enum):
    InfectionLevel = {"id": 0xA4613E, "weight": 25}