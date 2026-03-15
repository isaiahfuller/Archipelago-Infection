from collections.abc import Sequence
from dataclasses import dataclass
from abc import ABC
import random

from BaseClasses import Item, ItemClassification
from .Strings import APConsole, APHelper, Meta, InfectionAreaWordNames as AreaWordNames, InfectionCharacterNames as CharacterNames, InfectionServerNames as ServerNames, InfectionItemNames as ItemNames
from .items.AreaWords import InfectionAreaWords as AreaWords, ExtraAreaWords as ExtraAreaWords, ADDRESS as AreaWordAddress
from .items.PartyMembers import InfectionPartyMembers as PartyMembers, ADDRESS as PartyMemberAddress
from .items.Servers import InfectionServers as Servers, ADDRESS as ServerAddress
from .locations.WordList import InfectionWordListBase, InfectionDeltaWordList, InfectionThetaWordList, get_wordlist_name, ADDRESS as WordListAddress
from .items.FillerItems import Consumables, VirusCores, STORAGE_ADDRESS


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
        self.item_id = self.wordlist.value["address"] * 100 + WordListAddress

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=self.classification
        )


class PartyMemberItem(InfectionItemMeta):
    def __init__(self, party_member, name, id, address, type):
        self.name = name
        self.item_id = id + address
        self.classification = type
        self.party_member = party_member

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=self.classification
        )


class ServerItem(InfectionItemMeta):
    def __init__(self, server, name, id, address, type):
        self.server: Servers = server
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


class ConsumableItem(InfectionItemMeta):
    def __init__(self, name, item, address):
        self.name = name
        self.item_id = item.value["id"] + address
        self.classification = ItemClassification.filler
        self.item = item

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=self.classification
        )


class VirusCoreItem(InfectionItemMeta):
    def __init__(self, name, item, address):
        self.name = name
        self.item_id = item.value["id"] + address
        self.classification = ItemClassification.filler
        self.item = item

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=self.classification
        )


AreaWordItems: list[AreaWordItem] = []
WordListItems: list[InfectionWordListItem] = []
PartyMemberItems: list[PartyMemberItem] = []
ServerItems: list[ServerItem] = []
ConsumableItems: list[ConsumableItem] = []
VirusCoreItems: list[VirusCoreItem] = []

# for word in ExtraAreaWords:
#     AreaWordItems.append(AreaWordItem(
#         name=AreaWordNames[word.name].value,
#         id=word.value["id"],
#         address=AreaWordAddress + word.value["id"],
#         type=word.value["importance"]
#     ))

AreaWordItems.append(AreaWordItem(
    name="Extra Word",
    id=ExtraAreaWords.Stalking.value["id"],
    address=AreaWordAddress + 43768578,
    type=ItemClassification.filler
))

for consumable in Consumables:
    ConsumableItems.append(ConsumableItem(
        name=ItemNames[consumable.name].value,
        item=consumable,
        address=STORAGE_ADDRESS + consumable.value["id"]
    ))
for virus_core in VirusCores:
    VirusCoreItems.append(VirusCoreItem(
        name=ItemNames[virus_core.name].value,
        item=virus_core,
        address=STORAGE_ADDRESS + virus_core.value["id"]
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
        party_member=member,
        name=CharacterNames[member.name].value,
        id=member.value["id"],
        address=PartyMemberAddress + member.value["id"],
        type=member.value["importance"]
    ))

for server in Servers:
    ServerItems.append(ServerItem(
        server=server,
        name=ServerNames[server.name].value,
        id=server.value["id"],
        address=ServerAddress + server.value["id"],
        type=server.value["importance"]
    ))

ITEMS_MASTER: Sequence[Sequence] = [
    *PartyMemberItems,
    *ServerItems,
    *WordListItems,
    *AreaWordItems,
    *ConsumableItems,
    *VirusCoreItems
]

ITEMS_INDEX: Sequence[Sequence] = [
    ITEMS_MASTER,
    PartyMemberItems,
    ServerItems,
    WordListItems,
    AreaWordItems,
    ConsumableItems,
    VirusCoreItems
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
    for i in PartyMemberItems:
        groups.setdefault(APHelper.party_members.value, set()).add("Party Members")
    for i in ServerItems:
        groups.setdefault(APHelper.servers.value, set()).add("Servers")
    for i in WordListItems:
        groups.setdefault(APHelper.word_lists.value, set()).add("Word Lists")
    for i in AreaWordItems:
        groups.setdefault(APHelper.area_words.value, set()).add("Area Words")
    for i in ConsumableItems:
        groups.setdefault(APHelper.consumables.value, set()).add("Consumables")
    for i in VirusCoreItems:
        groups.setdefault(APHelper.virus_cores.value, set()).add("Virus Cores")
    return groups
