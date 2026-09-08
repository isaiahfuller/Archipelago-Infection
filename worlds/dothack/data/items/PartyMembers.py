from enum import Enum
from typing import TypedDict
from BaseClasses import ItemClassification


class PartyMemberAttributes(TypedDict):
    id: int
    classifications: dict[int, ItemClassification]
    volumes: list[int]
    weight: int


class PartyMembers(Enum):
    _value_: PartyMemberAttributes

    @classmethod
    def from_id(self, id: int):
        for member in self:
            if member.value["id"] == id:
                return member
        return None
    Mia = {"id": 1, "classifications": {1: ItemClassification.progression}, "volumes": [1], "weight": 85}
    Orca = {"id": 2, "classifications": {1: ItemClassification.useful}, "volumes": [1], "weight": 98}
    Marlo = {"id": 3, "classifications": {1: ItemClassification.useful}, "volumes": [1], "weight": 93}
    Sanjuro = {"id": 4, "classifications": {1: ItemClassification.useful}, "volumes": [1], "weight": 88}
    NukeUsagimaru = {"id": 5, "classifications": {1: ItemClassification.useful}, "volumes": [1], "weight": 93}
    Balmung = {"id": 6, "classifications": {1: ItemClassification.useful}, "volumes": [1], "weight": 98}
    Moonstone = {"id": 7, "classifications": {1: ItemClassification.useful}, "volumes": [1], "weight": 95}
    Piros = {"id": 8, "classifications": {1: ItemClassification.progression}, "volumes": [1], "weight": 85}
    Wiseman = {"id": 9, "classifications": {1: ItemClassification.useful}, "volumes": [1], "weight": 96}
    Elk = {"id": 10, "classifications": {1: ItemClassification.progression}, "volumes": [1], "weight": 85}
    Natsume = {"id": 11, "classifications": {1: ItemClassification.useful}, "volumes": [1], "weight": 85}
    Rachel = {"id": 12, "classifications": {1: ItemClassification.useful}, "volumes": [1], "weight": 93}
    Gardenia = {"id": 13, "classifications": {1: ItemClassification.progression}, "volumes": [1], "weight": 92}
    TerajimaRyoko = {"id": 14, "classifications": {1: ItemClassification.useful}, "volumes": [1], "weight": 85}
    BlackRose = {"id": 15, "classifications": {1: ItemClassification.progression}, "volumes": [1], "weight": 85}
    Mistral = {"id": 16, "classifications": {1: ItemClassification.progression}, "volumes": [1], "weight": 85}
    Helba = {"id": 17, "classifications": {1: ItemClassification.useful}, "volumes": [1], "weight": 99}
