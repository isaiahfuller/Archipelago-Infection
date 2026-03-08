from enum import IntEnum, auto, Enum
from BaseClasses import Item, ItemClassification


ADDRESS = 0xa41bf0


class InfectionPartyMemberBase(Enum):
    @classmethod
    def from_id(self, id: int):
        for member in self:
            if member.value["id"] == id:
                return member
        return None


class InfectionPartyMembers(InfectionPartyMemberBase):
    Mia = {"id": 1, "importance": ItemClassification.progression}
    Orca = {"id": 2, "importance": ItemClassification.progression}
    Marlo = {"id": 3, "importance": ItemClassification.filler}
    Sanjuro = {"id": 4, "importance": ItemClassification.useful}
    NukeUsagimaru = {"id": 5, "importance": ItemClassification.filler}
    Balmung = {"id": 6, "importance": ItemClassification.filler}
    Moonstone = {"id": 7, "importance": ItemClassification.filler}
    Piros = {"id": 8, "importance": ItemClassification.progression}
    Wiseman = {"id": 9, "importance": ItemClassification.filler}
    Elk = {"id": 10, "importance": ItemClassification.progression}
    Natsume = {"id": 11, "importance": ItemClassification.useful}
    Rachel = {"id": 12, "importance": ItemClassification.filler}
    Gardenia = {"id": 13, "importance": ItemClassification.progression}
    TerajimaRyoko = {"id": 14, "importance": ItemClassification.filler}
    BlackRose = {"id": 15, "importance": ItemClassification.progression}
    Mistral = {"id": 16, "importance": ItemClassification.progression}
    Helba = {"id": 17, "importance": ItemClassification.filler}
