from abc import ABC
from typing import Dict

from .Strings import ItemNames, EventNames, PlayStatNames, MonsterNames


class VolumeAddresses(ABC):
    Items: Dict[str, int]
    Events: Dict[str, int]
    PlayStats: Dict[str, int]
    Monsters: Dict[str, int]
    AreaWords: int
    WordLists: int
    FieldInfo: int
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
    FieldInfo = 0x315564
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
    Monsters = {
        MonsterNames.Razine1.name: 0xa46287,
        MonsterNames.Swordmanoid2.name: 0xa46288,
        MonsterNames.Gladiator3.name: 0xa46289,
        MonsterNames.Ochimusha4.name: 0xa4628a,
        MonsterNames.HeavyMetal6.name: 0xa4628c,
        MonsterNames.DarkRider8.name: 0xa4628E,
        MonsterNames.TetraArmor11.name: 0xa46291,
        MonsterNames.GeneralArmor13.name: 0xa46293,
        MonsterNames.Porolin14.name: 0xa46294,
        MonsterNames.MummyRipper15.name: 0xa46295,
        MonsterNames.CadetValkyrie20.name: 0xa4629E,
        MonsterNames.FreshValkyrie21.name: 0xa4629F,
        MonsterNames.LongLived23.name: 0xa4629D,
        MonsterNames.GrandMage24.name: 0xa462A2,
        MonsterNames.Flamer36.name: 0xa462B0,
        MonsterNames.FireWitch37.name: 0xa462B1,
        MonsterNames.WaterWitch38.name: 0xa462B2,
        MonsterNames.DarkWitch39.name: 0xa462B3,
        MonsterNames.Kakasinger49.name: 0xa462BDE,
        MonsterNames.Guardian50.name: 0xa462B8,
        MonsterNames.MetalEmperor52.name: 0xa462BA,
        MonsterNames.MuGuardian57.name: 0xa462BF,
        MonsterNames.Pippy67.name: 0xa462C9,
        MonsterNames.ChickenHand68.name: 0xa462CA,
        MonsterNames.WoodHarpy69.name: 0xa462CB,
        MonsterNames.PhoenixQueen72.name: 0xa462CE,
        MonsterNames.MonkeyCrab80.name: 0xa462D6,
        MonsterNames.SnipSnap81.name: 0xa462D7,
        MonsterNames.CrabTurtle82.name: 0xa462D8,
        MonsterNames.RedScissors83.name: 0xa462D9,
        MonsterNames.SquillaDemon84.name: 0xa462DA,
        MonsterNames.Mantis86.name: 0xa462DC,
        MonsterNames.ShieldMan91.name: 0xa462E1,
        MonsterNames.Moai105.name: 0xa462EF,
        MonsterNames.RockHead106.name: 0xa462F0,
        MonsterNames.MysteryRock107.name: 0xa462F1,
        MonsterNames.StoneTuttle114.name: 0xa462F8,
        MonsterNames.StoneTuttleDataBug116.name: 0xa462FA,
        MonsterNames.Minnow117.name: 0xa462FB,
        MonsterNames.SkyFish118.name: 0xa462FC,
        MonsterNames.ArrowFish119.name: 0xa462FD,
        MonsterNames.CycloShark123.name: 0xa46301,
        MonsterNames.HammerShark124.name: 0xa46302,
        MonsterNames.Gremlin130.name: 0xa46308,
        MonsterNames.Goblin131.name: 0xa46309,
        MonsterNames.Stehoney132.name: 0xa4630A,
        MonsterNames.Jonue133.name: 0xa4630B,
        MonsterNames.HobGoblin140.name: 0xa46312,
        MonsterNames.Zyan141.name: 0xa46313,
        MonsterNames.GoblinNight145.name: 0xa46317,
        MonsterNames.MetalGoblin146.name: 0xa46318,
        MonsterNames.Albert148.name: 0xa4631A,
        MonsterNames.MagicalGoblin152.name: 0xa4631E,
        MonsterNames.GoblinWiz153.name: 0xa4631F,
        MonsterNames.Martina155.name: 0xa46321,
        MonsterNames.Cannibal159.name: 0xa46325,
        MonsterNames.Ogre161.name: 0xa46327,
        MonsterNames.IronBallFreak163.name: 0xa46329,
        MonsterNames.LittleDoggie168.name: 0xa4632E,
        MonsterNames.SledDog169.name: 0xa4632F,
        MonsterNames.HellDoberman172.name: 0xa46332,
        MonsterNames.HellHound173.name: 0xa46333,
        MonsterNames.FlameHeads176.name: 0xa46336,
        MonsterNames.WiggleSnake179.name: 0xa46339,
        MonsterNames.Menhir180.name: 0xa4633A,
        MonsterNames.GoilMenhir181.name: 0xa4633B,
        MonsterNames.FiendMenhir184.name: 0xa4633E,
        MonsterNames.LimpKnife185.name: 0xa4633F,
        MonsterNames.DiscoKnife186.name: 0xa46340,
        MonsterNames.LambadaKnife187.name: 0xa46341,
        MonsterNames.DustCurse188.name: 0xa46342,
        MonsterNames.CursedBlades189.name: 0xa46343,
        MonsterNames.SwordofChaos190.name: 0xa46344,
        MonsterNames.ArmorShogun191.name: 0xa46345,
        MonsterNames.DragonPuppy194.name: 0xa46348,
        MonsterNames.Snakoid195.name: 0xa46349,
        MonsterNames.LeadSnakoid196.name: 0xa4634A,
        MonsterNames.RedWyrm200.name: 0xa4634E,
        MonsterNames.RedWyrmDataBug202.name: 0xa46350,
        MonsterNames.ParasiteDragon215.name: 0xa4635D,
        MonsterNames.TwinkleGrass219.name: 0xa46361,
        MonsterNames.MadGrass220.name: 0xa46362,
        MonsterNames.HungryGrass221.name: 0xa46363,
        MonsterNames.SnappyGrass222.name: 0xa46364,
        MonsterNames.WoodStock223.name: 0xa46365,
        MonsterNames.ThousandTrees224.name: 0xa46366,
        MonsterNames.WoodStockDataBug225.name: 0xa46367,
        MonsterNames.ScarletKing227.name: 0xa46369,
        MonsterNames.MushroomKing229.name: 0xa4636A,
        MonsterNames.Charmer230.name: 0xa4636C,
        MonsterNames.LamiaFighter231.name: 0xa4636D,
        MonsterNames.LamiaHunter232.name: 0xa4636E,
        MonsterNames.KillerSnaker234.name: 0xa46370,
        MonsterNames.KillerSnakerDataBug236.name: 0xa46372,
        MonsterNames.FakeMoney240.name: 0xa46377,
        MonsterNames.Mimic241.name: 0xa46378,
        MonsterNames.HellBox242.name: 0xa46379,
        MonsterNames.DeathHead246.name: 0xa4637C,
        MonsterNames.NomadicBones247.name: 0xa4637D,
        MonsterNames.LivingDead250.name: 0xa46380,
        MonsterNames.Headhunter253.name: 0xa46383,
        MonsterNames.HeadhunterDataBug256.name: 0xa46386,
        MonsterNames.Wiggly268.name: 0xa46392,
        MonsterNames.DeadlyMoth269.name: 0xa46393,
        MonsterNames.PhantomWing270.name: 0xa46394,
        MonsterNames.BeeArmy272.name: 0xa46396,
        MonsterNames.BeeAssault273.name: 0xa46397,
        MonsterNames.BabyWorm275.name: 0xa46399,
        MonsterNames.Odoro280.name: 0xa4639E,
        MonsterNames.Ectoplasm281.name: 0xa46398,
        MonsterNames.NoisyWisp282.name: 0xa463A0,
        MonsterNames.Halloween283.name: 0xa463A1,
        MonsterNames.ShiningEyes288.name: 0xa463A6,

    }

class MutationAddresses(VolumeAddresses):
    """"""


class OutbreakAddresses(VolumeAddresses):
    """"""


class QuarantineAddresses(VolumeAddresses):
    """"""
