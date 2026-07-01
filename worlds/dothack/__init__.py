from BaseClasses import LocationProgressType, ItemClassification
from typing import ClassVar, List, cast
import logging
import settings

from BaseClasses import MultiWorld, Tutorial, Location, Region
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, launch_subprocess, Type

from .data.Strings import APConsole, APHelper, Meta, AreaWordNames, CharacterNames, PlayStatNames, ServerNames
from .data import Locations, Items
from .data.Items import InfectionItem, InfectionItemMeta, ITEMS_MASTER
from .data.locations.WordList import InfectionDeltaWordList as DeltaWordList, get_wordlist_name
from .DotHackOptions import DotHackOptions, slot_data_options, create_option_groups
from .data.DataManager import VOLUME_DATA


# Identifier for Archipelago to recognize and run the client
def run_client():
    from .DotHackClient import launch
    launch_subprocess(launch, name="DotHackClient")


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

    automatically_read_emails: GamePreferences | bool = False
    completion_condition: GenerationPreferences | int = 0
    opened_portals: GenerationPreferences | int = 100
    cleared_portals: GenerationPreferences | int = 10
    gott_treasures: GenerationPreferences | int = 10
    volume: GenerationPreferences | int = 1


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


class DotHackWorld(World):
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
    game = str(Meta.game.value)
    settings: ClassVar[InfectionSettings]
    web: ClassVar[WebWorld] = InfectionWeb()
    topology_present = True

    # Initialize randomizer options
    options_dataclass = DotHackOptions
    options: DotHackOptions

    # Define the Items and Locations to/for Archipelago
    item_name_to_id = Items.generate_name_to_id()
    event_location_name_to_id: dict[str, int] = Locations.generate_event_name_to_id()
    playstat_location_name_to_id: dict[str, int] = Locations.generate_playstat_name_to_id()
    location_name_to_id: ClassVar[dict[str, int]] = {**event_location_name_to_id, **playstat_location_name_to_id}
    playstat_locations: list = []
    item_name_groups = Items.generate_item_groups()
    location_name_groups = Locations.generate_location_groups()

    logger: logging.Logger = logging.getLogger()

    def __init__(self, multiworld: MultiWorld, player: int):
        self.item_pool: List[InfectionItem] = []
        self.filler_items: List[InfectionItem] = []
        super(DotHackWorld, self).__init__(multiworld, player)

    def generate_early(self):
        ut_initialized: bool = self.prepare_ut
        if ut_initialized:
            return
        stats = {}
        stats[PlayStatNames.AreasVisited.name] = self.options.areas_visited.value
        stats[PlayStatNames.ChestsOpened.name] = self.options.chests.value
        stats[PlayStatNames.BreakablesBroken.name] = self.options.breakables.value
        stats[PlayStatNames.SymbolsActivated.name] = self.options.symbols_activated.value
        stats[PlayStatNames.TotalDataDrains.name] = self.options.data_drains.value
        stats[PlayStatNames.KiteLevel.name] = self.options.kite_levels.value
        stats[PlayStatNames.GottOpened.name] = self.options.gott_treasures.value
        stats[PlayStatNames.AllDungeonPortalsOpened.name] = self.options.cleared_portals.value
        stats[PlayStatNames.AllFieldPortalsOpened.name] = self.options.cleared_portals.value
        stats[PlayStatNames.PortalsOpened.name] = self.options.opened_portals.value
        self.playstat_locations = Locations.playstat_gen(stats)

    def create_regions(self):
        main_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(main_region)

        v_data = VOLUME_DATA[self.options.volume.value]

        for loc_meta in self.playstat_locations:
            main_region.locations.append(loc_meta.to_location(self.player, main_region))
        for loc_meta in v_data.event_locations:
            if loc_meta.event == Locations.CompletionConditions.SkeithDefeated and self.options.completion_condition == 1:
                loc_meta.progress_type = LocationProgressType.EXCLUDED
            if loc_meta.event == Locations.CompletionConditions.ParasiteDragonDefeated and self.options.completion_condition == 0:
                loc_meta.progress_type = LocationProgressType.EXCLUDED
            loc = loc_meta.to_location(self.player, main_region)
            main_region.locations.append(loc)
        for loc_meta in v_data.wordlist_locations:
            if loc_meta.wordlist == DeltaWordList.HideousSomeonesGiant and self.options.completion_condition == 0:
                loc_meta.progress_type = LocationProgressType.EXCLUDED
            loc = loc_meta.to_location(self.player, main_region)
            main_region.locations.append(loc)

        main_region.add_event("Victory")

    def create_item(self, item: str) -> InfectionItem:
        for itm in ITEMS_MASTER:
            if isinstance(itm, InfectionItemMeta):
                if itm.name == item:
                    return itm.to_item(self.player)
        raise ValueError(f"Could not create item '{item}'")

    def get_filler_item_name(self) -> str:
        return self.random.choice(self.filler_items).name

    def create_items(self):
        # Define items
        items = []
        starting_items = [
            ServerNames.Delta.value,
            # AreaWordNames.Bursting.value,
            # AreaWordNames.AquaField.value,
            # AreaWordNames.PassedOver.value,
            # AreaWordNames.Hidden.value,
            # AreaWordNames.Forbidden.value,
            # AreaWordNames.HolyGround.value,
            # CharacterNames.BlackRose.value,
            # CharacterNames.Orca.value,
            # get_wordlist_name(DeltaWordList.HiddenForbiddenHolyGround),
            # get_wordlist_name(DeltaWordList.BurstingPassedOverAquaField),
        ]
        for item_name in starting_items:
            item = self.create_item(item_name)
            self.multiworld.push_precollected(item)

        v_data = VOLUME_DATA[self.options.volume.value]

        for item in v_data.items:
            if item.name in starting_items:
                continue
            elif item.classification == ItemClassification.filler:
                self.filler_items.append(item.to_item(self.player))
            else:
                items.append(item.to_item(self.player))
        self.item_pool.extend(items)

        needed_filler = len(self.multiworld.get_unfilled_locations(self.player)) - len(self.item_pool)
        self.item_pool.extend(cast(list[InfectionItem], [self.create_filler() for _ in range(needed_filler)]))
        self.multiworld.itempool += self.item_pool

    def set_rules(self):
        match(self.options.volume.value):
            case 1:
                from .Rules import infection_rules as set_rules
        set_rules(self)

    @property
    def prepare_ut(self):
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        is_in_ut: bool = bool(re_gen_passthrough and self.game in re_gen_passthrough)
        if is_in_ut:
            slot_data = re_gen_passthrough[self.game]
            self.options.automatically_read_emails.value = slot_data.get(APHelper.automatically_read_emails.value, [])
            stats = {}
            self.options.monster_hunt = slot_data.get(APHelper.monster_hunt.value, [] )
            self.options.kite_class.value = slot_data.get(APHelper.kite_class.value, [])
            stats[PlayStatNames.AreasVisited.name] = self.options.areas_visited.value
            stats[PlayStatNames.ChestsOpened.name] = self.options.chests.value
            stats[PlayStatNames.BreakablesBroken.name] = self.options.breakables.value
            stats[PlayStatNames.SymbolsActivated.name] = self.options.symbols_activated.value
            stats[PlayStatNames.TotalDataDrains.name] = self.options.data_drains.value
            stats[PlayStatNames.KiteLevel.name] = self.options.kite_levels.value
            stats[PlayStatNames.GottOpened.name] = self.options.gott_treasures.value
            stats[PlayStatNames.AllDungeonPortalsOpened.name] = self.options.cleared_portals.value
            stats[PlayStatNames.AllFieldPortalsOpened.name] = self.options.cleared_portals.value
            stats[PlayStatNames.PortalsOpened.name] = self.options.opened_portals.value
            stats[PlayStatNames.MonsterHuntInfection.name] = self.options.monster_hunt.value
            self.playstat_locations = Locations.playstat_gen(stats)
        return is_in_ut

    def fill_slot_data(self):
        slot_data: dict = self.options.as_dict(*slot_data_options())
        slot_data[APHelper.version.value] = APConsole.Info.world_ver.value
        return slot_data

    def generate_output(self, directory: str):
        datas = {
            "slot_data": self.fill_slot_data()
        }
