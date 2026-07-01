from enum import Enum

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
    FortuneWire = {"id": 0x000d0000}
    SpriteOcarina = {"id": 0x000d0001}
    FairysOrb = {"id": 0x000d0002}


class VirusCores(Enum):
    VirusCoreA = {"id": 0xa406cc}
    VirusCoreB = {"id": 0xa406cd}
    VirusCoreC = {"id": 0xa406ce}

class GruntyFood(Enum):
    GoldenEgg = {"id": 0xA406E6}
    GruntMints = {"id": 0xA406E7}
    TwilightOnion = {"id": 0xA406E8}
    SnakyCactus = {"id": 0xA406E9}
    OhNoMelon = {"id": 0xA406EA}
    Cordyceps = {"id": 0xA406EB}
    WhiteCherry = {"id": 0xA406EC}
    RootVegetable = {"id": 0xA406ED}
    LaPumpkin = {"id": 0xA406EE}
    Mushroom = {"id": 0xA406EF}
    Mandragora = {"id": 0xA406F0}
    PineyApple = {"id": 0xA406F1}
    ImmatureEgg = {"id": 0xA406F2}
    BearCatEgg = {"id": 0xA406F3}
    InvisibleEgg = {"id": 0xA406F4}
    BloodyEgg = {"id": 0xA406F5}

class InfectionLevel(Enum):
    InfectionLevel = {"id": 0xA4613E}