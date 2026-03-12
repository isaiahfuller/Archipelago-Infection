from .pcsx2_interface.pine import Pine
from enum import IntEnum
from logging import Logger
from typing import Optional
from .data.Strings import APConsole, Meta, InfectionGameStateNames
from .data.GameState import InfectionGameState
from .data.locations.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList
from .data.items.AreaWords import InfectionAreaWords as AreaWords
from .data.items.Servers import InfectionServers as Servers
from .data.items.PartyMembers import InfectionPartyMembers as PartyMembers
from .data.items.AreaWords import InfectionAreaWords as AreaWords


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

    def get_ingame_status(self) -> InfectionGameStateNames | None:
        address = 0xa3f5f0
        try:
            return InfectionGameStateNames(InfectionGameState(self.pine.get_memory(address)).name)
        except RuntimeError:
            return None
        except ConnectionError:
            return None

    def modify_word(self, word: AreaWords, lock: bool = False) -> None:
        offset: int = math.floor(word / 8)
        unlocked_words: int = self.pine.read_int8(offset + 0xa44c0c)
        if lock:
            self.pine.write_int8(offset + 0xa44c0c, unlocked_words & ~(2 ** (word % 8)))
        else:
            self.pine.write_int8(offset + 0xa44c0c, unlocked_words | 2 ** (word % 8))

    def scan_word_list(self, ctx) -> None:
        starting_addr: int = 0xa44d46
        ending_addr: int = 0xa44c47

        for i in range(starting_addr, ending_addr, -1):
            current_addr: int = self.pine.read_int8(i)
            delta_member: DeltaWordList | None = DeltaWordList.from_address(
                current_addr)
            combined_list: DeltaWordList | ThetaWordList | None = None
            if delta_member:
                combined_list = delta_member
            else:
                combined_list = ThetaWordList.from_address(current_addr)
            if combined_list:
                if combined_list in current_word_list:
                    if combined_list not in unlocked_word_list:
                        self.pine.write_int8(i + 1, 0xff)
                        for word in combined_list.value["words"]:
                            self.modify_word(word, True)
                else:
                    self.pine.write_int8(i + 1, 0x00)
                    for word in combined_list.value["words"]:
                        self.modify_word(word, False)
            else:
                current_word_list.add(combined_list)
                self.pine.write_int8(i + 1, 0x00)
                words = []
                for word in combined_list.value["words"]:
                    self.modify_word(word, False)
                    words.append(AreaWordNames[word.name].value)
                self.logger.info(f"New Delta Word: {words[0]} {words[1]} {words[2]}")
