from copy import deepcopy
from typing import ClassVar, List, Optional, TextIO
import logging

from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, launch_subprocess, Type
from BaseClasses import MultiWorld, Tutorial, Location
from .data.Strings import APConsole, Meta
from .InfectionOptions import create_option_groups
from .data import Locations, Items
from .data.Items import InfectionItem, InfectionItemMeta, ITEMS_MASTER
from .data.Locations import EventLocations
import settings


# Identifier ffor Archipelago to recognize and run the client
def run_client():
    from InfectionClient import launch
    launch_subprocess(launch, name="InfectionClient")


components.append(Component(APConsole.Info.client_name.value,
                  func=run_client, component_type=Type.CLIENT))


class InfectionSettings(settings.Group):
    class SessionPreferences(settings.Bool):
        """
        Preferences for game session management.

        > save_state_on_room_transition: Automatically create a save state when transitioning between rooms.
        > save_state_on_item_received: Automatically create a save state when receiving a new progressive item.
        > save_state_on_location_check: Automatically create a save state when checking a new location.
        > load_state_on_connect: Load a state automatically after connecting to the multiworld if the client
        is already connected to the game and that the last save is from a save state and not a normal game save.
        """

    class SessionsPreferences(settings.Bool):
        """"""

    class GamePreferences(settings.Bool):
        """
        Preferences for game/client-enforcement behavior

        > auto-equip : Automatically assign received gadgets to a face button
        """

    class GenerationPreferences(settings.Bool):
        """
        Preferences for game generation. Only relevant for world generation and not the setup of or during play.
        """

        def __len__(self):
            return len(self)

        def __getitem__(self, index):
            return self[index]

    class GenerationPreference(settings.Bool):
        """"""

        def __len__(self):
            return len(self)

        def __getitem__(self, index):
            return self[index]

    save_state_on_room_transition: SessionPreferences | bool = False
    save_state_on_item_received: SessionsPreferences | bool = True
    save_state_on_location_check: SessionsPreferences | bool = False
    load_state_on_connect: SessionsPreferences | bool = False

    auto_equip: GamePreferences | bool = True


class InfectionWeb(WebWorld):
    theme = "ocean"
    option_groups = create_option_groups()

    tutorials = [Tutorial(
        "Multiworld Guide Setup",
        " - A guide to setting up .hack//INFECTION for Archipelago",
        "English",
        "setup.md",
        "setup/en",
        ["isaiahfuller"]
    )]


class InfectionWorld(World):
    """
    .hack (/dɒt hæk/) is a series of single-player action role-playing video 
    games developed by CyberConnect2 and published by Bandai for the PlayStation 2. 
    The four games, .hack//Infection, .hack//Mutation, .hack//Outbreak, and .hack//Quarantine, 
    all feature a "game within a game", a fictional massively multiplayer online role-playing 
    game (MMORPG) called The World which does not require the player to connect to the Internet. 
    Players may transfer their characters and data between games in the series. Each game comes 
    with an extra DVD containing an episode of .hack//Liminality, the accompanying original 
    video animation (OVA) series which details fictional events that occur concurrently with the games.
    """
    # Define basic game parameters
    game = Meta.game
    settings: InfectionSettings
    web: ClassVar[WebWorld] = InfectionWeb()
    topology_present = True

    # Initialize randomizer options
    options_dataclass = InfectionOptions
    options: InfectionOptions

    # Define the Items and Locations to/for Archipelago
    item_name_to_id = Items.generate_name_to_id()
    location_name_to_id = Locations.generate_name_to_id()

    item_name_groups = Items.generate_item_groups()
    location_name_groups = Locations.generate_location_groups()

    logger: logging.Logger = logging.getLogger()

    def __init__(self, multiworld: MultiWorld, player: int):
        self.item_pool: List[InfectionItem] = []
        super(InfectionWorld, self).__init__(multiworld, player)

    def generate_early(self):
        ut_initialized: bool = self.prepare_ut()
        if ut_initialized:
            return

    def create_regions(self):
        create_regions(self)

    def create_item(self, item: str) -> InfectionItem:
        for itm in ITEMS_MASTER:
            if isinstance(itm, InfectionItemMeta):
                if itm.name == item:
                    return itm.to_item(self.player)
        return None

    def create_items(self):
        # Define items
        items = []
        for item in ITEMS_MASTER:
            items.append(item.to_item(self.player))
        self.item_pool.extend(items)
