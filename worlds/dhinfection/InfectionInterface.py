
from worlds.dhinfection.data.locations.Events import CompletionConditions
from worlds.dhinfection.data.locations.PlayStats import PlayStats
from worlds.dhinfection import PlayStatNames
import math
import asyncio
from enum import IntEnum
from logging import Logger
from typing import Optional, List, Set

from NetUtils import NetworkItem
from .pcsx2_interface.pine import Pine
from . import InfectionItem
from .data.Strings import APConsole, Meta, InfectionGameStateNames as GameStateNames, InfectionAreaWordNames as AreaWordNames, InfectionEventNames as EventNames
from .data.GameState import InfectionGameState as GameState
from .data.locations.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList, InfectionWordListBase as WordListBase, get_wordlist_name
from .data.locations.Events import InfectionStoryEvents as StoryEvents, InfectionGoldenGoblins as GoldenGoblins, InfectionOtherSideQuests as SideQuests, InfectionOptionalPartyMembers as OptionalPartyMembers

from .data.items.AreaWords import InfectionAreaWords as AreaWords
from .data.items.Servers import InfectionServers as Servers
from .data.items.PartyMembers import InfectionPartyMembers as PartyMembers
from .data.items.FillerItems import Consumables, VirusCores

from .data import Items
from .data.Items import InfectionWordListItem as WordListItem, AreaWordItem, PartyMemberItem, ServerItem, ConsumableItem, VirusCoreItem
from .data.Items import WordListItems, ConsumableItems, VirusCoreItems
from .data.Items import ServerItems
from .data.Items import PartyMemberItems
# Notes:
# latest item idx can seemingly be written to 0xA44EC8 safely.
# game doesn't seem to use it for anything.


class ConnectionStatus(IntEnum):
    WRONG_GAME = -1
    DISCONNECTED = 0
    CONNECTED = 1
    IN_GAME = 2


class InfectionInterface:
    pine: Pine = Pine()
    status: ConnectionStatus = ConnectionStatus.DISCONNECTED.value
    logger: Logger
    loaded_game: Optional[str] = None

    def __init__(self, logger: Logger):
        self.logger = logger

    def connect_game(self) -> None:
        if not self.pine.is_connected():
            self.pine.connect()
            if not self.pine.is_connected():
                self.status = ConnectionStatus.DISCONNECTED.value
                return
            self.logger.info(APConsole.Info.init.value)
        try:
            if self.status is ConnectionStatus.CONNECTED.value:
                self.logger.info(APConsole.Info.p_init_g.value)
            game_id: str = self.pine.get_game_id()
            self.loaded_game = None
            if game_id in Meta.supported_versions.value:
                self.loaded_game = game_id
                self.status = ConnectionStatus.IN_GAME.value
            elif not self.status is ConnectionStatus.WRONG_GAME.value:
                self.logger.warning(APConsole.Err.game_wrong.value)
                self.status = ConnectionStatus.WRONG_GAME.value
        except RuntimeError:
            return
        except ConnectionError:
            return

        if self.status is ConnectionStatus.DISCONNECTED.value:
            self.status = ConnectionStatus.CONNECTED.value

    def disconnect_game(self) -> None:
        self.pine.disconnect()
        self.loaded_game = None
        self.status = ConnectionStatus.DISCONNECTED.value

    def get_connection_state(self) -> bool:
        try:
            connected: bool = self.pine.is_connected()
            return not (not connected or self.loaded_game is None)
        except RuntimeError:
            return False

    def get_ingame_status(self) -> GameStateNames | None:
        address = 0xa3f5f0
        overlay_address = 0x00400804
        try:
            st_val = self.pine.read_int8(address)
            overlay_val = self.pine.read_int8(overlay_address)
            if overlay_val == 0:
                return None
            status = GameStateNames[GameState(st_val).name]
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
        return self.pine.read_int32(0xa44ec8)

    def set_last_item_index(self, index: int) -> None:
        self.pine.write_int32(0xa44ec8, index)

    def initial_state(self) -> None:
        # # Read emails before meeting Orca
        # email_state(0x04, 4) # Registered yet?
        # email_state(0x05, 4) # Thank You
        # email_state(0x140, 4) # Version update
        self.pine.write_int8(0xa44ed7, self.pine.read_int8(0xa44ed7) |
                             0b00000111)  # Not needed when setting emails read

        # Unlock Data Drain
        self.pine.write_int8(0xA46141, 1)  # Unlock Data Drain skill category
        self.pine.write_int8(0xA41894, 2)  # Unlock Data Drain, use red dye

        # Give Ryu Books
        self.pine.write_int8(0xA407DD, 1)
        self.pine.write_int8(0xA407DE, 1)
        self.pine.write_int8(0xA407DF, 1)
        self.pine.write_int8(0xA407E0, 1)
        self.pine.write_int8(0xA407E1, 1)
        self.pine.write_int8(0xA407E2, 1)
        self.pine.write_int8(0xA407E3, 1)
        self.pine.write_int8(0xA407E4, 1)

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
            try:
                val: int = self.pine.read_int16(stat.value["addr"])
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
            addr: int = goblin.value["address"]
            bitflags: int = goblin.value["bits"]
            loc_id = get_location_id(name)
            if loc_id is None:
                continue
            addr_check(addr, bitflags, loc_id)

        # Optional Party Members
        for member in OptionalPartyMembers:
            name: str = EventNames[member.name].value
            addr: int = member.value["address"]
            bitflags: int = member.value["bits"]
            loc_id = get_location_id(name)
            if loc_id is None:
                continue
            addr_check(addr, bitflags, loc_id)

        # Other Side Quests
        for quest in SideQuests:
            name: str = EventNames[quest.name].value
            addr: int = quest.value["address"]
            bitflags: int = quest.value["bits"]
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
            loc_id = get_location_id(name)
            if loc_id is None:
                continue
            addr_check(addr, bitflags, loc_id)

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
                elif isinstance(item, VirusCoreItem):
                    """Add item to inventory"""
                    self.add_key(item.item.value["id"])
                elif isinstance(item, WordListItem):
                    """Add to list of word lists to unlock"""
                    ctx.unlocked_word_lists.add(item.wordlist.value["address"])
                elif isinstance(item, PartyMemberItem):
                    """Add to list of allowed party members"""
                    ctx.unlocked_party_members.add(item.party_member)
                elif isinstance(item, ServerItem):
                    """Add to list of allowed servers"""
                    ctx.unlocked_servers.add(item.server)
                elif isinstance(item, AreaWordItem):
                    """Unlock word"""
                    pass
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
        # for item in ConsumableItems:
        #     if item.item_id in received_id:
        #         self.add_consumable(item)
        # for item in VirusCoreItems:
        #     if item.item_id in received_id:
        #         self.add_key(item.item.value["id"])
        self.set_last_item_index(len(ctx.items_received))

    def add_consumable(self, item_obj: ConsumableItem) -> None:
        addr: int = 0xa40540
        item: int = item_obj.item.value["id"]
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

    async def scan_server(self, ctx) -> None:
        addr: int = 0xa41c04
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
        addr: int = 0xa41bf0
        try:
            val = self.pine.read_int32(addr)
            new_val = val
            for member in PartyMembers:
                m_id = member.value["id"]
                if member in ctx.unlocked_party_members:
                    new_val |= (1 << m_id)
                else:
                    new_val &= ~(1 << (m_id % 32))

            if new_val != val:
                self.pine.write_int32(addr, new_val)
                if ctx.always_online_party_members:
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
