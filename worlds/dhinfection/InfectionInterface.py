from .pcsx2_interface.pine import Pine
from enum import IntEnum
from logging import Logger
from .data.Strings import APConsole, Meta


class ConnectionStatus(IntEnum):
    WRONG_GAME = -1
    DISCONNECTED = 0
    CONNECTED = 1
    IN_GAME = 2


class InfectionInterface:
    pine: Pine = Pine()
    status: ConnectionStatus = ConnectionStatus.DISCONNECTED
    logger: Logger

    def __init__(self, logger: Logger):
        self.logger = logger

    def connect_game(self) -> None:
        if not self.pine.is_connected():
            self.pine.connect()
            if not self.pine.is_connected():
                self.logger.error("Failed to connect to game")
                self.status = ConnectionStatus.DISCONNECTED
                return
            self.status = ConnectionStatus.CONNECTED
        try:
            if self.status is ConnectionStatus.CONNECTED:
                self.logger.info(APConsole.Info.p_init_g.value)
            game_id: str = self.pine.get_game_id()
            self.loaded_game = None
            if game_id in Meta.supported_versions:
                self.loaded_game = Meta.game.value
                self.status = ConnectionStatus.IN_GAME
            elif not self.status is ConnectionStatus.WRONG_GAME:
                self.logger.error(APConsole.Err.game_wrong.value)
                self.status = ConnectionStatus.WRONG_GAME
        except RuntimeError:
            return
        except ConnectionError:
            return

        if self.status is ConnectionStatus.DISCONNECTED:
            self.status = ConnectionStatus.CONNECTED

    def disconnect_game(self) -> None:
        self.pine.disconnect()
        self.loaded_game = None
        self.status = ConnectionStatus.DISCONNECTED

    def get_connection_state(self) -> bool:
        try:
            connected: bool = self.pine.is_connected()
            if connected:
                self.status = ConnectionStatus.CONNECTED
            else:
                self.status = ConnectionStatus.DISCONNECTED
            return connected
        except RuntimeError:
            return False
