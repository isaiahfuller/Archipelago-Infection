import asyncio
import typing
import multiprocessing
import traceback
from typing import Optional, Sequence, List

from CommonClient import ClientStatus, logger
from settings import get_settings
import Utils

from . import InfectionSettings
from .data.Strings import APConsole, APHelper, InfectionGameStateNames, InfectionCharacterNames, InfectionAreaWordNames, Meta
from .InfectionInterface import InfectionInterface, ConnectionStatus
from .data import Locations, Items

from .data.locations.WordList import InfectionWordListBase as WordListBase
from .data.items.PartyMembers import InfectionPartyMembers as PartyMembers
from .data.items.Servers import InfectionServers as Server
from .data.items.AreaWords import InfectionAreaWords as AreaWords

gui_loaded_from_utils: bool = False
try:
    from Utils import gui_enabled
    gui_loaded_from_utils = True
except ImportError:
    pass

tracker_loaded: bool = False
try:
    from worlds.tracker.TrackerClient import (
        ClientCommandProcessor, TrackerGameContext as SuperContext, get_base_parser, server_loop)
    tracker_loaded = True
    if not gui_loaded_from_utils:
        from worlds.tracker.TrackerClient import gui_enabled
except ImportError:
    from CommonClient import (
        ClientCommandProcessor, CommonContext as SuperContext, get_base_parser, server_loop)
    if not gui_loaded_from_utils:
        from CommonClient import gui_enabled


class InfectionCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: SuperContext):
        super().__init__(ctx)

    def _cmd_resync(self) -> None:
        """
        Resyncs the client with the game.
        """
        if not isinstance(self.ctx, InfectionContext):
            return
        if self.ctx.is_game_connected and self.ctx.server:
            self.ctx.pending_resync = True

    def _cmd_status(self) -> None:
        """
        Shows the status of the client.
        """
        if isinstance(self.ctx, InfectionContext):
            logger.info(f"Client Status")
            if tracker_loaded:
                logger.info(f"Universal Tracker Integrated")
            logger.info(f"Game")
            if self.ctx.server:
                game_status: int = self.ctx.ipc.status.value
                if game_status < 0:
                    logger.info(f"Connected but playing a different game")
                elif game_status == 0:
                    logger.info(f"Disconnected from PCSX2")
                else:
                    logger.info(f"Playing .hack//INFECTION")


class InfectionContext(SuperContext):
    # Archipelago Meta
    client_version: str = APConsole.Info.client_ver.value
    world_version: str = APConsole.Info.world_ver.value

    # Game Details
    game: str = Meta.game.value
    platform: str = Meta.platform.value
    items_handling: int = 0b111

    # Client Properties
    command_processor: InfectionCommandProcessor
    tags: set[str] = {"AP"}

    # Interface Properties
    ipc: InfectionInterface = InfectionInterface
    is_game_connected: bool = bool(ConnectionStatus.DISCONNECTED.value)
    has_just_connected: bool = False
    interface_sync_task: asyncio.tasks = None
    last_message: Optional[str] = None

    pending_resync: bool = True

    # Server Properties
    next_item_slot: int = -1

    # APWorld Properties
    locations_name_to_id: dict[str, int] = Locations.generate_name_to_id()
    items_name_to_id: dict[str, int] = Items.generate_name_to_id()

    # Session Properties
    unlocked_word_lists: List[int] = [0x0e, 0x0f]
    obtained_word_lists: List[int] = [0x0e, 0x0f]
    unlocked_party_members: List[PartyMembers] = [PartyMembers.BlackRose, PartyMembers.Orca, PartyMembers.Mia]
    unlocked_servers: List[Server] = [Server.Delta]
    unlocked_words: List[AreaWords] = []

    are_item_status_synced: bool = False

    # Local Session Save Properties
    last_item_processed_index = -1

    # Player Set Settings
    settings: InfectionSettings

    def __init__(self, address: str, password: str | None = None,):
        super().__init__(address, password)
        self.ipc = InfectionInterface(logger)
        Utils.init_logging(APConsole.Info.client_name_clean.value + self.client_version)
        self.settings = get_settings().get("dot_hack_infection_options", False)

    # Archipelago Server Authentication
    async def server_auth(self, password_requested: bool = False) -> None:
        # Ask for password if requested
        if password_requested and not self.password:
            await super(InfectionContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict) -> None:
        super().on_package(cmd, args)
        if cmd == APHelper.cmd_conn.value:
            data = args[APHelper.arg_sl_dt.value]

            if APHelper.version.value in data:
                world_ver: str = data[APHelper.version.value]
                assert_version_compatibility(
                    world_ver, APConsole.Info.world_ver.value)
            else:
                assert_version_compatibility(
                    "", APConsole.Info.world_ver.value)

        elif cmd == APHelper.cmd_rcv.value:
            index = args["index"]

            if not self.checked_locations:
                self.are_item_status_synced = True

            if self.are_item_status_synced or not self.items_received:
                return

        elif cmd == APHelper.cmd_rminfo.value:
            seed: str = args[APHelper.arg_seed.value]

            if self.seed_name is not seed:
                self.checked_locations.clear()
                self.locations_checked.clear()

                self.seed_name = seed

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        if not self.death_link:
            return

        super().on_deathlink(data)
        self.pending_deathlinks += 1

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = APConsole.Info.game_name.value
        ui.logging_pairs = [("Client", "Archipelago")]
        return ui

    async def goal(self):
        if self.game_goaled:
            return
        await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        self.game_goaled = True


def update_connection_status(ctx: InfectionContext, status: bool):
    if bool(ctx.is_game_connected) == status:
        return

    if status:
        ctx.has_just_connected = True
        logger.info(APConsole.Info.init_game.value)
    else:
        logger.info(APConsole.Err.sock_fail.value +
                    APConsole.Err.sock_re.value)

    ctx.is_game_connected = status


async def main_sync_task(ctx: InfectionContext):
    ctx.ipc.connect_game()

    while not ctx.exit_event.is_set():
        try:
            # Check connection to PCSX2 first
            is_game_connected: bool = ctx.ipc.get_connection_state()
            update_connection_status(ctx, is_game_connected)

            # Check Progress if connection is good
            if is_game_connected:
                status = ctx.ipc.get_ingame_status()
                if status is None:
                    await asyncio.sleep(3)
                    continue
                await check_game(ctx)

            # Attempt reconnection to PCSX2 otherwise
            else:
                await reconnect_game(ctx)

        except ConnectionError:
            ctx.ipc.disconnect_game()
        except Exception as e:
            if isinstance(e, RuntimeError):
                logger.error(str(e))
            else:
                logger.error(traceback.format_exc())

            await asyncio.sleep(3)
            continue


async def check_game(ctx: InfectionContext):
    """Check game progress, send deathlink updates, and update connection status"""

    if ctx.server:
        ctx.last_message = None
        if not ctx.slot:
            await asyncio.sleep(1)
            return
        if ctx.last_item_processed_index < 0:
            ctx.last_item_processed_index = ctx.ipc.get_last_item_index()

        ctx.ipc.initial_state()

        await ctx.ipc.check_locations(ctx)
        await ctx.ipc.receive_items(ctx)

        await ctx.ipc.scan_party_member(ctx)
        await ctx.ipc.scan_server(ctx)
        await ctx.ipc.scan_word_list(ctx)

        if ctx.has_just_connected or ctx.pending_resync:
            await ctx.ipc.resync_items(ctx)
            ctx.has_just_connected = False
            if ctx.pending_resync:
                logger.info("Resyncing complete")
                ctx.pending_resync = False
    else:
        message: str = APConsole.Info.p_init_g_sre.value
        if ctx.last_message is not message:
            logger.info(message)
            ctx.last_message = message
    await asyncio.sleep(1.5)
    return


async def reconnect_game(ctx: InfectionContext):
    ctx.ipc.connect_game()
    await asyncio.sleep(3)


def parse_version(version: str) -> list[str]:
    """
    Converts String of version into a list of attributes (Major.minor.patch-pre+build)

    We use a modified version of Semver for our purposes:
        > Major - Denotes a significant feature update and will not have backwards compatibility
            with any other major version.
        > Minor - Denotes a small feature update and will not have backwards compatibility with previous minor versions.
        > Patch - Denotes bug fixes with compatability with other versions of the same minor and major version.
        > Pre - Denotes a pre-release that is not compatible with any other pre-release version
            of the same Major and Minor version.
        > Build - Denotes a minor pre-release patch that is compatible with the same Major, Minor and Pre version.
    """

    if not str:
        return []

    ext: list[str] = [*version.split("+")]
    ext = [*ext[0].split("-"), *ext[1:]]
    ext = [*ext[0].split("."), *ext[1:]]

    if len(ext) == 4:
        ext.append("0")

    return ext


def compare_versions(subject: list[str], base: list[str]) -> int:
    if len(subject) < 3 or len(base) < 3 or len(subject) != len(base):
        return -2

    # Major Check
    if subject[0] != base[0]:
        return -1

    # Minor Check
    if subject[1] != base[1]:
        return -1

    # Pre Check
    if len(subject) >= len(base) > 3 and subject[3] != base[3]:
        return -1

    return 0


def assert_version_compatibility(subject: str, base: str):
    subject_ver: list[str] = parse_version(subject)
    base_ver: list[str] = parse_version(base)

    error: int = compare_versions(subject_ver, base_ver)

    if not error:
        return

    if error == -2:
        raise AssertionError(f"The world being connected to has been generated with an incompatible version of "
                             f".hack//INFECTION Archipelago. Connection Aborted.")

    elif error == -1:
        raise AssertionError(f"The world being connected to has been generated with a .hack//INFECTION Archipelago "
                             f"version that this client is not compatible with. Connection Aborted."
                             f"\nWorld version: {subject}\nClient version: {base}")


async def main():
    multiprocessing.freeze_support()

    # # Parse command line
    parser: ArgumentParser = get_base_parser()
    args: Namespace = parser.parse_args()

    # Create game context
    ctx = InfectionContext(args.connect, args.password)

    # Archipelago Server Connections
    logger.info(APConsole.Info.p_init_s.value)
    ctx.server_task = asyncio.create_task(
        server_loop(ctx), name="Server Loop")

    if tracker_loaded:
        ctx.run_generator()
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    # Create Main Loop
    ctx.interface_sync_task = asyncio.create_task(
        main_sync_task(ctx), name="PCSX2 Sync")

    await ctx.exit_event.wait()
    ctx.server_address = None
    await ctx.shutdown()

    # Call Main Client Loop
    if ctx.interface_sync_task:
        await asyncio.sleep(3)
        await ctx.interface_sync_task


def launch():
    # Run Client
    import colorama

    colorama.init()
    asyncio.run(main())
    colorama.deinit()


# Ensure file will only run as the main file
if __name__ == "__main__":
    launch()
