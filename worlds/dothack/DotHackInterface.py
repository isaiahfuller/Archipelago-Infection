
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
    VirusCoreItem, RyuBookItem, GruntyFoodItem, InfectionLevelItem, WeaponItem, ArmorItem
from .data.Items import PartyMemberItems
from .data.Items import ServerItems
from .data.Items import WordListItems, RyuBookItems
from .data.Strings import APConsole, Meta, GameStateNames, EventNames, MonsterNames
from .data.items.AreaWords import AreaWords
from .data.items.PartyMembers import PartyMembers
from .data.items.RyuBooks import RyuBooks
from .data.items.Servers import Servers
from .data.locations.Events import InfectionStoryEvents as StoryEvents, InfectionGoldenGoblins as GoldenGoblins, \
    InfectionOptionalPartyMembers as OptionalPartyMembers, MonsterHunt1, MonsterHunt2
from .data.locations.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList, \
    WordListBase, get_wordlist_name
from .pcsx2_interface.pine import Pine

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
        return

    def infection_initial_state(self, ctx) -> None:
        self.pine.write_int8(0xa44ed7, self.pine.read_int8(0xa44ed7) |
                             0b00000111)  # Not needed when setting emails read

        # Unlock Data Drain
        self.pine.write_int8(0xA46141, 1)  # Unlock Data Drain skill category
        self.pine.write_int8(0xA41894, 2)  # Unlock Data Drain, use red dye

        # Ryu Books have been changed to items
        # # Give Ryu Books
        ##self.pine.write_int8(0xA407DD, 1)
        ##self.pine.write_int8(0xA407DE, 1)
        ##self.pine.write_int8(0xA407DF, 1)
        ##self.pine.write_int8(0xA407E0, 1)
        ##self.pine.write_int8(0xA407E1, 1)
        ##self.pine.write_int8(0xA407E2, 1)
        ##self.pine.write_int8(0xA407E3, 1)
        ##self.pine.write_int8(0xA407E4, 1)

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

        # Equal Start - Setting most PCs to base stats, early equipment and Level 1
        if ctx.equal_start:
            if self.pine.read_int8(0xA43C35) == 0:  # Check if return value is 0
                return
            self.pine.write_int8(0xA46F42, 1) # Mia's Level
            self.pine.write_int8(0xA46F58, 70) #Mia's HP
            self.pine.write_int8(0xA46F59, 0)
            self.pine.write_int8(0xA46F5A, 13) #Mia's SP
            self.pine.write_int8(0xA46F5B, 0)
            self.pine.write_int8(0xA46F5C, 16) #Mia's base Attack
            self.pine.write_int8(0xA46F5D, 0)
            self.pine.write_int8(0xA46F5E, 16) #Mia's base Defense
            self.pine.write_int8(0xA46F5F, 0)
            self.pine.write_int8(0xA46F60, 31)  #Mia's base Accuracy
            self.pine.write_int8(0xA46F61, 0)
            self.pine.write_int8(0xA46F62, 31) #Mia's base Evasion
            self.pine.write_int8(0xA46F63, 0)
            self.pine.write_int8(0xA46F64, 13) #Mia's base Magic Attack
            self.pine.write_int8(0xA46F65, 0)
            self.pine.write_int8(0xA46F66, 13) #Mia's base Magic Defense
            self.pine.write_int8(0xA46F67, 0)
            self.pine.write_int8(0xA46F68, 26) #Mia's base Magic Accuracy
            self.pine.write_int8(0xA46F69, 0)
            self.pine.write_int8(0xA46F6a, 25)  #Mia's base Magic Evasion
            self.pine.write_int8(0xA46F6b, 0)
            self.pine.write_int8(0xA46F6e, 13)  #Mia's base Water Element
            self.pine.write_int8(0xA46F6f, 0)
            self.pine.write_int8(0xA46F78, 50) #Mia's base Body
            self.pine.write_int8(0xA46F79, 0)
            self.pine.write_int8(0xA46F7A, 50) #Mia's base Soul
            self.pine.write_int8(0xA46F7B, 0)
            self.pine.write_int8(0xA46FFC, 0) #Mia's Headgear
            self.pine.write_int8(0xA46FFE, 40) #Mia's Body Armor
            self.pine.write_int8(0xA47000, 40) #Mia's Armguards
            self.pine.write_int8(0xA47002, 40) #Mia's Leg Armor
            self.pine.write_int8(0xA47004, 0) #Mia's Weapon
            self.pine.write_int8(0xA46F42, 1) # Mia's Level
            self.pine.write_int8(0xA46F58, 70) #Mia's HP
            self.pine.write_int8(0xA46F59, 0)
            self.pine.write_int8(0xA46F5A, 13) #Mia's SP
            self.pine.write_int8(0xA46F5B, 0)
            self.pine.write_int8(0xA46F5C, 16) #Mia's base Attack
            self.pine.write_int8(0xA46F5D, 0)
            self.pine.write_int8(0xA46F5E, 16) #Mia's base Defense
            self.pine.write_int8(0xA46F5F, 0)
            self.pine.write_int8(0xA46F60, 31)  #Mia's base Accuracy
            self.pine.write_int8(0xA46F61, 0)
            self.pine.write_int8(0xA46F62, 31) #Mia's base Evasion
            self.pine.write_int8(0xA46F63, 0)
            self.pine.write_int8(0xA46F64, 13) #Mia's base Magic Attack
            self.pine.write_int8(0xA46F65, 0)
            self.pine.write_int8(0xA46F66, 13) #Mia's base Magic Defense
            self.pine.write_int8(0xA46F67, 0)
            self.pine.write_int8(0xA46F68, 26) #Mia's base Magic Accuracy
            self.pine.write_int8(0xA46F69, 0)
            self.pine.write_int8(0xA46F6a, 26)  #Mia's base Magic Evasion
            self.pine.write_int8(0xA46F6b, 0)
            self.pine.write_int8(0xA46F6e, 13)  #Mia's base Water Element
            self.pine.write_int8(0xA46F6f, 0)
            self.pine.write_int8(0xA46F78, 50) #Mia's base Body
            self.pine.write_int8(0xA46F79, 0)
            self.pine.write_int8(0xA46F7A, 50) #Mia's base Soul
            self.pine.write_int8(0xA46F7B, 0)
            self.pine.write_int8(0xA46FFC, 0) #Mia's Headgear
            self.pine.write_int8(0xA46FFE, 40) #Mia's Body Armor
            self.pine.write_int8(0xA47000, 40) #Mia's Armguards
            self.pine.write_int8(0xA47002, 40) #Mia's Leg Armor
            self.pine.write_int8(0xA4701E, 1) # Orca's Level
            self.pine.write_int8(0xA47034, 70) #Orca's HP
            self.pine.write_int8(0xA47035, 0)
            self.pine.write_int8(0xA47036, 13) #Orca's SP
            self.pine.write_int8(0xA47037, 0)
            self.pine.write_int8(0xA47038, 16) #Orca's base Attack
            self.pine.write_int8(0xA47039, 0)
            self.pine.write_int8(0xA4703A, 16) #Orca's base Defense
            self.pine.write_int8(0xA4703B, 0)
            self.pine.write_int8(0xA4703C, 31)  #Orca's base Accuracy
            self.pine.write_int8(0xA4703D, 0)
            self.pine.write_int8(0xA4703E, 31) #Orca's base Evasion
            self.pine.write_int8(0xA4703F, 0)
            self.pine.write_int8(0xA47040, 13) #Orca's base Magic Attack
            self.pine.write_int8(0xA47041, 0)
            self.pine.write_int8(0xA47042, 13) #Orca's base Magic Defense
            self.pine.write_int8(0xA47043, 0)
            self.pine.write_int8(0xA47044, 26) #Orca's base Magic Accuracy
            self.pine.write_int8(0xA47045, 0)
            self.pine.write_int8(0xA47046, 26)  #Orca's base Magic Evasion
            self.pine.write_int8(0xA47047, 0)
            self.pine.write_int8(0xA47048, 13)  #Orca's base Earth Element
            self.pine.write_int8(0xA47049, 0)
            self.pine.write_int8(0xA47054, 1) #Orca's base Soul
            self.pine.write_int8(0xA47055, 0)
            self.pine.write_int8(0xA47056, 50) #Orca's base Body
            self.pine.write_int8(0xA47057, 0)
            self.pine.write_int8(0xA470D8, 0) #Orca's Headgear
            self.pine.write_int8(0xA470DA, 40) #Orca's Body Armor
            self.pine.write_int8(0xA470DC, 40) #Orca's Armguards
            self.pine.write_int8(0xA470DE, 40) #Orca's Leg Armor
            self.pine.write_int8(0xA470E0, 2) #Orca's Weapon
            self.pine.write_int8(0xA470FA, 1) # Marlo's Level
            self.pine.write_int8(0xA47110, 70) #Marlo's HP
            self.pine.write_int8(0xA47111, 0)
            self.pine.write_int8(0xA47112, 13) #Marlo's SP
            self.pine.write_int8(0xA47113, 0)
            self.pine.write_int8(0xA47114, 16) #Marlo's base Attack
            self.pine.write_int8(0xA47115, 0)
            self.pine.write_int8(0xA47116, 16) #Marlo's base Defense
            self.pine.write_int8(0xA47117, 0)
            self.pine.write_int8(0xA47118, 31)  #Marlo's base Accuracy
            self.pine.write_int8(0xA47119, 0)
            self.pine.write_int8(0xA4711A, 31) #Marlo's base Evasion
            self.pine.write_int8(0xA4711B, 0)
            self.pine.write_int8(0xA4711C, 13) #Marlo's base Magic Attack
            self.pine.write_int8(0xA4711D, 0)
            self.pine.write_int8(0xA4711E, 13) #Marlo's base Magic Defense
            self.pine.write_int8(0xA4711F, 0)
            self.pine.write_int8(0xA47120, 26) #Marlo's base Magic Accuracy
            self.pine.write_int8(0xA47121, 0)
            self.pine.write_int8(0xA47122, 26)  #Marlo's base Magic Evasion
            self.pine.write_int8(0xA47123, 0)
            self.pine.write_int8(0xA4712E, 13)  #Marlo's base Dark Element
            self.pine.write_int8(0xA4712F, 0)
            self.pine.write_int8(0xA47130, 1) #Marlo's base Soul
            self.pine.write_int8(0xA47131, 0)
            self.pine.write_int8(0xA47132, 50) #Marlo's base Body
            self.pine.write_int8(0xA47133, 0)
            self.pine.write_int8(0xA471B4, 0) #Marlo's Headgear
            self.pine.write_int8(0xA471B6, 40) #Marlo's Body Armor
            self.pine.write_int8(0xA471B8, 40) #Marlo's Armguards
            self.pine.write_int8(0xA471BA, 40) #Marlo's Leg Armor
            self.pine.write_int8(0xA471BC, 7) #Marlo's Weapon
            self.pine.write_int8(0xA471D6, 1) # Sanjuro's Level
            self.pine.write_int8(0xA471EC, 70) #Sanjuro's HP
            self.pine.write_int8(0xA471ED, 0)
            self.pine.write_int8(0xA471EE, 13) #Sanjuro's SP
            self.pine.write_int8(0xA471EF, 0)
            self.pine.write_int8(0xA471F0, 17) #Sanjuro's base Attack
            self.pine.write_int8(0xA471F1, 0)
            self.pine.write_int8(0xA471F2, 15) #Sanjuro's base Defense
            self.pine.write_int8(0xA471F3, 0)
            self.pine.write_int8(0xA471F4, 32)  #Sanjuro's base Accuracy
            self.pine.write_int8(0xA471F5, 0)
            self.pine.write_int8(0xA471F6, 30) #Sanjuro's base Evasion
            self.pine.write_int8(0xA471F7, 0)
            self.pine.write_int8(0xA471F8, 13) #Sanjuro's base Magic Attack
            self.pine.write_int8(0xA471F9, 0)
            self.pine.write_int8(0xA471FA, 13) #Sanjuro's base Magic Defense
            self.pine.write_int8(0xA471FB, 0)
            self.pine.write_int8(0xA471FC, 26) #Sanjuro's base Magic Accuracy
            self.pine.write_int8(0xA471FD, 0)
            self.pine.write_int8(0xA471FE, 26)  #Sanjuro's base Magic Evasion
            self.pine.write_int8(0xA471FF, 0)
            self.pine.write_int8(0xA47206, 13)  #Sanjuro's base Wood Element
            self.pine.write_int8(0xA47207, 0)
            self.pine.write_int8(0xA4720C, 1) #Sanjuro's base Soul
            self.pine.write_int8(0xA4720D, 0)
            self.pine.write_int8(0xA4720E, 50) #Sanjuro's base Body
            self.pine.write_int8(0xA4720F, 0)
            self.pine.write_int8(0xA471B4, 40) #Sanjuro's Headgear
            self.pine.write_int8(0xA471B6, 40) #Sanjuro's Body Armor
            self.pine.write_int8(0xA471B8, 40) #Sanjuro's Armguards
            self.pine.write_int8(0xA471BA, 40) #Sanjuro's Leg Armor
            self.pine.write_int8(0xA472B2, 1) # Nuke Usagimaru's Level
            self.pine.write_int8(0xA472C8, 70) #Nuke Usagimaru's HP
            self.pine.write_int8(0xA472C9, 0)
            self.pine.write_int8(0xA472CA, 13) #Nuke Usagimaru's SP
            self.pine.write_int8(0xA472CB, 0)
            self.pine.write_int8(0xA472CC, 17) #Nuke Usagimaru's base Attack
            self.pine.write_int8(0xA472CD, 0)
            self.pine.write_int8(0xA472CE, 16) #Nuke Usagimaru's base Defense
            self.pine.write_int8(0xA472CF, 0)
            self.pine.write_int8(0xA472D0, 33)  #Nuke Usagimaru's base Accuracy
            self.pine.write_int8(0xA472D1, 0)
            self.pine.write_int8(0xA472D2, 32) #Nuke Usagimaru's base Evasion
            self.pine.write_int8(0xA472D3, 0)
            self.pine.write_int8(0xA472D4, 12) #Nuke Usagimaru's base Magic Attack
            self.pine.write_int8(0xA472D5, 0)
            self.pine.write_int8(0xA472D6, 14) #Nuke Usagimaru's base Magic Defense
            self.pine.write_int8(0xA472D7, 0)
            self.pine.write_int8(0xA472D8, 26) #Nuke Usagimaru's base Magic Accuracy
            self.pine.write_int8(0xA472D9, 0)
            self.pine.write_int8(0xA472DA, 26)  #Nuke Usagimaru's base Magic Evasion
            self.pine.write_int8(0xA472DB, 0)
            self.pine.write_int8(0xA472E4, 13)  #Nuke Usagimaru's base Light Element
            self.pine.write_int8(0xA472E5, 0)
            self.pine.write_int8(0xA472E8, 1) #Nuke Usagimaru's base Soul
            self.pine.write_int8(0xA472E9, 0)
            self.pine.write_int8(0xA472EA, 50) #Nuke Usagimaru's base Body
            self.pine.write_int8(0xA472EB, 0)
            self.pine.write_int8(0xA4736C, 20) #Nuke Usagimaru's Headgear
            self.pine.write_int8(0xA4736E, 20) #Nuke Usagimaru's Body Armor
            self.pine.write_int8(0xA47370, 20) #Nuke Usagimaru's Armguards
            self.pine.write_int8(0xA47372, 20) #Nuke Usagimaru's Leg Armor
            self.pine.write_int8(0xA47374, 0) #Nuke Usagimaru's Weapon
            self.pine.write_int8(0xA4738E, 1) # Balmung's Level
            self.pine.write_int8(0xA473A4, 70) #Balmung's HP
            self.pine.write_int8(0xA473A5, 0)
            self.pine.write_int8(0xA473A6, 13) #Balmung's SP
            self.pine.write_int8(0xA473A7, 0)
            self.pine.write_int8(0xA473A8, 16) #Balmung's base Attack
            self.pine.write_int8(0xA473A9, 0)
            self.pine.write_int8(0xA473AA, 16) #Balmung's base Defense
            self.pine.write_int8(0xA473AB, 0)
            self.pine.write_int8(0xA473AC, 31)  #Balmung's base Accuracy
            self.pine.write_int8(0xA473AD, 0)
            self.pine.write_int8(0xA473AE, 31) #Balmung's base Evasion
            self.pine.write_int8(0xA473AF, 0)
            self.pine.write_int8(0xA473B0, 13) #Balmung's base Magic Attack
            self.pine.write_int8(0xA473B1, 0)
            self.pine.write_int8(0xA473B2, 13) #Balmung's base Magic Defense
            self.pine.write_int8(0xA473B3, 0)
            self.pine.write_int8(0xA473B4, 26) #Balmung's base Magic Accuracy
            self.pine.write_int8(0xA473B5, 0)
            self.pine.write_int8(0xA473B6, 26)  #Balmung's base Magic Evasion
            self.pine.write_int8(0xA473B7, 0)
            self.pine.write_int8(0xA473BA, 13)  #Balmung's base Water Element
            self.pine.write_int8(0xA473BB, 0)
            self.pine.write_int8(0xA473C4, 1) #Balmung's base Soul
            self.pine.write_int8(0xA473C5, 0)
            self.pine.write_int8(0xA473C6, 50) #Balmung's base Body
            self.pine.write_int8(0xA473C7, 0)
            self.pine.write_int8(0xA47448, 0) #Balmung's Headgear
            self.pine.write_int8(0xA4744A, 40) #Balmung's Body Armor
            self.pine.write_int8(0xA4744C, 20) #Balmung's Armguards
            self.pine.write_int8(0xA4744E, 20) #Balmung's Leg Armor
            self.pine.write_int8(0xA47450, 3) #Balmung's Weapon
            self.pine.write_int8(0xA4746A, 1) # Moonstone's Level
            self.pine.write_int8(0xA47480, 63) #Moonstone's HP
            self.pine.write_int8(0xA47481, 0)
            self.pine.write_int8(0xA47482, 13) #Moonstone's SP
            self.pine.write_int8(0xA47483, 0)
            self.pine.write_int8(0xA47484, 15) #Moonstone's base Attack
            self.pine.write_int8(0xA47485, 0)
            self.pine.write_int8(0xA47486, 14) #Moonstone's base Defense
            self.pine.write_int8(0xA47487, 0)
            self.pine.write_int8(0xA47488, 33)  #Moonstone's base Accuracy
            self.pine.write_int8(0xA47489, 0)
            self.pine.write_int8(0xA4748A, 33) #Moonstone's base Evasion
            self.pine.write_int8(0xA4748B, 0)
            self.pine.write_int8(0xA4748C, 14) #Moonstone's base Magic Attack
            self.pine.write_int8(0xA4748D, 0)
            self.pine.write_int8(0xA4748E, 14) #Moonstone's base Magic Defense
            self.pine.write_int8(0xA4748F, 0)
            self.pine.write_int8(0xA47490, 26) #Moonstone's base Magic Accuracy
            self.pine.write_int8(0xA47491, 0)
            self.pine.write_int8(0xA47492, 26)  #Moonstone's base Magic Evasion
            self.pine.write_int8(0xA47493, 0)
            self.pine.write_int8(0xA47496, 13)  #Moonstone's base Water Element
            self.pine.write_int8(0xA47497, 0)
            self.pine.write_int8(0xA474A0, 38) #Moonstone's base Soul
            self.pine.write_int8(0xA474A1, 0)
            self.pine.write_int8(0xA474A2, 33) #Moonstone's base Body
            self.pine.write_int8(0xA474A3, 0)
            self.pine.write_int8(0xA47524, 20) #Moonstone's Headgear
            self.pine.write_int8(0xA47526, 20) #Moonstone's Body Armor
            self.pine.write_int8(0xA47528, 20) #Moonstone's Armguards
            self.pine.write_int8(0xA4752A, 20) #Moonstone's Leg Armor
            self.pine.write_int8(0xA4752C, 3) #Moonstone's Weapon
            self.pine.write_int8(0xA47622, 1) # Wiseman's Level
            self.pine.write_int8(0xA47638, 55) #Wiseman's HP
            self.pine.write_int8(0xA47639, 0)
            self.pine.write_int8(0xA4763A, 20) #Wiseman's SP
            self.pine.write_int8(0xA4763B, 0)
            self.pine.write_int8(0xA4763C, 10) #Wiseman's base Attack
            self.pine.write_int8(0xA4763D, 0)
            self.pine.write_int8(0xA4763E, 14) #Wiseman's base Defense
            self.pine.write_int8(0xA4763F, 0)
            self.pine.write_int8(0xA47640, 33)  #Wiseman's base Accuracy
            self.pine.write_int8(0xA47641, 0)
            self.pine.write_int8(0xA47642, 31) #Wiseman's base Evasion
            self.pine.write_int8(0xA47643, 0)
            self.pine.write_int8(0xA47644, 18) #Wiseman's base Magic Attack
            self.pine.write_int8(0xA47645, 0)
            self.pine.write_int8(0xA47646, 13) #Wiseman's base Magic Defense
            self.pine.write_int8(0xA47647, 0)
            self.pine.write_int8(0xA47648, 32) #Wiseman's base Magic Accuracy
            self.pine.write_int8(0xA47649, 0)
            self.pine.write_int8(0xA4764A, 28)  #Wiseman's base Magic Evasion
            self.pine.write_int8(0xA4764B, 0)
            self.pine.write_int8(0xA47652, 13)  #Wiseman's base Wood Element
            self.pine.write_int8(0xA47653, 0)
            self.pine.write_int8(0xA47658, 50) #Wiseman's base Soul
            self.pine.write_int8(0xA47659, 0)
            self.pine.write_int8(0xA4745A, 2) #Wiseman's base Body
            self.pine.write_int8(0xA4745B, 0)
            self.pine.write_int8(0xA476DC, 0) #Wiseman's Headgear
            self.pine.write_int8(0xA476DE, 0) #Wiseman's Body Armor
            self.pine.write_int8(0xA476E0, 0) #Wiseman's Armguards
            self.pine.write_int8(0xA475E2, 0) #Wiseman's Leg Armor
            self.pine.write_int8(0xA475E4, 9) #Wiseman's Weapon
            self.pine.write_int8(0xA478B6, 1) # Rachel's Level
            self.pine.write_int8(0xA478CC, 70) #Rachel's HP
            self.pine.write_int8(0xA478CD, 0)
            self.pine.write_int8(0xA478CE, 13) #Rachel's SP
            self.pine.write_int8(0xA478CF, 0)
            self.pine.write_int8(0xA478D0, 16) #Rachel's base Attack
            self.pine.write_int8(0xA478D1, 0)
            self.pine.write_int8(0xA478D2, 14) #Rachel's base Defense
            self.pine.write_int8(0xA478D3, 0)
            self.pine.write_int8(0xA478D4, 31)  #Rachel's base Accuracy
            self.pine.write_int8(0xA478D5, 0)
            self.pine.write_int8(0xA478D6, 31) #Rachel's base Evasion
            self.pine.write_int8(0xA478D7, 0)
            self.pine.write_int8(0xA478D8, 13) #Rachel's base Magic Attack
            self.pine.write_int8(0xA478D9, 0)
            self.pine.write_int8(0xA478DA, 13) #Rachel's base Magic Defense
            self.pine.write_int8(0xA478DB, 0)
            self.pine.write_int8(0xA478DC, 26) #Rachel's base Magic Accuracy
            self.pine.write_int8(0xA478DD, 0)
            self.pine.write_int8(0xA478DE, 26)  #Rachel's base Magic Evasion
            self.pine.write_int8(0xA478DF, 0)
            self.pine.write_int8(0xA478E2, 13)  #Rachel's base Water Element
            self.pine.write_int8(0xA474E3, 0)
            self.pine.write_int8(0xA474EC, 1) #Rachel's base Soul
            self.pine.write_int8(0xA474ED, 0)
            self.pine.write_int8(0xA474EE, 50) #Rachel's base Body
            self.pine.write_int8(0xA474EF, 0)
            self.pine.write_int8(0xA47970, 40) #Rachel's Headgear
            self.pine.write_int8(0xA47972, 40) #Rachel's Body Armor
            self.pine.write_int8(0xA47974, 40) #Rachel's Armguards
            self.pine.write_int8(0xA47976, 40) #Rachel's Leg Armor
            self.pine.write_int8(0xA47978, 5) #Rachel's Weapon
            self.pine.write_int8(0xA47992, 1)  # Gardenia's Level
            self.pine.write_int8(0xA479A8, 70)  # Gardenia's HP
            self.pine.write_int8(0xA479A9, 0)
            self.pine.write_int8(0xA479AA, 13)  # Gardenia's SP
            self.pine.write_int8(0xA479AB, 0)
            self.pine.write_int8(0xA479AC, 17)  # Gardenia's base Attack
            self.pine.write_int8(0xA479AD, 0)
            self.pine.write_int8(0xA479AE, 14)  # Gardenia's base Defense
            self.pine.write_int8(0xA479AF, 0)
            self.pine.write_int8(0xA479B0, 33)  # Gardenia's base Accuracy
            self.pine.write_int8(0xA479B1, 0)
            self.pine.write_int8(0xA479B2, 32)  # Gardenia's base Evasion
            self.pine.write_int8(0xA479B3, 0)
            self.pine.write_int8(0xA479B4, 12)  # Gardenia's base Magic Attack
            self.pine.write_int8(0xA479B5, 0)
            self.pine.write_int8(0xA479B6, 14)  # Gardenia's base Magic Defense
            self.pine.write_int8(0xA479B7, 0)
            self.pine.write_int8(0xA479B8, 26)  # Gardenia's base Magic Accuracy
            self.pine.write_int8(0xA479B9, 0)
            self.pine.write_int8(0xA479BA, 26)  # Gardenia's base Magic Evasion
            self.pine.write_int8(0xA479BB, 0)
            self.pine.write_int8(0xA479C6, 13)  # Gardenia's base Dark Element
            self.pine.write_int8(0xA479C7, 0)
            self.pine.write_int8(0xA479C8, 1)  # Gardenia's base Soul
            self.pine.write_int8(0xA479C9, 0)
            self.pine.write_int8(0xA479CA, 50)  # Gardenia's base Body
            self.pine.write_int8(0xA479CB, 0)
            self.pine.write_int8(0xA47A4C, 20)  # Gardenia's Headgear
            self.pine.write_int8(0xA47A4E, 20)  # Gardenia's Body Armor
            self.pine.write_int8(0xA47A50, 20)  # Gardenia's Armguards
            self.pine.write_int8(0xA47A52, 20)  # Gardenia's Leg Armor
            self.pine.write_int8(0xA47A54, 5)  # Gardenia's Weapon
            self.pine.write_int8(0xA47D02, 1)  # Helba's Level
            self.pine.write_int8(0xA47D18, 200)  # Helba's HP
            self.pine.write_int8(0xA47D19, 0)
            self.pine.write_int8(0xA47D1A, 40)  # Helba's SP
            self.pine.write_int8(0xA47D1B, 0)
            self.pine.write_int8(0xA47D1C, 10)  # Helba's base Attack
            self.pine.write_int8(0xA47D1D, 0)
            self.pine.write_int8(0xA47D1E, 10)  # Helba's base Defense
            self.pine.write_int8(0xA47D1F, 0)
            self.pine.write_int8(0xA47D20, 10)  # Helba's base Accuracy
            self.pine.write_int8(0xA47D21, 0)
            self.pine.write_int8(0xA47D22, 10)  # Helba's base Evasion
            self.pine.write_int8(0xA47D23, 0)
            self.pine.write_int8(0xA47D24, 10)  # Helba's base Magic Attack
            self.pine.write_int8(0xA47D25, 0)
            self.pine.write_int8(0xA47D26, 10)  # Helba's base Magic Defense
            self.pine.write_int8(0xA47D27, 0)
            self.pine.write_int8(0xA47D28, 10)  # Helba's base Magic Accuracy
            self.pine.write_int8(0xA47D29, 0)
            self.pine.write_int8(0xA47D2A, 10)  # Helba's base Magic Evasion
            self.pine.write_int8(0xA47D2B, 0)
            self.pine.write_int8(0xA47D2C, 10)  # Helba's base Earth Element
            self.pine.write_int8(0xA47D2D, 0)
            self.pine.write_int8(0xA47D2E, 10)  # Helba's base Water Element
            self.pine.write_int8(0xA47D2F, 0)
            self.pine.write_int8(0xA47D30, 10)  # Helba's base Fire Element
            self.pine.write_int8(0xA47D31, 0)
            self.pine.write_int8(0xA47D32, 10)  # Helba's base Wood Element
            self.pine.write_int8(0xA47D33, 0)
            self.pine.write_int8(0xA47D34, 10)  # Helba's base Light Element
            self.pine.write_int8(0xA47D35, 0)
            self.pine.write_int8(0xA47D36, 10)  # Helba's base Dark Element
            self.pine.write_int8(0xA47D37, 0)
            self.pine.write_int8(0xA47D38, 10)  # Helba's base Soul
            self.pine.write_int8(0xA47D39, 0)
            self.pine.write_int8(0xA47D3A, 10)  # Helba's base Body
            self.pine.write_int8(0xA47D3B, 0)
            self.pine.write_int8(0xA47DBC, 0)  # Helba's Headgear
            self.pine.write_int8(0xA47DBE, 0)  # Helba's Body Armor
            self.pine.write_int8(0xA47DC0, 0)  # Helba's Armguards
            self.pine.write_int8(0xA47DC2, 0)  # Helba's Leg Armor
            self.pine.write_int8(0xA47DC4, 0)  # Helba's Weapon

            self.pine.write_int8(0xA43C35, 0) #Set this value to 0 to not run the initializing again.


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

            # Monster Hunt Delta Server
        for monster_hunt in MonsterHunt1:
            name: str = MonsterNames[monster_hunt.name].value
            addr: int = self.addresses.Monsters[monster_hunt.name]
            bitflags: int = monster_hunt.value["bits"]
            loc_id = get_location_id(name)
            if loc_id is None:
              continue
            addr_check(addr, bitflags, loc_id)

            # Monster Hunt Theta Server
        for monster_hunt in MonsterHunt2:
            name: str = MonsterNames[monster_hunt.name].value
            addr: int = self.addresses.Monsters[monster_hunt.name]
            bitflags: int = monster_hunt.value["bits"]
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
                ctx.queued_messages.append((MessageType.RECEIVED_ITEM, classification_to_color(item.classification), f"{item.name}"))
                self.logger.debug(f"Applying item [{ctx.next_item_slot}]: {item.name}")
                if isinstance(item, ConsumableItem):
                    """Add item to storage"""
                    self.add_consumable(item)
                elif isinstance(item, WeaponItem):
                    """Add weapon to storage"""
                    self.add_weapon(item)
                elif isinstance(item, ArmorItem):
                    """Add armor to storage"""
                    self.add_armor(item)
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

    def add_armor(self, item_obj: ArmorItem) -> None:
        addr: int = self.addresses.Storage
        item: int = item_obj.armor.value["id"]
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
        self.pine.write_int8(0xA4613E, max(0, amt-100))


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
