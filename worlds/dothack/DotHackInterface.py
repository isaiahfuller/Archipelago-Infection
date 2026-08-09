
import math
from enum import IntEnum
from logging import Logger
from typing import Optional, List, Set
import pkgutil
from BaseClasses import ItemClassification
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
from .data.Strings import APConsole, Meta, GameStateNames, EventNames, ShopsanityNames, TradesanityNames
from .data.items.AreaWords import AreaWords
from .data.items.PartyMembers import PartyMembers
from .data.items.RyuBooks import RyuBooks
from .data.items.Servers import Servers
from .data.locations.Events import InfectionStoryEvents as StoryEvents, InfectionGoldenGoblins as GoldenGoblins, \
    InfectionOptionalPartyMembers as OptionalPartyMembers
from .data.locations.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList, \
    WordListBase, get_wordlist_name
from .data.locations.Sanity import InfectionShopsanity, APItems
from .pcsx2_interface.pine import Pine
import random
from .DotHackOptions import APItemPrice, APHelper


# Notes:
# latest item idx can seemingly be written to 0xA44EC8 safely.
# game doesn't seem to use it for anything.

class MessageType(IntEnum):
    RAW = 0
    RECEIVED_ITEM = 1

class MessageColor(IntEnum):
    WHITE = 7
    BLACK = 15
    RED = 24
    GREEN = 25
    YELLOW = 26
    BLUE = 27
    MAGENTA = 28
    CYAN = 29
    SLATEBLUE = 30
    PLUM = 31
    SALMON = 32
    ORANGE = 34

def classification_to_color(classification: ItemClassification) -> int:
    if classification == ItemClassification.filler:
        return MessageColor.CYAN
    elif classification & ItemClassification.progression:  # advancement
        return MessageColor.PLUM
    elif classification & ItemClassification.useful:  # useful
        return MessageColor.SLATEBLUE
    elif classification & ItemClassification.trap:  # trap
        return MessageColor.SALMON
    else:
        return MessageColor.CYAN

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
        self._cached_value = None
        self.random = random
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

    def infection_apply_patch(self):
        current_overlay = self.pine.read_int8(0x00400804)

        if current_overlay == 1:
            # gcmn.prg is loaded

            if self.pine.read_int32(0x0051d12c) == 0x8f849174:
                # Patch has not been written
                #These will remove the suppression and deletion of Key Items from NPC Trading Menus
                self.pine.write_int32(0x54E8D8, 00000000)
                self.pine.write_int32(0x5517A8, 00000000)
                self.pine.write_int32(0x54F680, 00000000)



                patch_data = pkgutil.get_data(__name__, "data/infection.patch")
                if patch_data:
                    self.pine.write_bytes(0x006f9e50, patch_data)

                    # Hook
                    self.pine.write_bytes(0x0051d12c, bytes([0x2d, 0x20, 0x00, 0x02, 0x94, 0xE7, 0x1B, 0x0C]))

    def infection_show_message(self, message_type: int, color: int, message: str) -> int:
        address = 0x6FA660
        size = 0x46
        current_overlay = self.pine.read_int8(0x00400804)

        if current_overlay != 1 or self.pine.read_int8(address) == 0x83:
            return 1

        message_bytes = bytes([*message.encode("shift-jis"), 0])
        if len(message_bytes) > 64:
            print(f"Message too long ({len(message_bytes)} bytes)")
            return 2

        for i in range(4):
            status = self.pine.read_int8(address + i*size)
            if status == 0:
                self.pine.write_int8(address + i*size + 1, 0) # Queue position
                self.pine.write_int8(address + i*size + 2, color) # Color
                self.pine.write_int8(address + i*size + 3, message_type) # Type
                self.pine.write_int16(address + i*size + 4, 120) # Frames
                self.pine.write_bytes(address + i*size + 6, message_bytes) # Text
                self.pine.write_int8(address + i*size + 0, 1) # Status
                return 0

        return 3

    def inject_ap_items(self, ctx=None) -> None:
        """
        Injects randomized APItems into the trade tables.
        Party Members receive 3 items; NPCs receive 1 item.
        Items are appended starting at the first 0xFFFFFF00 sentinel.
        """
        # Configuration: (Label, Base Address, Entity Count, Stride, Amount to Inject)
        targets = [
            ("Party Members", 0xA4080C, 0x11, 0x40, 3),
            ("NPCs", 0xA40C64, 0x27, 0x40, 1)
        ]

        for label, base_addr, count, stride, amount in targets:
            self.logger.info(f"Processing {label} trade table injection...")

            for i in range(count):
                entity_block_start = base_addr + (i * stride)
                found_sentinel = False

                # Scan for the sentinel value 0xFFFFFF00
                for slot_index in range(16):
                    curr_addr = entity_block_start + (slot_index * 4)
                    val = self.pine.read_int32(curr_addr)

                    if (val & 0xFFFF) == 0xFFFF:
                        # We found the end of the existing list.
                        # Inject 'amount' number of random items.
                        for j in range(amount):
                            # Calculate the injection address relative to the sentinel
                            inject_addr = curr_addr + (j * 4)

                            # Safety Check: Ensure we don't write past the 0x40 block boundary
                            if inject_addr < (entity_block_start + 0x40):
                                random_item = random.choice(list(APItems)).value
                                self.pine.write_int32(inject_addr, random_item)

                        found_sentinel = True

                        break # Move to the next entity


                if not found_sentinel:
                    self.logger.warning(f"No empty slot found for {label} at index {i}")


    def infection_initial_state(self, ctx) -> None:
        self.pine.write_int8(0xa44ed7, self.pine.read_int8(0xa44ed7) |
                             0b00000111)  # Not needed when setting emails read

        # Unlock Data Drain
        self.pine.write_int8(0xA46141, 1)  # Unlock Data Drain skill category
        self.pine.write_int8(0xA41894, 2)  # Unlock Data Drain, use red dye

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
            if loc_id is None or loc_id in checked \
                    or loc_id in ctx.checked_locations \
                    or loc_id in ctx.excluded_locations:
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
        if ctx.golden_goblins:
            for goblin in GoldenGoblins:
                name: str = EventNames[goblin.name].value
                addr: int = self.addresses.Events[goblin.name]
                bitflags: int = goblin.value["bits"]
                loc_id = get_location_id(name)
                if loc_id is None:
                    continue
                addr_check(addr, bitflags, loc_id)

        # Optional Party Members
        if ctx.optional_party_members:
            for member in OptionalPartyMembers:
                name: str = EventNames[member.name].value
                addr: int = self.addresses.Events[member.name]
                bitflags: int = member.value["bits"]
                loc_id = get_location_id(name)
                if loc_id is None:
                    continue
                addr_check(addr, bitflags, loc_id)

        #Shopsanity
        if ctx.shopsanity:
            for shopsanity in InfectionShopsanity:
                name: str = ShopsanityNames[shopsanity.name].value
                addr: int = self.addresses.Shopsanity[shopsanity.name]
                bitflags: int = shopsanity.value["bits"]
                loc_id = get_location_id(name)
                if loc_id is None:
                    continue
                addr_check(addr, bitflags, loc_id)

        #Tradesanity
        if ctx.tradesanity:
            current_overlay = self.pine.read_int8(0x00400804)

            if current_overlay == 1:
                for tradesanity in TradesanityNames:
                    name: str = TradesanityNames[tradesanity.name].value
                    addr: int = self.addresses.Tradesanity[tradesanity.name]
                    bitflags: int = 0xFF
                    loc_id = get_location_id(name)
                    print(f"[DEBUG] Checking {name}: Addr={hex(addr)}, Bit={bitflags}, ID={loc_id}")
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
                ctx.queued_messages.append((MessageType.RECEIVED_ITEM, classification_to_color(item.classification), f"{item.name}"))
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
        self.pine.write_int8(0xA4613E, 0)

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

    async def setup_sanity(self, ctx) -> None:
        # Creation of Archipelago Item Labels and Prices - Rerun at every resync.
        self.pine.write_bytes(0x6BB358, bytes([0x41, 0x50, 0x20, 0x49, 0x74, 0x65, 0x6D, 0x00])) #Replace The Twilight with AP Item
        self.pine.write_bytes(0x6BEC08, bytes([0x41, 0x50, 0x20, 0x49, 0x74, 0x65, 0x6D, 0x00])) #Replace M:Wavemaster with AP Item
        self.pine.write_bytes(0x6BEC38, bytes([0x41, 0x50, 0x20, 0x49, 0x74, 0x65, 0x6D, 0x00])) #Replace M:Twin Blade with AP Item
        self.pine.write_bytes(0x6BEC48, bytes([0x41, 0x50, 0x20, 0x49, 0x74, 0x65, 0x6D, 0x00])) #Replace M:Heavy Axeman with AP Item
        self.pine.write_bytes(0x6BEC58, bytes([0x41, 0x50, 0x20, 0x49, 0x74, 0x65, 0x6D, 0x00])) #Replace M:Long Arm with AP Item


        #Prices will be set for each of the five items, then saved to 20 bytes in total. Using 20 bytes of the free space starting at 0xA47E10
        #Each of the AP Items Prices randomly determined from the range of Start and End
        if not (self.pine.read_int8(0xA47E04) & 0x01): #Unused data
            price1 = self.random.randint(APItemPrice.range_start, ctx.apitemprice)
            self.pine.write_int32(0xA47E10, price1)
            price2 = self.random.randint(APItemPrice.range_start, ctx.apitemprice)
            self.pine.write_int32(0xA47E14, price2)
            price3 = self.random.randint(APItemPrice.range_start, ctx.apitemprice)
            self.pine.write_int32(0xA47E18, price3)
            price4 = self.random.randint(APItemPrice.range_start, ctx.apitemprice)
            self.pine.write_int32(0xA47E1C, price4)
            price5 = self.random.randint(APItemPrice.range_start, ctx.apitemprice)
            self.pine.write_int32(0xA47E20, price5)
            self.pine.write_int8(0xA47E04, self.pine.read_int8(0xa47E04) | 0x01)

        #Take the prices saved to memory and write them to the 5 Key Items
        apprice1 = self.pine.read_int32(0xA47E10)
        self.pine.write_int32(0x6247F8, apprice1)
        apprice2 = self.pine.read_int32(0xA47E14)
        self.pine.write_int32(0x6259C8, apprice2)
        apprice3 = self.pine.read_int32(0xA47E18)
        self.pine.write_int32(0x6259DC, apprice3)
        apprice4 = self.pine.read_int32(0xA47E1C)
        self.pine.write_int32(0x6259F0, apprice4)
        apprice5 = self.pine.read_int32(0xA47E20)
        self.pine.write_int32(0x625A04, apprice5)

        #Set the item description of the AP Items to The Twilight's and change it to "I wonder what's inside?"
        description = 0x006BB370
        self.pine.write_int32(0x6259CC, description)
        self.pine.write_int32(0x6259E0, description)
        self.pine.write_int32(0x6259F4, description)
        self.pine.write_int32(0x625A08, description)
        self.pine.write_bytes(0x6BB370, bytes([0x49, 0x20, 0x77, 0x6F, 0x6E, 0x64, 0x65, 0x72, 0x20, 0x77, 0x68, 0x61, 0x74, 0x27, 0x73, 0x20, 0x69, 0x6E, 0x73, 0x69, 0x64, 0x65, 0x3F, 0x00, 0x00, 0x00, 0x00]))

        #Always set the AP Items slot in Key Items to 0.

        self.pine.write_int8(0xA40707, 0x00)
        self.pine.write_int8(0xA407EB, 0x00)
        self.pine.write_int8(0xA407EC, 0x00)
        self.pine.write_int8(0xA407ED, 0x00)
        self.pine.write_int8(0xA407EE, 0x00)

        if ctx.shopsanity:
            if self.pine.read_int8(0x648664) == 0:
                self.pine.write_bytes(0x648088, bytes([0x3B, 0x00, 0x0F, 0x00, 0x1F, 0x01, 0x0F, 0x00, 0x20, 0x01, 0x0F, 0x00, 0x21, 0x01, 0x0F, 0x00, 0x22, 0x01, 0x0F, 0x00,]))  # Add the 5 AP Items to Mac Anu Item Shop
                self.pine.write_bytes(0x6480E8, bytes([0x3B, 0x00, 0x0F, 0x00, 0x1F, 0x01, 0x0F, 0x00, 0x20, 0x01, 0x0F, 0x00, 0x21, 0x01, 0x0F, 0x00, 0x22, 0x01, 0x0F, 0x00,]))  # Add the 5 AP Items to Dun Loireag Item Shop
                self.pine.write_bytes(0x648270, bytes([0x3B, 0x00, 0x0F, 0x00, 0x1F, 0x01, 0x0F, 0x00, 0x20, 0x01, 0x0F, 0x00, 0x21, 0x01, 0x0F, 0x00, 0x22, 0x01, 0x0F, 0x00,]))  # Add the 5 AP Items to Mac Anu Weapon Shop
                self.pine.write_bytes(0x6482FC, bytes([0x3B, 0x00, 0x0F, 0x00, 0x1F, 0x01, 0x0F, 0x00, 0x20, 0x01, 0x0F, 0x00, 0x21, 0x01, 0x0F, 0x00, 0x22, 0x01, 0x0F, 0x00,]))  # Add the 5 AP Items to Dun Loireag Weapon Shop
                self.pine.write_bytes(0x648488, bytes([0x3B, 0x00, 0x0F, 0x00, 0x1F, 0x01, 0x0F, 0x00, 0x20, 0x01, 0x0F, 0x00, 0x21, 0x01, 0x0F, 0x00, 0x22, 0x01, 0x0F, 0x00,]))  # Add the 5 AP Items to Mac Anu Magic Shop
                self.pine.write_bytes(0x6484F8, bytes([0x3B, 0x00, 0x0F, 0x00, 0x1F, 0x01, 0x0F, 0x00, 0x20, 0x01, 0x0F, 0x00, 0x21, 0x01, 0x0F, 0x00, 0x22, 0x01, 0x0F, 0x00,]))  # Add the 5 AP Items to Dun Loireag Magic Shop
                self.pine.write_int8(0x648664, 1)
            if self.pine.read_int8(0xA47E05) & 0b00000001:  # If an AP Item in Mac Anu Weapon Shop has been purchased
                self.pine.write_int32(0x648270, 0x000D0000)  # Set it to Fortune Wire
            if self.pine.read_int8(0xA47E05) & 0b00000010:
                self.pine.write_int32(0x648274, 0x000D0000)
            if self.pine.read_int8(0xA47E05) & 0b00000100:
                self.pine.write_int32(0x648278, 0x000D0000)
            if self.pine.read_int8(0xA47E05) & 0b00001000:
                self.pine.write_int32(0x64827C, 0x000D0000)
            if self.pine.read_int8(0xA47E05) & 0b00010000:
                self.pine.write_int32(0x648280, 0x000D0000)
            if self.pine.read_int8(0xA47E05) & 0b00100000:  # If an AP Item in Mac Anu Item Shop has been purchased
                self.pine.write_int32(0x648088, 0x000D0000)  # Set it to Fortune Wire
            if self.pine.read_int8(0xA47E05) & 0b01000000:
                self.pine.write_int32(0x64808C, 0x000D0000)
            if self.pine.read_int8(0xA47E05) & 0b10000000:
                self.pine.write_int32(0x648090, 0x000D0000)
            if self.pine.read_int8(0xA47E06) & 0b00000001:
                self.pine.write_int32(0x648094, 0x000D0000)
            if self.pine.read_int8(0xA47E06) & 0b00000010:
                self.pine.write_int32(0x648098, 0x000D0000)
            if self.pine.read_int8(0xA47E06) & 0b00000100:  # If an AP Item in Mac Anu Magic Shop has been purchased
                self.pine.write_int32(0x648488, 0x000D0000)  # Set it to Fortune Wire
            if self.pine.read_int8(0xA47E06) & 0b00001000:
                self.pine.write_int32(0x64848C, 0x000D0000)
            if self.pine.read_int8(0xA47E06) & 0b00010000:
                self.pine.write_int32(0x648490, 0x000D0000)
            if self.pine.read_int8(0xA47E06) & 0b00100000:
                self.pine.write_int32(0x648494, 0x000D0000)
            if self.pine.read_int8(0xA47E06) & 0b01000000:
                self.pine.write_int32(0x648498, 0x000D0000)
            if self.pine.read_int8(0xA47E07) & 0b00000001:  # If an AP Item in Dun Loireag Weapon Shop has been purchased
                self.pine.write_int32(0x6482FC, 0x0009002A)  # Set it to Mountain Guard
            if self.pine.read_int8(0xA47E07) & 0b00000010:
                self.pine.write_int32(0x648300, 0x000D0000) #Set it to Fortune Wire
            if self.pine.read_int8(0xA47E07) & 0b00000100:
                self.pine.write_int32(0x648304, 0x000D0000)
            if self.pine.read_int8(0xA47E07) & 0b00001000:
                self.pine.write_int32(0x648308, 0x000D0000)
            if self.pine.read_int8(0xA47E07) & 0b00010000:
                self.pine.write_int32(0x64830C, 0x000D0000)
            if self.pine.read_int8(0xA47E07) & 0b00100000:  # If an AP Item in Dun Loireag Item Shop has been purchased
                self.pine.write_int32(0x6480E8, 0x000D0000)  # Set it to Fortune Wire
            if self.pine.read_int8(0xA47E07) & 0b01000000:
                self.pine.write_int32(0x6480EC, 0x000D0000)
            if self.pine.read_int8(0xA47E07) & 0b10000000:
                self.pine.write_int32(0x6480F0, 0x000D0000)
            if self.pine.read_int8(0xA47E08) & 0b00000001:
                self.pine.write_int32(0x6480F4, 0x000D0000)
            if self.pine.read_int8(0xA47E08) & 0b00000010:
                self.pine.write_int32(0x6480F8, 0x000D0000)
            if self.pine.read_int8(0xA47E08) & 0b00000100:  # If an AP Item in Mac Anu Magic Shop has been purchased
                self.pine.write_int32(0x6484F8, 0x000D0000)  # Set it to Fortune Wire
            if self.pine.read_int8(0xA47E08) & 0b00001000:
                self.pine.write_int32(0x6484FC, 0x000D0000)
            if self.pine.read_int8(0xA47E08) & 0b00010000:
                self.pine.write_int32(0x648500, 0x000D0000)
            if self.pine.read_int8(0xA47E08) & 0b00100000:
                self.pine.write_int32(0x648504, 0x000D0000)
            if self.pine.read_int8(0xA47E08) & 0b01000000:
                self.pine.write_int32(0x648508, 0x000D0000)
        if ctx.tradesanity:
            current_val = self.pine.read_int8(0xA47E04)
            if not (current_val & 0x02):
                self.logger.info("Tradesanity enabled: Injecting AP items into trade tables...")
                try:
                    self.inject_ap_items(ctx)
                    self.logger.info("AP items successfully injected.")
                    self.pine.write_int8(0xA47E04, current_val | 0x02)

                except Exception as e:
                    self.logger.error(f"Injection failed: {e}")


    async def monitor_decrease(self) -> None:
        try:
            current_value: int = self.pine.read_int32(0xA46E6C)
            if self._cached_value is None:
                self._cached_value = current_value
                return

            if current_value < self._cached_value:
                # 1. Immediate Capture (Atomic Snapshot)
                server_id = self.pine.read_int8(0xA3F60C)
                shop_type = self.pine.read_int8(0x72F2F1)
                cursor_pos = self.pine.read_int8(0x72F670)

                delta = self._cached_value - current_value
                target_addr = None
                flag_bit = 0

                # 2. Address Resolution Logic
                if server_id == 0:  # Mac Anu
                    if shop_type == 1:  # Weapon
                        mapping = {0x08: 0b00000001, 0x09: 0b00000010, 0x0A: 0b00000100, 0x0B: 0b00001000,
                                   0x0C: 0b00010000}
                        if cursor_pos in mapping:
                            target_addr, flag_bit = 0xA47E05, mapping[cursor_pos]
                    elif shop_type == 4:  # Item
                        mapping = {0x0E: 0b00100000, 0x0F: 0b01000000, 0x10: 0b10000000,
                                   0x11: 0b00000001, 0x12: 0b00000010}
                        if cursor_pos in mapping:
                            target_addr = 0xA47E05 if cursor_pos <= 0x10 else 0xA47E06
                            flag_bit = mapping[cursor_pos]
                    elif shop_type == 8:  # Magic
                        mapping = {0x0E: 0b00000100, 0x0F: 0b00001000, 0x10: 0b00010000, 0x11: 0b00100000,
                                   0x12: 0b01000000}
                        if cursor_pos in mapping:
                            target_addr, flag_bit = 0xA47E06, mapping[cursor_pos]

                elif server_id == 1:  # Dun Loireag
                    if shop_type == 1:  # Weapon
                        mapping = {0x13: 0b00000001, 0x14: 0b00000010, 0x15: 0b00000100, 0x16: 0b00001000,
                                   0x17: 0b00010000}
                        if cursor_pos in mapping:
                            target_addr, flag_bit = 0xA47E07, mapping[cursor_pos]
                    elif shop_type == 4:  # Item
                        mapping = {0x0E: 0b00100000, 0x0F: 0b01000000, 0x10: 0b10000000, 0x11: 0b00000001,
                                   0x12: 0b00000010}
                        if cursor_pos in mapping:
                            target_addr = 0xA47E07 if cursor_pos <= 0x10 else 0xA47E08
                            flag_bit = mapping[cursor_pos]
                    elif shop_type == 8:  # Magic
                        mapping = {0x0E: 0b00000100, 0x0F: 0b00001000, 0x10: 0b00010000, 0x11: 0b00100000,
                                   0x12: 0b01000000}
                        if cursor_pos in mapping:
                            target_addr, flag_bit = 0xA47E08, mapping[cursor_pos]

                # 3. Critical Write Path (Outside the server_id blocks)
                if target_addr and flag_bit:
                    current_flag = self.pine.read_int8(target_addr)
                    self.pine.write_int8(target_addr, current_flag | flag_bit)

                # 4. Post-write callback (Non-blocking sequence)
                await self.on_value_decrease(delta, current_value)

            self._cached_value = current_value
        except (RuntimeError, ConnectionError):
            pass

    async def on_value_decrease(self, delta: int, current_val: int):
        """This is the callback function that runs only when a drop is detected."""