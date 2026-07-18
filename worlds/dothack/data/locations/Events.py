from typing import NotRequired
from ..items.Servers import Servers
from enum import Enum
from typing import TypedDict


class InfectionEventAttributes(TypedDict):
    address: int
    bits: int
    volumes: list[int]
    server: NotRequired[Servers]


class InfectionEventBase(Enum):
    _value_: InfectionEventAttributes

    @classmethod
    def from_address(self, address: int):
        for member in self:
            if member.value["address"] == address:
                return member
        return None


class InfectionStoryEvents(InfectionEventBase):
    FirstDataBug = {"address": 0xa44f39, "bits": 0b00000100, "volumes": [1], "server": Servers.Delta}
    LearnGateHacking = {"address": 0xa44f52, "bits": 0b00000010, "volumes": [1], "server": Servers.Delta}
    SavedPiros = {"address": 0xa44f41, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    BoardProtected = {"address": 0xa44f5a, "bits": 0b00010000, "volumes": [1], "server": Servers.Delta}
    BlackRoseDungeon = {"address": 0xa44f6a, "bits": 0b00000100, "volumes": [1], "server": Servers.Theta}
    ElkMiaFavorite = {"address": 0xa44f71, "bits": 0b10000000, "volumes": [1], "server": Servers.Delta}
    PirosDiary = {"address": 0xa44f7b, "bits": 0b00100000, "volumes": [1], "server": Servers.Delta}
    MistralMeetUp = {"address": 0xa44f90, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    Epitaph00 = {"address": 0xa44f92, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    DescendentsOfFianna = {"address": 0xa44fa8, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    EpitaphQ = {"address": 0xa44fb0, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    MetMeg = {"address": 0xa44fb8, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}


class CompletionConditions(InfectionEventBase):
    SkeithDefeated = {"address": 0xa44fc0, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    ParasiteDragonDefeated = {"address": 0xa450b8, "bits": 0b00010000, "volumes": [1], "server": Servers.Theta}


class InfectionGoldenGoblins(InfectionEventBase):
    Stehony = {"address": 0xa45059, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Jonue = {"address": 0xa45061, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Zyan = {"address": 0xa45069, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Albert = {"address": 0xa45071, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Martina = {"address": 0xa45079, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}


class InfectionOptionalPartyMembers(InfectionEventBase):
    Sanjuro = {"address": 0xa45099, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Gardenia = {"address": 0xa450a2, "bits": 0b00000100, "volumes": [1], "server": Servers.Theta}
    Natsume = {"address": 0xa450b0, "bits": 0b10000000, "volumes": [1], "server": Servers.Delta}
    GracefulBook = {"address": 0xa450a9, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
