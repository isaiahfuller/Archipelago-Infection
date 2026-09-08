from enum import Enum
from typing import TypedDict

class InfectionShopsanityAttributes(TypedDict):
    address: int
    bits: int
    volumes: list[int]

class InfectionTradesanityAttributes(TypedDict):
    address: int
    volumes: list[int]


class InfectionShopsanityBase(Enum):
    _value_: InfectionShopsanityAttributes

    @classmethod
    def from_address(cls, address: int):
        for member in cls:
            if member.value["address"] == address:
                return member
        return None

class InfectionTradesanityBase(Enum):
    _value_: InfectionTradesanityAttributes

    @classmethod
    def from_address(cls, address: int):
        for member in cls:
            if member.value["address"] == address:
                return member
        return None


class InfectionShopsanity(InfectionShopsanityBase):
    #Mac Anu AP Items
    MAWS1 = {"address": 0xa47e05, "bits": 0b00000001, "volumes": [1]}
    MAWS2 = {"address": 0xa47e05, "bits": 0b00000010, "volumes": [1]}
    MAWS3 = {"address": 0xa47E05, "bits": 0b00000100, "volumes": [1]}
    MAWS4 = {"address": 0xa47E05, "bits": 0b00001000, "volumes": [1]}
    MAWS5 = {"address": 0xa47E05, "bits": 0b00010000, "volumes": [1]}
    MAIS1 = {"address": 0xa47E05, "bits": 0b00100000, "volumes": [1]}
    MAIS2 = {"address": 0xa47E05, "bits": 0b01000000, "volumes": [1]}
    MAIS3 = {"address": 0xa47E05, "bits": 0b10000000, "volumes": [1]}
    MAIS4 = {"address": 0xa47E06, "bits": 0b00000001, "volumes": [1]}
    MAIS5 = {"address": 0xa47E06, "bits": 0b00000010, "volumes": [1]}
    MAMS1 = {"address": 0xa47E06, "bits": 0b00000100, "volumes": [1]}
    MAMS2 = {"address": 0xa47E06, "bits": 0b00001000, "volumes": [1]}
    MAMS3 = {"address": 0xa47E06, "bits": 0b00010000, "volumes": [1]}
    MAMS4 = {"address": 0xa47E06, "bits": 0b00100000, "volumes": [1]}
    MAMS5 = {"address": 0xa47E06, "bits": 0b01000000, "volumes": [1]}
    #Dun Loireag AP Items
    DLWS1 = {"address": 0xa47e07, "bits": 0b00000001, "volumes": [1]}
    DLWS2 = {"address": 0xa47e07, "bits": 0b00000010, "volumes": [1]}
    DLWS3 = {"address": 0xa47E07, "bits": 0b00000100, "volumes": [1]}
    DLWS4 = {"address": 0xa47E07, "bits": 0b00001000, "volumes": [1]}
    DLWS5 = {"address": 0xa47E07, "bits": 0b00010000, "volumes": [1]}
    DLIS1 = {"address": 0xa47E07, "bits": 0b00100000, "volumes": [1]}
    DLIS2 = {"address": 0xa47E07, "bits": 0b01000000, "volumes": [1]}
    DLIS3 = {"address": 0xa47E07, "bits": 0b10000000, "volumes": [1]}
    DLIS4 = {"address": 0xa47E08, "bits": 0b00000001, "volumes": [1]}
    DLIS5 = {"address": 0xa47E08, "bits": 0b00000010, "volumes": [1]}
    DLMS1 = {"address": 0xa47E08, "bits": 0b00000100, "volumes": [1]}
    DLMS2 = {"address": 0xa47E08, "bits": 0b00001000, "volumes": [1]}
    DLMS3 = {"address": 0xa47E08, "bits": 0b00010000, "volumes": [1]}
    DLMS4 = {"address": 0xa47E08, "bits": 0b00100000, "volumes": [1]}
    DLMS5 = {"address": 0xa47E08, "bits": 0b01000000, "volumes": [1]}

class InfectionTradesanity(InfectionTradesanityBase):
    # Target State: value == 0
    Mia1 = {"address": 0xA40814, "volumes": [1]}
    Mia2 = {"address": 0xA40818, "volumes": [1]}
    Mia3 = {"address": 0xA4081C, "volumes": [1]}
    Orca1 = {"address": 0xA40850, "volumes": [1]}
    Orca2 = {"address": 0xA40854, "volumes": [1]}
    Orca3 = {"address": 0xA40858, "volumes": [1]}
    Marlo1 = {"address": 0xA40890, "volumes": [1]}
    Marlo2 = {"address": 0xA40894, "volumes": [1]}
    Marlo3 = {"address": 0xA40898, "volumes": [1]}
    Sanjuro1 = {"address": 0xA408DC, "volumes": [1]}
    Sanjuro2 = {"address": 0xA408E0, "volumes": [1]}
    Sanjuro3 = {"address": 0xA408E4, "volumes": [1]}
    NukeUsagimaru1 = {"address": 0xA40910, "volumes": [1]}
    NukeUsagimaru2 = {"address": 0xA40914, "volumes": [1]}
    NukeUsagimaru3 = {"address": 0xA40918, "volumes": [1]}
    Balmung1 = {"address": 0xA40950, "volumes": [1]}
    Balmung2 = {"address": 0xA40954, "volumes": [1]}
    Balmung3 = {"address": 0xA40958, "volumes": [1]}
    Moonstone1 = {"address": 0xA40990, "volumes": [1]}
    Moonstone2 = {"address": 0xA40994, "volumes": [1]}
    Moonstone3 = {"address": 0xA40998, "volumes": [1]}
    Piros1 = {"address": 0xA409DC, "volumes": [1]}
    Piros2 = {"address": 0xA409E0, "volumes": [1]}
    Piros3 = {"address": 0xA409E4, "volumes": [1]}
    Wiseman1 = {"address": 0xA40A10, "volumes": [1]}
    Wiseman2 = {"address": 0xA40A14, "volumes": [1]}
    Wiseman3 = {"address": 0xA40A18, "volumes": [1]}
    Elk1 = {"address": 0xA40A5C, "volumes": [1]}
    Elk2 = {"address": 0xA40A60, "volumes": [1]}
    Elk3 = {"address": 0xA40A64, "volumes": [1]}
    Natsume1 = {"address": 0xA40A94, "volumes": [1]}
    Natsume2 = {"address": 0xA40A98, "volumes": [1]}
    Natsume3 = {"address": 0xA40A9C, "volumes": [1]}
    Rachel1 = {"address": 0xA40AD0, "volumes": [1]}
    Rachel2 ={"address": 0xA40AD4, "volumes": [1]}
    Rachel3 = {"address": 0xA40AD8, "volumes": [1]}
    Gardenia1 = {"address": 0xA40B1C, "volumes": [1]}
    Gardenia2 = {"address": 0xA40B20, "volumes": [1]}
    Gardenia3 = {"address": 0xA40B24, "volumes": [1]}
    TerajimaRyoko1 = {"address": 0xA40B50, "volumes": [1]}
    TerajimaRyoko2 = {"address": 0xA40B54, "volumes": [1]}
    TerajimaRyoko3 = {"address": 0xA40B58, "volumes": [1]}
    BlackRose1 = {"address": 0xA40B90, "volumes": [1]}
    BlackRose2 = {"address": 0xA40B94, "volumes": [1]}
    BlackRose3 = {"address": 0xA40B98, "volumes": [1]}
    Mistral1 = {"address": 0xA40BDC, "volumes": [1]}
    Mistral2 = {"address": 0xA40BE0, "volumes": [1]}
    Mistral3 = {"address": 0xA40BE4, "volumes": [1]}
    Helba1 = {"address": 0xA40C10, "volumes": [1]}
    Helba2 = {"address": 0xA40C14, "volumes": [1]}
    Helba3 = {"address": 0xA40C18, "volumes": [1]}
    Wing = {"address": 0xA40C64, "volumes": [1]}
    Macky = {"address": 0xA40CA4, "volumes": [1]}
    NOVA = {"address": 0xA40CE4, "volumes": [1]}
    Sachiko = {"address": 0xA40D24, "volumes": [1]}
    Neja = {"address": 0xA40D64, "volumes": [1]}
    Heavy = {"address": 0xA40DA4, "volumes": [1]}
    Benkei = {"address": 0xA40DE4, "volumes": [1]}
    Hayate = {"address": 0xA40E24, "volumes": [1]}
    Task = {"address": 0xA40E64, "volumes": [1]}
    Hinata = {"address": 0xA40EA4, "volumes": [1]}
    AKichi = {"address": 0xA40EE4, "volumes": [1]}
    Cleama = {"address": 0xA40F24, "volumes": [1]}
    Grid = {"address": 0xA40F64, "volumes": [1]}
    Quess = {"address": 0xA40FA4, "volumes": [1]}
    Nekoshi = {"address": 0xA40FE4, "volumes": [1]}
    Gyokuro = {"address": 0xA41024, "volumes": [1]}
    Osugi = {"address": 0xA41064, "volumes": [1]}
    Acerola = {"address": 0xA410A4, "volumes": [1]}
    Borscht = {"address": 0xA410E4, "volumes": [1]}
    M_78 = {"address": 0xA41124, "volumes": [1]}
    Yuckey = {"address": 0xA41164, "volumes": [1]}
    Nijukata = {"address": 0xA411A4, "volumes": [1]}
    Hirami = {"address": 0xA411E4, "volumes": [1]}
    Henako = {"address": 0xA41224, "volumes": [1]}
    BIG = {"address": 0xA41264, "volumes": [1]}
    Yuji = {"address": 0xA412A4, "volumes": [1]}
    Cima = {"address": 0xA412E8, "volumes": [1]}
    Koji = {"address": 0xA41328, "volumes": [1]}
    Crest = {"address": 0xA41364, "volumes": [1]}
    Mayonusuke = {"address": 0xA413A4, "volumes": [1]}
    Mutsuki = {"address": 0xA413E8, "volumes": [1]}
    Oborozukiyo = {"address": 0xA41424, "volumes": [1]}
    Bell = {"address": 0xA41464, "volumes": [1]}
    Cossack_Leader = {"address": 0xA414A8, "volumes": [1]}
    Alue = {"address": 0xA414E4, "volumes": [1]}
    AlphaIchigiro = {"address": 0xA41524, "volumes": [1]}
    NobleGrunty = {"address": 0xA41564, "volumes": [1]}
    IronGrunty = {"address": 0xA415A4, "volumes": [1]}
    PoisonGrunty = {"address": 0xA415E4, "volumes": [1]}

class APItems(Enum):
    APItem1 = 0x010F003B
    APItem2 = 0x010F011F
    APItem3 = 0x010F0120
    APItem4 = 0x010F0121
    APItem5 = 0x010F0122


class TradingLists:
    name: str
    offset: int
    index: int

    @property
    def pm_trade(self) -> int:
        """Calculates the memory address for the specific Party Member."""
        base_address = 0xA4080C
        size = 0x11
        return base_address + (self.index * size + 0x40)

    def npc_trade(self) -> int:
        """Calculates the memory address for the specific NPC/Grunty."""
        base_address = 0xA40C64
        size = 0x27
        return base_address + (self.index * size + 0x40)
