from collections.abc import Sequence
from dataclasses import dataclass
from abc import ABC
import random

from BaseClasses import Item, ItemClassification
from .Strings import APConsole, APHelper,Meta, InfectionAreaWordNames as AreaWordNames, InfectionCharacterNames as CharacterNames
from .items.AreaWords import InfectionAreaWords as AreaWords, ADDRESS as AreaWordAddress
from .items.PartyMembers import InfectionPartyMembers as PartyMembers, ADDRESS as PartyMemberAddress
from .items.Servers import InfectionServers as Servers, ADDRESS as ServerAddress
from .locations.WordList import InfectionWordListBase, InfectionDeltaWordList, InfectionThetaWordList, get_wordlist_name


class InfectionItem(Item):
    game: str = Meta.game


class InfectionItemMeta(ABC):
    name: str
    item_id: int
    address: int

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=ItemClassification.filler
        )


class AreaWordItem(InfectionItemMeta):
    def __init__(self, name, id, address, type):
        self.name = name
        self.item_id = id + address
        self.classification = type

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=self.classification
        )

class InfectionWordListItem(InfectionItemMeta):
    def __init__(self, name, wordlist: InfectionWordListBase):
        self.name = name
        self.classification = wordlist.value["importance"]
        self.wordlist = wordlist
        self.item_id = None

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=None,
            player=player,
            classification=self.classification
        )


class PartyMemberItem(InfectionItemMeta):
    def __init__(self, name, id, address, type):
        self.name = name
        self.item_id = id + address
        self.classification = type

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=self.classification
        )


class ServerItem(InfectionItemMeta):
    def __init__(self, name, id, address, type):
        self.name = name
        self.item_id = id + address
        self.classification = type

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=self.classification
        )


# class CollectableItem(InfectionItemMeta):
#     resource: str
#     amount: int | float
#     capacity: int
#     weight: int

#     def __init__(self, name: str, resource: str, amount: int | float, weight: int, id_offset: int = 0):
#         self.name = name
#         self.address = NTSCU.GameStates[resource]
#         self.item_id = self.address + id_offset
#         self.resource = resource

#         self.amount = amount
#         self.capacity = Capacities[resource]
#         self.weight = weight


# Nothing = CollectableItem("Nothing", "Nothing", 0, 1)

AreaWordItems: list[AreaWordItem] = []
WordListItems: list[InfectionWordListItem] = []
PartyMemberItems: list[PartyMemberItem] = []
ServerItems: list[ServerItem] = []

for word in AreaWords:
    AreaWordItems.append(AreaWordItem(
        name=AreaWordNames[word.name].value,
        id=word.value["id"],
        address=AreaWordAddress + word.value["id"],
        type=word.value["importance"]
    ))


for wordlist in InfectionDeltaWordList:
    WordListItems.append(InfectionWordListItem(
        name=get_wordlist_name(wordlist),
        wordlist=wordlist
    ))

for wordlist in InfectionThetaWordList:
    WordListItems.append(InfectionWordListItem(
        name=get_wordlist_name(wordlist),
        wordlist=wordlist
    ))

for member in PartyMembers:
    PartyMemberItems.append(PartyMemberItem(
        name=CharacterNames[member.name].value,
        id=member.value["id"],
        address=PartyMemberAddress + member.value["id"],
        type=member.value["importance"]
    ))

for server in Servers:
    ServerItems.append(ServerItem(
        name=server.name,
        id=server.value["id"],
        address=ServerAddress + server.value["id"],
        type=server.value["importance"]
    ))

ITEMS_MASTER: Sequence[Sequence] = [
    *AreaWordItems, *PartyMemberItems, *ServerItems
]

ITEMS_INDEX: Sequence[Sequence] = [
    ITEMS_MASTER, AreaWordItems, PartyMemberItems, ServerItems
]


def from_id(item_id=int, category: int = 0):
    ref: Sequence = ITEMS_INDEX[category]

    i: InfectionItemMeta = next((i for i in ref if i.item_id == item_id), None)
    return i


def generate_name_to_id() -> dict[str: int]:
    i: InfectionItemMeta
    return {i.name: i.item_id for i in ITEMS_MASTER}


def generate_item_groups() -> dict[str: list[int]]:
    groups: dict[str: set[str]] = {}
    i: InfectionItemMeta
    for i in AreaWordItems:
        groups.setdefault(APHelper.area_words.value, set()).add("Area Words")
    for i in PartyMemberItems:
        groups.setdefault(APHelper.party_members.value, set()).add("Party Members")
    for i in ServerItems:
        groups.setdefault(APHelper.servers.value, set()).add("Servers")
    return groups
