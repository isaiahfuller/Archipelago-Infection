from enum import Enum
from typing import TypedDict
from BaseClasses import ItemClassification


class ServerAttributes(TypedDict):
    id: int
    classifications: dict[int, ItemClassification]
    volumes: list[int]
    weight: int


class Servers(Enum):
    _value_: ServerAttributes

    @classmethod
    def from_id(self, id: int):
        for member in self:
            if member.value["id"] == id:
                return member
        return None
    Delta = {"id": 0, "classifications": {1: ItemClassification.progression}, "volumes": [1], "weight": 88 }
    Theta = {"id": 1, "classifications": {1: ItemClassification.progression}, "volumes": [1], "weight": 93 }
    Lambda = {"id": 2, "classifications": {1: ItemClassification.useful}, "volumes": [1], "weight": 96 }
    Sigma = {"id": 3, "classifications": {1: ItemClassification.useful}, "volumes": [1], "weight": 98 }
    Omega = {"id": 4, "classifications": {1: ItemClassification.useful}, "volumes": [1], "weight": 99 }
