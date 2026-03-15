
from worlds.dhinfection.data.locations.PlayStats import RyuBookI, RyuBookII, RyuBookVI, RyuBookVII, OtherStats
from worlds.dhinfection import PlayStatNames
from worlds.dhinfection.data.locations.PlayStats import PlayStats, CharacterLevels
import math
from enum import IntEnum
from logging import Logger
from typing import Optional, List, Set

from NetUtils import NetworkItem
from .pcsx2_interface.pine import Pine
from . import InfectionItem
from .data.Strings import APConsole, Meta, InfectionGameStateNames as GameStateNames, InfectionAreaWordNames as AreaWordNames, InfectionEventNames as EventNames
from .data.GameState import InfectionGameState as GameState
from .data.locations.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList, InfectionWordListBase as WordListBase
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
        try:
            st_val = self.pine.read_int8(address)
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

        # Get Mia and Elk out of your way
        self.pine.write_int8(0xa44f58, self.pine.read_int8(0xa44f58) | 0xff)

    async def check_locations(self, ctx) -> None:
        checked: Set[int] = set()

        def get_location_id(name: str) -> int | None:
            loc_id = ctx.locations_name_to_id.get(name)
            if loc_id is None or loc_id in checked:
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
                if stat.value["scale"] == "list" and val in stat.value["values"]:
                    for i in stat.value["values"]:
                        if val < i:
                            break
                        loc_id = get_location_id(f"{name}{i}")
                        if loc_id is None:
                            continue
                        checked.add(loc_id)
                elif stat.value["scale"] == "range" and val in range(stat.value["values"][0], stat.value["values"][1] + 1):
                    for i in range(stat.value["values"][0], stat.value["values"][1] + 1):
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
            addr: int = goblin.value["address"]
            bitflags: int = goblin.value["bits"]
            loc_id = get_location_id(name)
            if loc_id is None:
                continue
            addr_check(addr, bitflags, loc_id)

        # Optional Party Members
        for member in OptionalPartyMembers:
            addr: int = member.value["address"]
            bitflags: int = member.value["bits"]
            loc_id = get_location_id(name)
            if loc_id is None:
                continue
            addr_check(addr, bitflags, loc_id)

        # Other Side Quests
        for quest in SideQuests:
            addr: int = quest.value["address"]
            bitflags: int = quest.value["bits"]
            loc_id = get_location_id(name)
            if loc_id is None:
                continue
            addr_check(addr, bitflags, loc_id)

        # Character Levels
        for level in CharacterLevels:
            stat_check(level)

        # Ryu Book stats
        for stat in RyuBookI:
            stat_check(stat)
        for stat in RyuBookII:
            stat_check(stat)
        for stat in RyuBookVI:
            stat_check(stat)
        for stat in RyuBookVII:
            stat_check(stat)
        for stat in OtherStats:
            stat_check(stat)

        if checked:
            ctx.checked_locations.update(checked)
            if ctx.server:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": checked}])
            else:
                ctx.offline_locations_checked.update(checked)

    async def receive_items(self, ctx) -> None:
        if ctx.last_item_processed_index < 0:
            ctx.last_item_processed_index = self.get_last_item_index()
        elif ctx.last_item_processed_index:
            if ctx.next_item_slot < 0:
                ctx.next_item_slot = ctx.last_item_processed_index
            else:
                ctx.next_item_slot = max(min(ctx.last_item_processed_index, ctx.next_item_slot), 0)

        if not ctx.next_item_slot and ctx.items_received and ctx.checked_locations:
            ctx.next_item_slot = len(ctx.items_received)
        received: List[NetworkItem] = ctx.items_received[ctx.next_item_slot:]
        ctx.next_item_slot += len(received)
        ctx.last_item_processed_index = ctx.next_item_slot
        for server_item in received:
            item: InfectionItem = Items.from_id(server_item.item)

            if isinstance(item, ConsumableItem):
                """Add item to storage"""
                self.add_consumable(item)
            if isinstance(item, VirusCoreItem):
                """Add item to inventory"""
                addr: int = item.item.value["id"]
                curr_amt = self.pine.read_int8(addr)
                self.pine.write_int8(addr, curr_amt + 1)
            if isinstance(item, AreaWordItem):
                """Unlock word"""
            if isinstance(item, WordListItem):
                """Add to list of word lists to unlock"""
                ctx.unlocked_word_lists.append(item.wordlist.value["address"])
            if isinstance(item, PartyMemberItem):
                """Add to list of allowed party members"""
                ctx.unlocked_party_members.append(item.party_member)
            if isinstance(item, ServerItem):
                """Add to list of allowed servers"""
                ctx.unlocked_servers.append(item.server)
        if received:
            self.set_last_item_index(ctx.next_item_slot)

    async def resync_items(self, ctx) -> None:
        """
        Syncs items that were received before the client was fully initialized.
        Issue: Virus Cores and Consumables are currently only given once.
        """
        if ctx.last_item_processed_index < 0:
            return
        received_id = [item[0] for item in ctx.items_received[self.get_last_item_index():]]
        for member in PartyMemberItems:
            if member.item_id in received_id:
                ctx.unlocked_party_members.append(member.party_member)
        for server in ServerItems:
            if server.item_id in received_id:
                ctx.unlocked_servers.append(server.server)
        for wordlist in WordListItems:
            if wordlist.item_id in received_id:
                ctx.unlocked_word_lists.append(wordlist.wordlist.value["address"])
        for item in ConsumableItems:
            if item.item_id in received_id:
                self.add_consumable(item)
        for item in VirusCoreItems:
            if item.item_id in received_id:
                self.add_key(item.item.value["id"])
        self.set_last_item_index(len(ctx.items_received))

    def add_consumable(self, item_obj: ConsumableItem) -> None:
        addr: int = 0xa40540
        item: int = item_obj.item.value["id"]
        for i in range(addr, addr + 99, 4):
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
        Reported issue: Unlocks Natsume and Rachel when only Nuke Usagimaru is unlocked.
        - ids: Natsume (11), Rachel (12), Nuke Usagimaru (5)

        Order: 
        - Iterate through ALL members
        - Calculate offset
        - Read current value
        - Apply mask
        - Write value
        """
        addr: int = 0xa41bf0
        for member in PartyMembers:
            offset: int = math.floor(member.value["id"] / 8)
            unlocked_members: int = self.pine.read_int8(offset + addr)
            val = unlocked_members
            if member not in ctx.unlocked_party_members:
                val &= ~(2 ** (member.value["id"] % 8))
            else:
                val |= 2 ** (member.value["id"] % 8)
            self.pine.write_int8(offset + addr, val)

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
        starting_addr: int = 0xa44d46
        ending_addr: int = 0xa44c47
        current_list: int | None = None

        for i in range(starting_addr, ending_addr, -1):
            current_addr: int = self.pine.read_int8(i)
            delta_member: DeltaWordList | None = DeltaWordList.from_address(
                current_addr)
            theta_member: ThetaWordList | None = ThetaWordList.from_address(
                current_addr)
            current_list: int | None = None
            current_list_obj: WordListBase | None = None
            if delta_member:
                current_list = delta_member.value["address"]
                current_list_obj = delta_member
            elif theta_member:
                current_list = theta_member.value["address"]
                current_list_obj = theta_member
            if current_list:
                if current_list not in ctx.obtained_word_lists:
                    ctx.obtained_word_lists.append(current_list)
                    if ctx.server:
                        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [ctx.locations_name_to_id[current_list_obj.name]]}])
                if current_list in ctx.unlocked_word_lists:
                    self.pine.write_int8(i + 1, 0x00)
                else:
                    self.pine.write_int8(i + 1, 0xff)

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
