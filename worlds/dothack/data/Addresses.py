from abc import ABC
from typing import Dict

from .Strings import ItemNames, EventNames, PlayStatNames


class VolumeAddresses(ABC):
    Items: Dict[str, int]
    Events: Dict[str, int]
    PlayStats: Dict[str, int]
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


class MutationAddresses(VolumeAddresses):
    """"""


class OutbreakAddresses(VolumeAddresses):
    """"""


class QuarantineAddresses(VolumeAddresses):
    """"""
