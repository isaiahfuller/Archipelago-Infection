
import math
from enum import IntEnum
from logging import Logger
from typing import Optional, List, Set

from NetUtils import NetworkItem
from worlds.dothack import PlayStatNames
from worlds.dothack.data.locations.Events import CompletionConditions
from worlds.dothack.data.locations.PlayStats import PlayStats
from .data import Items
from .data.Addresses import VolumeAddresses, InfectionAddresses, MutationAddresses, OutbreakAddresses, \
    QuarantineAddresses
from .data.GameState import InfectionGameState as GameState
from .data.Items import InfectionWordListItem as WordListItem, PartyMemberItem, ServerItem, ConsumableItem, \
    VirusCoreItem, RyuBookItem, GruntyFoodItem, InfectionLevelItem, WeaponItem
from .data.Items import PartyMemberItems
from .data.Items import ServerItems
from .data.Items import WordListItems, RyuBookItems
from .data.Strings import APConsole, Meta, GameStateNames, EventNames
from .data.items.AreaWords import AreaWords
from .data.items.PartyMembers import PartyMembers
from .data.items.RyuBooks import RyuBooks
from .data.items.Servers import Servers
from .data.locations.Events import InfectionStoryEvents as StoryEvents, InfectionGoldenGoblins as GoldenGoblins, \
    InfectionOptionalPartyMembers as OptionalPartyMembers
from .data.locations.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList, \
    WordListBase, get_wordlist_name
from .pcsx2_interface.pine import Pine

# Notes:
# latest item idx can seemingly be written to 0xA44EC8 safely.
# game doesn't seem to use it for anything.


class ConnectionStatus(IntEnum):
    WRONG_GAME = -1
    DISCONNECTED = 0
    CONNECTED = 1
    IN_GAME = 2


class DotHackInterface:
    pine: Pine = Pine()
    status: ConnectionStatus = ConnectionStatus.DISCONNECTED
    logger: Logger
    loaded_game: Optional[str] = None
    volume: int
    addresses: type[VolumeAddresses]

    def __init__(self, logger: Logger, volume: int):
        self.logger = logger
        self.volume = volume
        match volume:
            case 1: self.addresses = InfectionAddresses
            case 2: self.addresses = MutationAddresses
            case 3: self.addresses = OutbreakAddresses
            case 4: self.addresses = QuarantineAddresses

    def connect_game(self) -> None:
        if not self.pine.is_connected():
            self.pine.connect()
            if not self.pine.is_connected():
                self.status = ConnectionStatus.DISCONNECTED
                return
            self.logger.info(APConsole.Info.init.value)
        try:
            if self.status is ConnectionStatus.CONNECTED.value:
                self.logger.info(APConsole.Info.p_init_g.value)
            game_id: str = self.pine.get_game_id()
            self.loaded_game = None
            if game_id in Meta.supported_versions.value:
                self.loaded_game = game_id
                self.status = ConnectionStatus.IN_GAME
            elif not self.status is ConnectionStatus.WRONG_GAME.value:
                self.logger.warning(APConsole.Err.game_wrong.value)
                self.status = ConnectionStatus.WRONG_GAME
        except RuntimeError:
            return
        except ConnectionError:
            return

        if self.status is ConnectionStatus.DISCONNECTED.value:
            self.status = ConnectionStatus.CONNECTED

    def disconnect_game(self) -> None:
        self.pine.disconnect()
        self.loaded_game = None
        self.status = ConnectionStatus.DISCONNECTED

    def get_connection_state(self) -> bool:
        try:
            connected: bool = self.pine.is_connected()
            return not (not connected or self.loaded_game is None)
        except RuntimeError:
            return False

    def get_ingame_status(self) -> GameStateNames | None:
        try:
            st_val = self.pine.read_int8(self.addresses.IngameStatus)
            overlay_val = self.pine.read_int8(self.addresses.IngameOverlay)
            if overlay_val == 0:
                return None
            status = GameStateNames[str(GameState(st_val).name)]
            if status in [GameStateNames.LoggedIn, GameStateNames.Login, GameStateNames.Desktop]:
                return status
            else:
                return None
        except KeyError:
            return None
        except RuntimeError:
            return None
        except ConnectionError:
            return None

    def get_last_item_index(self) -> int:
        return self.pine.read_int32(self.addresses.LastItemIdx)

    def set_last_item_index(self, index: int) -> None:
        self.pine.write_int32(self.addresses.LastItemIdx, index)

    def infection_initial_state(self, ctx) -> None:
        self.pine.write_int8(0xa44ed7, self.pine.read_int8(0xa44ed7) |
                             0b00000111)  # Not needed when setting emails read

        # Unlock Data Drain
        self.pine.write_int8(0xA46141, 1)  # Unlock Data Drain skill category
        self.pine.write_int8(0xA41894, 2)  # Unlock Data Drain, use red dye

        # Ryu Books have been changed to items
        # # Give Ryu Books
        # self.pine.write_int8(0xA407DD, 1)
        # self.pine.write_int8(0xA407DE, 1)
        # self.pine.write_int8(0xA407DF, 1)
        # self.pine.write_int8(0xA407E0, 1)
        # self.pine.write_int8(0xA407E1, 1)
        # self.pine.write_int8(0xA407E2, 1)
        # self.pine.write_int8(0xA407E3, 1)
        # self.pine.write_int8(0xA407E4, 1)

        # Add starting lists
        self.pine.write_int8(0xA44CC6, 0x0e)
        self.pine.write_int8(0xA44CC4, 0x0f)

        # Skip meeting Orca
        # self.pine.write_int8(0xa44ed7, self.pine.read_int8(0xa44ed7) | 0b11000000)
        self.pine.write_int8(0xa44ed8, self.pine.read_int8(0xa44ed8) | 0b00000111)
        self.pine.write_int8(0xa44edf, self.pine.read_int8(0xa44edf) | 0b11000000)
        self.pine.write_int8(0xa44ee0, self.pine.read_int8(0xa44ee0) | 0b00100101)
        self.pine.write_int8(0xa44ee7, self.pine.read_int8(0xa44ee7) | 0b01000000)
        self.pine.write_int8(0xa44ee8, self.pine.read_int8(0xa44ee8) | 0b11110100)
        self.pine.write_int8(0xa44ee9, self.pine.read_int8(0xa44ee9) | 0b00000011)
        self.pine.write_int8(0xa44eef, self.pine.read_int8(0xa44eef) | 0b10000000)

        # Skip BlackRose cutscene and Hidden Forbidden Holy Ground
        self.pine.write_int8(0xa44f20, self.pine.read_int8(0xa44f20) | 0xff)  # 0b11010101, b5 blocks gate w/o cutscene
        self.pine.write_int8(0xa44f22, self.pine.read_int8(0xa44f22) | 0xff)
        self.pine.write_int8(0xa44f23, self.pine.read_int8(0xa44f23) | 0b00000001)
        self.pine.write_int8(0xa44f27, self.pine.read_int8(0xa44f27) | 0b10000000)

        # Give Virus Core M
        self.pine.write_int8(0xa406d8, max(self.pine.read_int8(0xa406d8), 1))

        # Get Mia and Elk out of your way
        self.pine.write_int8(0xa44f58, self.pine.read_int8(0xa44f58) | 0xff)

        # Kite's Class from Options
        if ctx.kite_class == 0:
            self.pine.write_int8(0xA46F30, 0)
        if ctx.kite_class == 1:
            self.pine.write_int8(0xA46F30, 1)
        if ctx.kite_class == 2:
            self.pine.write_int8(0xA46F30, 2)
        if ctx.kite_class == 3:
            self.pine.write_int8(0xA46F30, 3)
        if ctx.kite_class == 4:
            self.pine.write_int8(0xA46F30, 4)
        if ctx.kite_class == 5:
            self.pine.write_int8(0xA46F30, 5)

    async def check_locations(self, ctx) -> None:
        checked: Set[int] = set()

        def get_location_id(name: str) -> int | None:
            loc_id = ctx.locations_name_to_id.get(name)
            if loc_id is None or loc_id in checked or loc_id in ctx.checked_locations:
                return None
            return loc_id

        def addr_check(addr: int, bitflags: int, loc_id: int) -> None:
            try:
                val: int = self.pine.read_int8(addr)
                if val & bitflags == bitflags:
                    checked.add(loc_id)
            except RuntimeError:
                return
            except ConnectionError:
                return

        def stat_check(stat: PlayStats):
            addr = self.addresses.PlayStats[stat.name]
            try:
                book = RyuBooks.get_by_stat(stat)
                if book and book not in ctx.obtained_ryu_books:
                    self.pine.write_int16(addr, 0)
                    return

                val: int = self.pine.read_int16(addr)
                name: str = PlayStatNames[stat.name].value
                if stat.value["scale"] == "list":
                    for i in stat.value["values"]:
                        if val < i:
                            break
                        loc_id = get_location_id(f"{name}{i}")
                        if loc_id is None:
                            continue
                        checked.add(loc_id)
                elif stat.value["scale"] == "range":
                    for i in range(stat.value["values"][0], stat.value["values"][1]):
                        if val < i:
                            break
                        loc_id = get_location_id(f"{name}{i}")
                        if loc_id is None:
                            continue
                        checked.add(loc_id)
            except RuntimeError:
                return
            except ConnectionError:
                return

        # Story Events
        for event in StoryEvents:
            name: str = EventNames[event.name].value
            addr: int = event.value["address"]
            bitflags: int = event.value["bits"]
            loc_id = get_location_id(name)
            if loc_id is None:
                continue
            addr_check(addr, bitflags, loc_id)

        # Golden Goblins
        for goblin in GoldenGoblins:
            name: str = EventNames[goblin.name].value
            addr: int = self.addresses.Events[goblin.name]
            bitflags: int = goblin.value["bits"]
            loc_id = get_location_id(name)
            if loc_id is None:
                continue
            addr_check(addr, bitflags, loc_id)

        # Optional Party Members
        for member in OptionalPartyMembers:
            name: str = EventNames[member.name].value
            addr: int = self.addresses.Events[member.name]
            bitflags: int = member.value["bits"]
            loc_id = get_location_id(name)
            if loc_id is None:
                continue
            addr_check(addr, bitflags, loc_id)

        # Ryu Book stats
        for stat in PlayStats:
            stat_check(stat)

        # Completion Conditions
        for condition in CompletionConditions:
            name: str = EventNames[condition.name].value
            addr: int = condition.value["address"]
            bitflags: int = condition.value["bits"]
            try:
                val: int = self.pine.read_int8(addr)
                if val & bitflags == bitflags:
                    loc_id = get_location_id(name)
                    if loc_id is not None:
                        checked.add(loc_id)

                    target_condition = CompletionConditions.SkeithDefeated if ctx.completion_condition == 0 \
                        else CompletionConditions.ParasiteDragonDefeated
                    if condition == target_condition:
                        await ctx.goal()
            except (RuntimeError, ConnectionError):
                continue

        if checked:
            ctx.checked_locations.update(checked)
            if ctx.server:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": checked}])
            else:
                ctx.offline_locations_checked.update(checked)

    async def receive_items(self, ctx) -> None:
        if ctx.next_item_slot < 0:
            last_in_mem = self.get_last_item_index()
            if last_in_mem < 0:
                last_in_mem = 0
            ctx.next_item_slot = last_in_mem
            ctx.last_item_processed_index = last_in_mem

        items_count = len(ctx.items_received)
        if ctx.next_item_slot >= items_count:
            return

        received: List[NetworkItem] = ctx.items_received[ctx.next_item_slot:]
        self.logger.debug(f"Processing {len(received)} items from Archipelago...")

        for server_item in received:
            item = Items.from_id(server_item.item)
            if item:
                self.logger.debug(f"Applying item [{ctx.next_item_slot}]: {item.name}")
                if isinstance(item, ConsumableItem):
                    """Add item to storage"""
                    self.add_consumable(item)
                elif isinstance(item, WeaponItem):
                    """Add weapon to storage"""
                    self.add_weapon(item)
                elif isinstance(item, VirusCoreItem):
                    """Add item to inventory"""
                    self.add_key(self.addresses.Items[item.virus_core.name])
                elif isinstance(item, GruntyFoodItem):
                    """Add item to inventory"""
                    self.add_key(self.addresses.Items[item.grunty_food.name])
                elif isinstance(item, InfectionLevelItem):
                    """Reduce Infection Rate to 0%"""
                    self.add_reset_rate(self.addresses.Items[item.infection_level.name])
                elif isinstance(item, WordListItem):
                    """Add to list of word lists to unlock"""
                    ctx.unlocked_word_lists.add(item.wordlist.value["address"])
                elif isinstance(item, PartyMemberItem):
                    """Add to list of allowed party members"""
                    ctx.unlocked_party_members.add(item.party_member)
                elif isinstance(item, ServerItem):
                    """Add to list of allowed servers"""
                    ctx.unlocked_servers.add(item.server)
                elif isinstance(item, RyuBookItem):
                    """Add to list of Ryu Books"""
                    ctx.obtained_ryu_books.add(item.ryu_book)
                    self.add_key(self.addresses.Items[item.ryu_book.name])
            else:
                self.logger.warning(f"Unknown item ID {server_item.item} received at slot {ctx.next_item_slot}")

            ctx.next_item_slot += 1
            ctx.last_item_processed_index = ctx.next_item_slot
            self.set_last_item_index(ctx.next_item_slot)

    async def resync_items(self, ctx) -> None:
        """
        Syncs items that were received before the client was fully initialized.
        Issue: Virus Cores and Consumables are currently only given once.
        """
        # if ctx.last_item_processed_index < 0:
        #     return
        self.logger.debug(f"items_received: {[item[0] for item in ctx.items_received]}")
        received_id = [item[0] for item in ctx.items_received]
        self.logger.debug(f"received_id: {received_id}")
        for member in PartyMemberItems:
            if member.item_id in received_id:
                ctx.unlocked_party_members.add(member.party_member)
        for server in ServerItems:
            if server.item_id in received_id:
                ctx.unlocked_servers.add(server.server)
        for wordlist in WordListItems:
            if wordlist.item_id in received_id:
                ctx.unlocked_word_lists.add(wordlist.wordlist.value["address"])
        for ryu_book in RyuBookItems:
            if ryu_book.item_id in received_id:
                ctx.obtained_ryu_books.add(ryu_book.ryu_book)
                # self.add_key(self.addresses.Items[ryu_book.name])
        # for item in ConsumableItems:
        #     if item.item_id in received_id:
        #         self.add_consumable(item)
        # for item in VirusCoreItems:
        #     if item.item_id in received_id:
        #         self.add_key(item.item.value["id"])
        self.set_last_item_index(len(ctx.items_received))

    def add_consumable(self, item_obj: ConsumableItem) -> None:
        addr: int = self.addresses.Storage
        item: int = item_obj.consumable.value["id"]
        for i in range(addr, addr + 396, 4):
            curr: int = self.pine.read_int32(i)
            amt: int = self.pine.read_int8(i+3)
            if curr | 0xff000000 == item | 0xff000000:
                self.pine.write_int8(i+3, amt + 1)
                return
            if curr == 0x00ffffff:
                self.pine.write_int32(i, item)
                self.pine.write_int8(i+3, 1)
                break

    def add_weapon(self, item_obj: WeaponItem) -> None:
        addr: int = self.addresses.Storage
        item: int = item_obj.weapon.value["id"]
        for i in range(addr, addr + 396, 4):
            curr: int = self.pine.read_int32(i)
            amt: int = self.pine.read_int8(i+3)
            if curr | 0xff000000 == item | 0xff000000:
                self.pine.write_int8(i+3, amt + 1)
                return
            if curr == 0x00ffffff:
                self.pine.write_int32(i, item)
                self.pine.write_int8(i+3, 1)
                break

    def add_key(self, addr) -> None:
        curr_amt = self.pine.read_int8(addr)
        self.pine.write_int8(addr, curr_amt + 1)

    def add_reset_rate(self, addr) -> None:
        amt = self.pine.read_int8(addr)
        self.pine.write_int8(0xA4613E, amt - 100)


    async def scan_server(self, ctx) -> None:
        addr: int = self.addresses.Servers
        unlocked_servers: int = self.pine.read_int8(addr)
        val = unlocked_servers
        for server in Servers:
            if server not in ctx.unlocked_servers:
                val &= ~(2 ** server.value["id"])
            else:
                val |= 2 ** server.value["id"]
        self.pine.write_int8(addr, val)

    async def scan_party_member(self, ctx) -> None:
        """
        Scans the party member list and locks/unlocks based on whether the party member is in ctx.unlocked_party_members
        """
        addr: int = self.addresses.Party
        try:
            val = self.pine.read_int32(addr)
            new_val = val
            for member in PartyMembers:
                m_id = member.value["id"]
                if member in ctx.unlocked_party_members:
                    new_val |= (1 << m_id)
                else:
                    new_val &= ~(1 << (m_id % 32))

            self.pine.write_int32(addr, new_val)
            self.pine.write_int32(addr + 4, new_val)
        except (RuntimeError, ConnectionError):
            return

    async def scan_word_list(self, ctx) -> None:
        """
        Scans the word list and locks/unlocks based on whether the word list is in ctx.unlocked_word_lists
        TODO:
        - Lock/unlock the individual words
          - Needs an additional data structure to keep track of the status of each word
        - Manually add/remove lists
          - The structure of the addresses makes this difficult. This would likely require rewriting
            the word list structure each time the game adds one.
        """
        starting_addr: int = 0xa44c47
        size: int = 256
        try:
            data = bytearray(self.pine.read_bytes(starting_addr, size))
            for i in range(255, 0, -1):
                current_addr = data[i]
                if current_addr == 0x00 or current_addr == 0xff:
                    continue

                delta_member: DeltaWordList | None = DeltaWordList.from_address(current_addr)
                theta_member: ThetaWordList | None = ThetaWordList.from_address(current_addr)
                current_list_val: int | None = None
                current_list_obj: WordListBase | None = None

                if delta_member:
                    current_list_val = delta_member.value["address"]
                    current_list_obj = delta_member
                elif theta_member:
                    current_list_val = theta_member.value["address"]
                    current_list_obj = theta_member

                if current_list_val:
                    if current_list_val not in ctx.obtained_word_lists:
                        ctx.obtained_word_lists.add(current_list_val)
                        if ctx.server:
                            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [ctx.locations_name_to_id[get_wordlist_name(current_list_obj)]]}])

                    status_byte_idx = i + 1
                    if status_byte_idx < size:
                        old_status = data[status_byte_idx]
                        new_status = 0x00 if current_list_val in ctx.unlocked_word_lists else 0xff
                        if old_status != new_status:
                            data[status_byte_idx] = new_status
                            self.pine.write_int8(starting_addr + status_byte_idx, new_status)
        except (RuntimeError, ConnectionError):
            return

    def modify_word(self, word_obj: AreaWords, lock: bool = False) -> None:
        """
        Locks/unlocks a word. 
        Based on feedback from party member/server, this might not work correctly.
        """
        word: int = word_obj.value["idx"]
        offset: int = math.floor(word / 8)
        unlocked_words: int = self.pine.read_int8(offset + 0xa44c0c)
        if lock:
            self.pine.write_int8(offset + 0xa44c0c, unlocked_words & ~(2 ** (word % 8)))
        else:
            self.pine.write_int8(offset + 0xa44c0c, unlocked_words | 2 ** (word % 8))

    def email_state(self, offset: int, value: int | None = None) -> int | None:
        BASE_ADDR: int = 0xa41c34
        # print(f"Email state: {hex(BASE_ADDR + offset)}: {bin(pine.read_int8(BASE_ADDR + offset))}")
        try:
            if value is None:
                return self.pine.read_int8(BASE_ADDR + offset)
            self.pine.write_int8(BASE_ADDR + offset, value)
        except (RuntimeError, ConnectionError):
            return None

    async def scan_emails(self) -> None:
        """Reads all received emails"""
        for i in range(0, 0x140):
            curr = self.email_state(i)
            if curr == 2:
                self.email_state(i, 4)

    async def scan_ryu_books(self, ctx) -> None:
        """
        Scans the Ryu Book list and locks/unlocks based on whether the Ryu Book is in ctx.obtained_ryu_books
        """
        try:
            for ryu_book in RyuBooks:
                if ryu_book in ctx.obtained_ryu_books:
                    self.pine.write_int8(self.addresses.Items[ryu_book.name], 1)
                else:
                    self.pine.write_int8(self.addresses.Items[ryu_book.name], 0)
        except (RuntimeError, ConnectionError):
            return None

    async def scan_kite_class(self, ctx) -> None:
        try:
            current_class: int = self.pine.read_int8(self.addresses.KiteClass)
            if current_class != ctx.kite_class:
                self.pine.write_int8(self.addresses.KiteClass, ctx.kite_class)
        except (RuntimeError, ConnectionError):
            return None
