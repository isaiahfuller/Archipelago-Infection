from abc import ABC
from typing import Dict


from .Strings import ItemNames, EventNames, PlayStatNames, ShopsanityNames, TradesanityNames


class VolumeAddresses(ABC):
    Items: Dict[str, int]
    Events: Dict[str, int]
    PlayStats: Dict[str, int]
    Shopsanity: Dict[str, int]
    Tradesanity: Dict[str, int]
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
    Shopsanity = {
        #Mac Anu - AP Items
        ShopsanityNames.MAWS1.name: 0xa47E05,
        ShopsanityNames.MAWS2.name: 0xa47E05,
        ShopsanityNames.MAWS3.name: 0xa47E05,
        ShopsanityNames.MAWS4.name: 0xa47E05,
        ShopsanityNames.MAWS5.name: 0xa47E05,
        ShopsanityNames.MAIS1.name: 0xa47E05,
        ShopsanityNames.MAIS2.name: 0xa47E05,
        ShopsanityNames.MAIS3.name: 0xa47E05,
        ShopsanityNames.MAIS4.name: 0xa47E06,
        ShopsanityNames.MAIS5.name: 0xa47E06,
        ShopsanityNames.MAMS1.name: 0xa47E06,
        ShopsanityNames.MAMS2.name: 0xa47E06,
        ShopsanityNames.MAMS3.name: 0xa47E06,
        ShopsanityNames.MAMS4.name: 0xa47E06,
        ShopsanityNames.MAMS5.name: 0xa47E06,
        #Dun Loireag AP Items
        ShopsanityNames.DLWS1.name: 0xa47E07,
        ShopsanityNames.DLWS2.name: 0xa47E07,
        ShopsanityNames.DLWS3.name: 0xa47E07,
        ShopsanityNames.DLWS4.name: 0xa47E07,
        ShopsanityNames.DLWS5.name: 0xa47E07,
        ShopsanityNames.DLIS1.name: 0xa47E07,
        ShopsanityNames.DLIS2.name: 0xa47E07,
        ShopsanityNames.DLIS3.name: 0xa47E07,
        ShopsanityNames.DLIS4.name: 0xa47E08,
        ShopsanityNames.DLIS5.name: 0xa47E08,
        ShopsanityNames.DLMS1.name: 0xa47E08,
        ShopsanityNames.DLMS2.name: 0xa47E08,
        ShopsanityNames.DLMS3.name: 0xa47E08,
        ShopsanityNames.DLMS4.name: 0xa47E08,
        ShopsanityNames.DLMS5.name: 0xa47E08,
    }
    Tradesanity = {
        TradesanityNames.Mia1.name: 0xA40814,
        TradesanityNames.Mia2.name: 0xA40818,
        TradesanityNames.Mia3.name: 0xA4081C,
        TradesanityNames.Orca1.name: 0xA40850,
        TradesanityNames.Orca2.name: 0xA40854,
        TradesanityNames.Orca3.name: 0xA40858,
        TradesanityNames.Marlo1.name: 0xA40890,
        TradesanityNames.Marlo2.name: 0xA40894,
        TradesanityNames.Marlo3.name: 0xA40898,
        TradesanityNames.Sanjuro1.name: 0xA408DC,
        TradesanityNames.Sanjuro2.name: 0xA408E0,
        TradesanityNames.Sanjuro3.name: 0xA408E4,
        TradesanityNames.NukeUsagimaru1.name: 0xA40910,
        TradesanityNames.NukeUsagimaru2.name: 0xA40914,
        TradesanityNames.NukeUsagimaru3.name: 0xA40918,
        TradesanityNames.Balmung1.name: 0xA40950,
        TradesanityNames.Balmung2.name: 0xA40954,
        TradesanityNames.Balmung3.name: 0xA40958,
        TradesanityNames.Moonstone1.name: 0xA40990,
        TradesanityNames.Moonstone2.name: 0xA40994,
        TradesanityNames.Moonstone3.name: 0xA40998,
        TradesanityNames.Piros1.name: 0xA409DC,
        TradesanityNames.Piros2.name: 0xA409E0,
        TradesanityNames.Piros3.name: 0xA409E4,
        TradesanityNames.Wiseman1.name: 0xA40A10,
        TradesanityNames.Wiseman2.name: 0xA40A14,
        TradesanityNames.Wiseman3.name: 0xA40A18,
        TradesanityNames.Elk1.name: 0xA40A5C,
        TradesanityNames.Elk2.name: 0xA40A60,
        TradesanityNames.Elk3.name: 0xA40A64,
        TradesanityNames.Natsume1.name: 0xA40A94,
        TradesanityNames.Natsume2.name: 0xA40A98,
        TradesanityNames.Natsume3.name: 0xA40A9C,
        TradesanityNames.Rachel1.name: 0xA40AD0,
        TradesanityNames.Rachel2.name: 0xA40AD4,
        TradesanityNames.Rachel3.name: 0xA40AD8,
        TradesanityNames.Gardenia1.name: 0xA40B1C,
        TradesanityNames.Gardenia2.name: 0xA40B20,
        TradesanityNames.Gardenia3.name: 0xA40B24,
        TradesanityNames.TerajimaRyoko1.name: 0xA40B50,
        TradesanityNames.TerajimaRyoko2.name: 0xA40B54,
        TradesanityNames.TerajimaRyoko3.name: 0xA40B58,
        TradesanityNames.BlackRose1.name: 0xA40B90,
        TradesanityNames.BlackRose2.name: 0xA40B94,
        TradesanityNames.BlackRose3.name: 0xA40B98,
        TradesanityNames.Mistral1.name: 0xA40BDC,
        TradesanityNames.Mistral2.name: 0xA40BE0,
        TradesanityNames.Mistral3.name: 0xA40BE4,
        TradesanityNames.Helba1.name: 0xA40C10,
        TradesanityNames.Helba2.name: 0xA40C14,
        TradesanityNames.Helba3.name: 0xA40C18,
        TradesanityNames.Wing.name: 0xA40C64,
        TradesanityNames.Macky.name: 0xA40CA4,
        TradesanityNames.NOVA.name: 0xA40CE4,
        TradesanityNames.Sachiko.name: 0xA40D24,
        TradesanityNames.Neja.name: 0xA40D64,
        TradesanityNames.Heavy.name: 0xA40DA4,
        TradesanityNames.Benkei.name: 0xA40DE0,
        TradesanityNames.Hayate.name: 0xA40E24,
        TradesanityNames.Task.name: 0xA40E64,
        TradesanityNames.Hinata.name: 0xA40EA4,
        TradesanityNames.AKichi.name: 0xA40EE4,
        TradesanityNames.Cleama.name: 0xA40F24,
        TradesanityNames.Grid.name: 0xA40F64,
        TradesanityNames.Quess.name: 0xA40FA4,
        TradesanityNames.Nekoshi.name: 0xA40FE4,
        TradesanityNames.Gyokuro.name: 0xA41024,
        TradesanityNames.Osugi.name: 0xA41064,
        TradesanityNames.Acerola.name: 0xA410A4,
        TradesanityNames.Borscht.name: 0xA410E4,
        TradesanityNames.M_78.name: 0xA41124,
        TradesanityNames.Yuckey.name: 0xA41164,
        TradesanityNames.Nijukata.name: 0xA411A4,
        TradesanityNames.Hirami.name: 0xA411E4,
        TradesanityNames.Henako.name: 0xA41224,
        TradesanityNames.BIG.name: 0xA41264,
        TradesanityNames.Yuji.name: 0xA412A4,
        TradesanityNames.Cima.name: 0xA412E8,
        TradesanityNames.Koji.name: 0xA41328,
        TradesanityNames.Crest.name: 0xA41364,
        TradesanityNames.Mayonusuke.name: 0xA413A4,
        TradesanityNames.Mutsuki.name: 0xA413E8,
        TradesanityNames.Oborozukiyo.name: 0xA41424,
        TradesanityNames.Bell.name: 0xA41464,
        TradesanityNames.Cossack_Leader.name: 0xA414A8,
        TradesanityNames.Alue.name: 0xA414E4,
        TradesanityNames.AlphaIchigiro.name: 0xA41524,
        TradesanityNames.NobleGrunty.name: 0xA41564,
        TradesanityNames.IronGrunty.name: 0xA415A4,
        TradesanityNames.PoisonGrunty.name: 0xA415E4,
    }

class MutationAddresses(VolumeAddresses):
    """"""


class OutbreakAddresses(VolumeAddresses):
    """"""


class QuarantineAddresses(VolumeAddresses):
    """"""
