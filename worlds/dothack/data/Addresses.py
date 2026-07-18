from abc import ABC
from typing import Dict

from .Strings import ItemNames, EventNames, PlayStatNames, MonsterNamesInfection


class VolumeAddresses(ABC):
    Items: Dict[str, int]
    Events: Dict[str, int]
    PlayStats: Dict[str, int]
    MonsterNames: Dict[str, int]
    AreaWords: int
    WordLists: int
    Storage: int
    Party: int
    Servers: int
    CurrentlyEntered: int
    IngameStatus: int
    IngameOverlay: int
    LastItemIdx: int
    KiteClass: int


class InfectionAddresses(VolumeAddresses):
    AreaWords = 0xa44c0c
    WordLists = 0xa44c47
    Storage = 0xa40540
    Party = 0xa41bf0
    Servers = 0xa41c04
    CurrentlyEntered = 0xADA71C
    IngameStatus = 0xa3f5f0
    IngameOverlay = 0x00400804
    LastItemIdx = 0xa44ec8
    KiteClass = 0xa46f30

    Items = {
        ItemNames.VirusCoreA.name: 0xa406cc,
        ItemNames.VirusCoreB.name: 0xa406cd,
        ItemNames.VirusCoreC.name: 0xa406ce,
        ItemNames.RyuBookI.name: 0xA407DD,
        ItemNames.RyuBookII.name: 0xA407DE,
        ItemNames.RyuBookIII.name: 0xA407DF,
        ItemNames.RyuBookIV.name: 0xA407E0,
        ItemNames.RyuBookV.name: 0xA407E1,
        ItemNames.RyuBookVI.name: 0xA407E2,
        ItemNames.RyuBookVII.name: 0xA407E3,
        ItemNames.RyuBookVIII.name: 0xA407E4,
        ItemNames.GoldenEgg.name: 0xA406E6,
        ItemNames.GruntMints.name: 0xA406E7,
        ItemNames.TwilightOnion.name: 0xA406E8,
        ItemNames.SnakyCactus.name: 0xA406E9,
        ItemNames.OhNoMelon.name: 0xA406EA,
        ItemNames.Cordyceps.name: 0xA406EB,
        ItemNames.WhiteCherry.name: 0xA406EC,
        ItemNames.RootVegetable.name: 0xA406ED,
        ItemNames.LaPumpkin.name: 0xA406EE,
        ItemNames.Mushroom.name: 0xA406EF,
        ItemNames.Mandragora.name: 0xA406F0,
        ItemNames.PineyApple.name: 0xA406F1,
        ItemNames.ImmatureEgg.name: 0xA406F2,
        ItemNames.BearCatEgg.name: 0xA406F3,
        ItemNames.InvisibleEgg.name: 0xA406F4,
        ItemNames.BloodyEgg.name: 0xA406F5,
        ItemNames.InfectionLevel.name: 0xA4613E

    }
    Events = {
        EventNames.Stehony.name: 0xa45059,
        EventNames.Jonue.name: 0xa45061,
        EventNames.Zyan.name: 0xa45069,
        EventNames.Albert.name: 0xa45071,
        EventNames.Martina.name: 0xa45079,
        EventNames.Sanjuro.name: 0xa45099,
        EventNames.Gardenia.name: 0xa450a2,
        EventNames.Natsume.name: 0xa450b0,
        EventNames.GracefulBook.name: 0xa450a9,
    }
    PlayStats = {
        PlayStatNames.AreasVisited.name: 0xa46232,
        PlayStatNames.AllFieldPortalsOpened.name: 0xa46236,
        PlayStatNames.AllDungeonPortalsOpened.name: 0xa46238,
        PlayStatNames.PortalsOpened.name: 0xa46234,
        PlayStatNames.ChestsOpened.name: 0xa46e10,
        PlayStatNames.BreakablesBroken.name: 0xa46e12,
        PlayStatNames.GottOpened.name: 0xa46e3e,
        PlayStatNames.SymbolsActivated.name: 0xa46e14,
        PlayStatNames.TotalDataDrains.name: 0xa4622e,
        PlayStatNames.KiteLevel.name: 0xa46e66,
    }
    MonsterNames = {
        MonsterNamesInfection.Razine1.name: 0xa46287,
        MonsterNamesInfection.Swordmanoid2.name: 0xa46288,
        MonsterNamesInfection.Gladiator3.name: 0xa46289,
        MonsterNamesInfection.Ochimusha4.name: 0xa4628a,
        MonsterNamesInfection.HeavyMetal6.name: 0xa4628c,
        MonsterNamesInfection.DarkRider8.name: 0xa4628E,
        MonsterNamesInfection.TetraArmor11.name: 0xa46291,
        MonsterNamesInfection.GeneralArmor13.name: 0xa46293,
        MonsterNamesInfection.Porolin14.name: 0xa46294,
        MonsterNamesInfection.MummyRipper15.name: 0xa46295,
        MonsterNamesInfection.CadetValkyrie20.name: 0xa4629E,
        MonsterNamesInfection.FreshValkyrie21.name: 0xa4629F,
        MonsterNamesInfection.LongLived23.name: 0xa4629D,
        MonsterNamesInfection.GrandMage24.name: 0xa462A2,
        MonsterNamesInfection.Flamer36.name: 0xa462B0,
        MonsterNamesInfection.FireWitch37.name: 0xa462B1,
        MonsterNamesInfection.WaterWitch38.name: 0xa462B2,
        MonsterNamesInfection.DarkWitch39.name: 0xa462B3,
        MonsterNamesInfection.Kakasinger49.name: 0xa462BDE,
        MonsterNamesInfection.Guardian50.name: 0xa462B8,
        MonsterNamesInfection.MetalEmperor52.name: 0xa462BA,
        MonsterNamesInfection.MuGuardian57.name: 0xa462BF,
        MonsterNamesInfection.Pippy67.name: 0xa462C9,
        MonsterNamesInfection.ChickenHand68.name: 0xa462CA,
        MonsterNamesInfection.WoodHarpy69.name: 0xa462CB,
        MonsterNamesInfection.PhoenixQueen72.name: 0xa462CE,
        MonsterNamesInfection.MonkeyCrab80.name: 0xa462D6,
        MonsterNamesInfection.SnipSnap81.name: 0xa462D7,
        MonsterNamesInfection.CrabTurtle82.name: 0xa462D8,
        MonsterNamesInfection.RedScissors83.name: 0xa462D9,
        MonsterNamesInfection.SquillaDemon84.name: 0xa462DA,
        MonsterNamesInfection.Mantis86.name: 0xa462DC,
        MonsterNamesInfection.ShieldMan91.name: 0xa462E1,
        MonsterNamesInfection.Moai105.name: 0xa462EF,
        MonsterNamesInfection.RockHead106.name: 0xa462F0,
        MonsterNamesInfection.MysteryRock107.name: 0xa462F1,
        MonsterNamesInfection.StoneTuttle114.name: 0xa462F8,
        MonsterNamesInfection.StoneTuttleDataBug116.name: 0xa462FA,
        MonsterNamesInfection.Minnow117.name: 0xa462FB,
        MonsterNamesInfection.SkyFish118.name: 0xa462FC,
        MonsterNamesInfection.ArrowFish119.name: 0xa462FD,
        MonsterNamesInfection.CycloShark123.name: 0xa46301,
        MonsterNamesInfection.HammerShark124.name: 0xa46302,
        MonsterNamesInfection.Gremlin130.name: 0xa46308,
        MonsterNamesInfection.Goblin131.name: 0xa46309,
        MonsterNamesInfection.Stehoney132.name: 0xa4630A,
        MonsterNamesInfection.Jonue133.name: 0xa4630B,
        MonsterNamesInfection.HobGoblin140.name: 0xa46312,
        MonsterNamesInfection.Zyan141.name: 0xa46313,
        MonsterNamesInfection.GoblinNight145.name: 0xa46317,
        MonsterNamesInfection.MetalGoblin146.name: 0xa46318,
        MonsterNamesInfection.Albert148.name: 0xa4631A,
        MonsterNamesInfection.MagicalGoblin152.name: 0xa4631E,
        MonsterNamesInfection.GoblinWiz153.name: 0xa4631F,
        MonsterNamesInfection.Martina155.name: 0xa46321,
        MonsterNamesInfection.Cannibal159.name: 0xa46325,
        MonsterNamesInfection.Ogre161.name: 0xa46327,
        MonsterNamesInfection.IronBallFreak163.name: 0xa46329,
        MonsterNamesInfection.LittleDoggie168.name: 0xa4632E,
        MonsterNamesInfection.SledDog169.name: 0xa4632F,
        MonsterNamesInfection.HellDoberman172.name: 0xa46332,
        MonsterNamesInfection.HellHound173.name: 0xa46333,
        MonsterNamesInfection.FlameHeads176.name: 0xa46336,
        MonsterNamesInfection.WiggleSnake179.name: 0xa46339,
        MonsterNamesInfection.Menhir180.name: 0xa4633A,
        MonsterNamesInfection.GoilMenhir181.name: 0xa4633B,
        MonsterNamesInfection.FiendMenhir184.name: 0xa4633E,
        MonsterNamesInfection.LimpKnife185.name: 0xa4633F,
        MonsterNamesInfection.DiscoKnife186.name: 0xa46340,
        MonsterNamesInfection.LambadaKnife187.name: 0xa46341,
        MonsterNamesInfection.DustCurse188.name: 0xa46342,
        MonsterNamesInfection.CursedBlades189.name: 0xa46343,
        MonsterNamesInfection.SwordofChaos190.name: 0xa46344,
        MonsterNamesInfection.ArmorShogun191.name: 0xa46345,
        MonsterNamesInfection.DragonPuppy194.name: 0xa46348,
        MonsterNamesInfection.Snakoid195.name: 0xa46349,
        MonsterNamesInfection.LeadSnakoid196.name: 0xa4634A,
        MonsterNamesInfection.RedWyrm200.name: 0xa4634E,
        MonsterNamesInfection.RedWyrmDataBug202.name: 0xa46350,
        MonsterNamesInfection.ParasiteDragon215.name: 0xa4635D,
        MonsterNamesInfection.TwinkleGrass219.name: 0xa46361,
        MonsterNamesInfection.MadGrass220.name: 0xa46362,
        MonsterNamesInfection.HungryGrass221.name: 0xa46363,
        MonsterNamesInfection.SnappyGrass222.name: 0xa46364,
        MonsterNamesInfection.WoodStock223.name: 0xa46365,
        MonsterNamesInfection.ThousandTrees224.name: 0xa46366,
        MonsterNamesInfection.WoodStockDataBug225.name: 0xa46367,
        MonsterNamesInfection.ScarletKing227.name: 0xa46369,
        MonsterNamesInfection.MushroomKing229.name: 0xa4636A,
        MonsterNamesInfection.Charmer230.name: 0xa4636C,
        MonsterNamesInfection.LamiaFighter231.name: 0xa4636D,
        MonsterNamesInfection.LamiaHunter232.name: 0xa4636E,
        MonsterNamesInfection.KillerSnaker234.name: 0xa46370,
        MonsterNamesInfection.KillerSnakerDataBug236.name: 0xa46372,
        MonsterNamesInfection.FakeMoney240.name: 0xa46377,
        MonsterNamesInfection.Mimic241.name: 0xa46378,
        MonsterNamesInfection.HellBox242.name: 0xa46379,
        MonsterNamesInfection.DeathHead246.name: 0xa4637C,
        MonsterNamesInfection.NomadicBones247.name: 0xa4637D,
        MonsterNamesInfection.LivingDead250.name: 0xa46380,
        MonsterNamesInfection.Headhunter253.name: 0xa46383,
        MonsterNamesInfection.HeadhunterDataBug256.name: 0xa46386,
        MonsterNamesInfection.Wiggly268.name: 0xa46392,
        MonsterNamesInfection.DeadlyMoth269.name: 0xa46393,
        MonsterNamesInfection.PhantomWing270.name: 0xa46394,
        MonsterNamesInfection.BeeArmy272.name: 0xa46396,
        MonsterNamesInfection.BeeAssault273.name: 0xa46397,
        MonsterNamesInfection.BabyWorm275.name: 0xa46399,
        MonsterNamesInfection.Odoro280.name: 0xa4639E,
        MonsterNamesInfection.Ectoplasm281.name: 0xa46398,
        MonsterNamesInfection.NoisyWisp282.name: 0xa463A0,
        MonsterNamesInfection.Halloween283.name: 0xa463A1,
        MonsterNamesInfection.ShiningEyes288.name: 0xa463A6,

    }

class MutationAddresses(VolumeAddresses):
    """"""


class OutbreakAddresses(VolumeAddresses):
    """"""


class QuarantineAddresses(VolumeAddresses):
    """"""
