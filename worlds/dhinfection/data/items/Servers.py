from enum import Enum
from BaseClasses import Item, ItemClassification

ADDRESS = 0xa41c04


class InfectionServersBase(Enum):
    @classmethod
    def from_id(self, id: int):
        for member in self:
            if member.value["id"] == id:
                return member
        return None


class InfectionServers(InfectionServersBase):
    Delta = {"id": 0, "importance": ItemClassification.progression}
    Theta = {"id": 1, "importance": ItemClassification.progression}
    Lambda = {"id": 2, "importance": ItemClassification.useful}
    Sigma = {"id": 3, "importance": ItemClassification.useful}
    Omega = {"id": 4, "importance": ItemClassification.useful}
