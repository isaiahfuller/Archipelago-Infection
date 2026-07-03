from collections.abc import Sequence
from abc import ABC

from BaseClasses import Item, ItemClassification
from .Strings import APHelper, Meta, CharacterNames, ServerNames, ItemNames
from .items.PartyMembers import PartyMembers
from .items.Servers import Servers
from .items.Weapons import Weapons
from .locations.WordList import WordListBase, InfectionDeltaWordList, InfectionThetaWordList, get_wordlist_name
from .items.FillerItems import Consumables, VirusCores, GruntyFood, InfectionLevel
from .items.RyuBooks import RyuBooks
from .DataManager import VOLUME_DATA

# Using Infection for IDs
from .Addresses import InfectionAddresses as Addresses


class InfectionItem(Item):
    game: str = str(Meta.game.value)


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

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=ItemClassification.filler
        )

class InfectionWordListItem(InfectionItemMeta):
    def __init__(self, name, wordlist: WordListBase, volume: int):
        self.name = name
        self.classification = wordlist.value["classifications"].get(volume, ItemClassification.filler)
        self.wordlist = wordlist
        self.item_id = self.wordlist.value["address"] * 125 + Addresses.WordLists

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=self.classification
        )


class PartyMemberItem(InfectionItemMeta):
    def __init__(self, party_member, name, id, address, volume: int):
        self.name = name
        self.item_id = (address * 268) + (id * 10)
        self.classification = party_member.value["classifications"].get(volume, ItemClassification.filler)
        self.party_member = party_member

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=self.classification
        )


class ServerItem(InfectionItemMeta):
    def __init__(self, server, name, id, address, volume: int):
        self.server: Servers = server
        self.name = name
        self.item_id = (address * 723) + (id * 10)
        self.classification = server.value["classifications"].get(volume, ItemClassification.filler)

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=self.classification
        )


class ConsumableItem(InfectionItemMeta):
    consumable: Consumables

    def __init__(self, name, item, address):
        self.name = name
        self.item_id = (address * 38) + item.value["id"]
        self.classification = ItemClassification.filler
        self.consumable = item

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=self.classification
        )

class WeaponItem(InfectionItemMeta):
    weapon: Weapons

    def __init__(self, name, item, address):
        self.name = name
        self.item_id = (address * 328) + item.value["id"]
        self.classification = ItemClassification.useful
        self.weapon = item

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=self.classification
        )

class VirusCoreItem(InfectionItemMeta):
    virus_core: VirusCores

    def __init__(self, name, item, address):
        self.name = name
        self.item_id = (address * 94) + item.value["id"]
        self.classification = ItemClassification.filler
        self.virus_core = item

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=self.classification
        )

class GruntyFoodItem(InfectionItemMeta):
    grunty_food: GruntyFood

    def __init__(self, name, item, address):
        self.name = name
        self.item_id = (address * 16) + item.value["id"]
        self.classification = ItemClassification.filler
        self.grunty_food = item

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=self.classification
        )
class RyuBookItem(InfectionItemMeta):
    ryu_book: RyuBooks

    def __init__(self, name, item, address):
        self.name = name
        self.item_id = (address * 42)
        self.classification = ItemClassification.progression
        self.ryu_book = item

    def to_item(self, player: int) -> InfectionItem:
        return InfectionItem(
            name=self.name,
            code=self.item_id,
            player=player,
            classification=self.classification
        )

class InfectionLevelItem(InfectionItemMeta):
        infection_level: InfectionLevel

        def __init__(self, name, item, address):
            self.name = name
            self.item_id = (address * 16)
            self.classification = ItemClassification.filler
            self.infection_level = item

        def to_item(self, player: int) -> InfectionItem:
            return InfectionItem(
                name=self.name,
                code=self.item_id,
                player=player,
                classification=self.classification

            )
ConsumableItems: list[ConsumableItem] = []
WeaponItems: list[WeaponItem] = []
VirusCoreItems: list[VirusCoreItem] = []
RyuBookItems: list[RyuBookItem] = []
GruntyFoodItems: list[GruntyFoodItem] = []
InfectionLevelItems: list[InfectionLevelItem] = []

for consumable in Consumables:
    ConsumableItems.append(ConsumableItem(
        name=ItemNames[consumable.name].value,
        item=consumable,
        address=Addresses.Storage + consumable.value["id"]
    ))
for weapon in Weapons:
    WeaponItems.append(WeaponItem(
        name=ItemNames[weapon.name].value,
        item=weapon,
        address=Addresses.Storage + weapon.value["id"]
    ))

for virus_core in VirusCores:
    VirusCoreItems.append(VirusCoreItem(
        name=ItemNames[virus_core.name].value,
        item=virus_core,
        address=Addresses.Storage + virus_core.value["id"]
    ))
for grunty_food in GruntyFood:
    GruntyFoodItems.append(GruntyFoodItem(
        name=ItemNames[grunty_food.name].value,
        item=grunty_food,
        address=Addresses.Storage + grunty_food.value["id"]
    ))
for ryu_book in RyuBooks:
    RyuBookItems.append(RyuBookItem(
        name=ItemNames[ryu_book.name].value,
        item=ryu_book,
        address=Addresses.Items[ryu_book.name]
    ))
for infection_level in InfectionLevel:
    InfectionLevelItems.append(InfectionLevelItem(
        name=ItemNames[infection_level.name].value,
        item=infection_level,
        address=Addresses.Items[infection_level.name]
    ))
def generate_volume_items(volume: int):
    v_data = VOLUME_DATA[volume]
    v_data.wordlist_items = []
    v_data.party_member_items = []
    v_data.server_items = []

    for wordlist in InfectionDeltaWordList:
        volumes = wordlist.value.get("volumes", [])
        if isinstance(volumes, list) and volume in volumes:
            v_data.wordlist_items.append(InfectionWordListItem(
                name=get_wordlist_name(wordlist),
                wordlist=wordlist,
                volume=volume
            ))

    for wordlist in InfectionThetaWordList:
        volumes = wordlist.value.get("volumes", [])
        if isinstance(volumes, list) and volume in volumes:
            v_data.wordlist_items.append(InfectionWordListItem(
                name=get_wordlist_name(wordlist),
                wordlist=wordlist,
                volume=volume
            ))

    for member in PartyMembers:
        volumes = member.value.get("volumes", [])
        if isinstance(volumes, list) and volume in volumes:
            v_data.party_member_items.append(PartyMemberItem(
                party_member=member,
                name=CharacterNames[member.name].value,
                id=member.value["id"],
                address=Addresses.Party + member.value["id"],
                volume=volume
            ))

    for server in Servers:
        volumes = server.value.get("volumes", [])
        if isinstance(volumes, list) and volume in volumes:
            v_data.server_items.append(ServerItem(
                server=server,
                name=ServerNames[server.name].value,
                id=server.value["id"],
                address=Addresses.Servers + server.value["id"],
                volume=volume
            ))

    v_data.items = [
        *v_data.party_member_items,
        *v_data.server_items,
        *v_data.wordlist_items,
        *ConsumableItems,
        *WeaponItems,
        *VirusCoreItems,
        *GruntyFoodItems,
        *RyuBookItems,
        *InfectionLevelItems
    ]


for v in VOLUME_DATA:
    generate_volume_items(v)

WordListItems: list[InfectionWordListItem] = []
for v_data in VOLUME_DATA.values():
    for item in v_data.wordlist_items:
        if item not in WordListItems:
            WordListItems.append(item)

PartyMemberItems: list[PartyMemberItem] = []
for v_data in VOLUME_DATA.values():
    for item in v_data.party_member_items:
        if item not in PartyMemberItems:
            PartyMemberItems.append(item)

ServerItems: list[ServerItem] = []
for v_data in VOLUME_DATA.values():
    for item in v_data.server_items:
        if item not in ServerItems:
            ServerItems.append(item)

ItemUnion = ConsumableItem | WeaponItem | InfectionWordListItem | PartyMemberItem | RyuBookItem | ServerItem | VirusCoreItem

ITEMS_MASTER: list[ItemUnion] = [
    *PartyMemberItems,
    *ServerItems,
    *WordListItems,
    *ConsumableItems,
    *WeaponItems,
    *VirusCoreItems,
    *GruntyFoodItems,
    *RyuBookItems,
    *InfectionLevelItems
]

ITEMS_INDEX: list[Sequence[ItemUnion]] = [
    ITEMS_MASTER,
    PartyMemberItems,
    ServerItems,
    WordListItems,
    ConsumableItems,
    WeaponItems,
    VirusCoreItems,
    GruntyFoodItems,
    RyuBookItems,
    InfectionLevelItems
]


def from_id(item_id=int, category: int = 0):
    ref: Sequence = ITEMS_INDEX[category]

    i: InfectionItemMeta | None = next((i for i in ref if i.item_id == item_id), None)
    return i


def generate_name_to_id() -> dict[str, int]:
    i: InfectionItemMeta
    return {i.name: i.item_id for i in ITEMS_MASTER}


def generate_item_groups() -> dict[str, set[str]]:
    groups: dict[str, set[str]] = {}
    i: InfectionItemMeta
    for i in PartyMemberItems:
        groups.setdefault(APHelper.party_members.value, set()).add(i.name)
    for i in ServerItems:
        groups.setdefault(APHelper.servers.value, set()).add(i.name)
    for i in WordListItems:
        groups.setdefault(APHelper.word_lists.value, set()).add(i.name)
    for i in ConsumableItems:
        groups.setdefault(APHelper.consumables.value, set()).add(i.name)
    for i in WeaponItems:
        groups.setdefault(APHelper.weapons.value, set()).add(i.name)
    for i in VirusCoreItems:
        groups.setdefault(APHelper.virus_cores.value, set()).add(i.name)
    for i in RyuBookItems:
        groups.setdefault(APHelper.ryu_books.value, set()).add(i.name)
    return groups
