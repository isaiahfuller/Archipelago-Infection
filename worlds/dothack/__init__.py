from worlds.dothack.data.items.RyuBooks import RyuBooks
from rule_builder.rules import Has
from BaseClasses import ItemClassification
from typing import ClassVar, List, cast
import logging
import settings

from BaseClasses import MultiWorld, Tutorial, Region
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, launch_subprocess, Type

from .data.Strings import APConsole, APHelper, Meta, PlayStatNames, ServerNames, ItemNames, CharacterNames
from .data import Locations, Items
from .data.Items import InfectionItem, InfectionItemMeta, ITEMS_MASTER
from .data.locations.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList, WordListBase, get_wordlist_name
from .data.locations.Events import InfectionEventBase, InfectionGoldenGoblins, InfectionOptionalPartyMembers
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
    golden_goblins: GenerationPreferences | bool = True
    optional_party_members: GenerationPreferences | bool = True
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
        delta_region = Region(ServerNames.Delta.value, self.player, self.multiworld)
        theta_region = Region(ServerNames.Theta.value, self.player, self.multiworld)

        ryu_book_i_region = Region(ItemNames.RyuBookI.value, self.player, self.multiworld)
        ryu_book_ii_region = Region(ItemNames.RyuBookII.value, self.player, self.multiworld)
        ryu_book_iv_region = Region(ItemNames.RyuBookIV.value, self.player, self.multiworld)
        ryu_book_vi_region = Region(ItemNames.RyuBookVI.value, self.player, self.multiworld)
        ryu_book_vii_region = Region(ItemNames.RyuBookVII.value, self.player, self.multiworld)
        
        self.multiworld.regions.append(main_region)
        self.multiworld.regions.append(delta_region)
        self.multiworld.regions.append(theta_region)
        self.multiworld.regions.append(ryu_book_i_region)
        self.multiworld.regions.append(ryu_book_ii_region)
        self.multiworld.regions.append(ryu_book_iv_region)
        self.multiworld.regions.append(ryu_book_vi_region)
        self.multiworld.regions.append(ryu_book_vii_region)

        main_region.connect(delta_region, ServerNames.Delta.value, rule=Has(ServerNames.Delta.value))
        main_region.connect(theta_region, ServerNames.Theta.value, rule=Has(ServerNames.Theta.value))
        main_region.connect(ryu_book_i_region, ItemNames.RyuBookI.value, rule=Has(ItemNames.RyuBookI.value))
        main_region.connect(ryu_book_ii_region, ItemNames.RyuBookII.value, rule=Has(ItemNames.RyuBookII.value))
        main_region.connect(ryu_book_iv_region, ItemNames.RyuBookIV.value, rule=Has(ItemNames.RyuBookIV.value))
        main_region.connect(ryu_book_vi_region, ItemNames.RyuBookVI.value, rule=Has(ItemNames.RyuBookVI.value))
        main_region.connect(ryu_book_vii_region, ItemNames.RyuBookVII.value, rule=Has(ItemNames.RyuBookVII.value))

        self.excluded_locations: set[int] = set()

        excluded_events: set[InfectionEventBase] = set()
        excluded_wordlist_locs: set[WordListBase] = set()

        if not self.options.golden_goblins.value:
            excluded_events.update(InfectionGoldenGoblins)
            excluded_wordlist_locs.update([
                DeltaWordList.DetestableGoldenSunnyDemon,
                DeltaWordList.DetestableGoldenMessenger,
                DeltaWordList.DetestableGoldenScent,
                DeltaWordList.DetestableGoldenNewTruth,
                DeltaWordList.DetestableGoldenGate
            ])
        if not self.options.optional_party_members.value:
            excluded_events.update(InfectionOptionalPartyMembers)
            excluded_wordlist_locs.update([
                DeltaWordList.RagingPassionateMelody,
                ThetaWordList.SoftSolitaryTriPansy,
                DeltaWordList.HideousDestroyersFarThunder,
                ThetaWordList.BeautifulSomeonesTreasureGem
            ])
        if self.options.completion_condition == 0:
            excluded_wordlist_locs.add(DeltaWordList.HideousSomeonesGiant)
            excluded_events.add(Locations.CompletionConditions.ParasiteDragonDefeated)
        if self.options.completion_condition == 1:
            # excluded_events.add(Locations.CompletionConditions.SkeithDefeated)
            pass

        self.logger.debug(f"Excluded Locations: {excluded_events}")
        self.logger.debug(f"Excluded Wordlists: {excluded_wordlist_locs}")

        v_data = VOLUME_DATA[self.options.volume.value]

        for loc_meta in self.playstat_locations:
            self.logger.debug(f"Adding Playstat Location: {loc_meta.stat}")
            if loc_meta.stat in RyuBooks.RyuBookI.value:
                ryu_book_i_region.locations.append(loc_meta.to_location(self.player, ryu_book_i_region))
            elif loc_meta.stat in RyuBooks.RyuBookII.value:
                ryu_book_ii_region.locations.append(loc_meta.to_location(self.player, ryu_book_ii_region))
            elif loc_meta.stat in RyuBooks.RyuBookIV.value:
                ryu_book_iv_region.locations.append(loc_meta.to_location(self.player, ryu_book_iv_region))
            elif loc_meta.stat in RyuBooks.RyuBookVI.value:
                ryu_book_vi_region.locations.append(loc_meta.to_location(self.player, ryu_book_vi_region))
            elif loc_meta.stat in RyuBooks.RyuBookVII.value:
                ryu_book_vii_region.locations.append(loc_meta.to_location(self.player, ryu_book_vii_region))
            else:
                main_region.locations.append(loc_meta.to_location(self.player, main_region))
        for loc_meta in v_data.event_locations:
            if loc_meta.event in excluded_events:
                self.logger.debug(f"Excluding Event Location: {loc_meta.name}")
                self.excluded_locations.add(loc_meta.location_id)
                continue
            loc = loc_meta.to_location(self.player, main_region)
            main_region.locations.append(loc)
        for loc_meta in v_data.wordlist_locations:
            if loc_meta.wordlist in excluded_wordlist_locs:
                self.logger.debug(f"Excluding Wordlist Location: {loc_meta.name}")
                self.excluded_locations.add(loc_meta.location_id)
                continue
            loc = loc_meta.to_location(self.player, main_region)
            if isinstance(loc_meta, DeltaWordList):
                delta_region.locations.append(loc)
            elif isinstance(loc_meta, ThetaWordList):
                theta_region.locations.append(loc)
            else:
                main_region.locations.append(loc)

        main_region.add_event("Victory")

    def create_item(self, item: str) -> InfectionItem:
        for itm in ITEMS_MASTER:
            if isinstance(itm, InfectionItemMeta):
                if itm.name == item:
                    return itm.to_item(self.player)
        raise ValueError(f"Could not create item '{item}'")

    def get_filler_item_name(self) -> str:
        res = self.random.choices(self.filler_items, weights=[item.weight for item in self.filler_items], k=1)
        self.logger.debug(f"Creating item: {res[0].name} ({res[0].weight})")
        return res[0].name if isinstance(res, list) else res.name

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
        excluded_items: set[str] = set(starting_items)

        if not self.options.golden_goblins.value:
            excluded_items.update([
                get_wordlist_name(DeltaWordList.DetestableGoldenSunnyDemon),
                get_wordlist_name(DeltaWordList.DetestableGoldenMessenger),
                get_wordlist_name(DeltaWordList.DetestableGoldenScent),
                get_wordlist_name(DeltaWordList.DetestableGoldenNewTruth),
                get_wordlist_name(DeltaWordList.DetestableGoldenGate),
            ])

        if not self.options.optional_party_members.value:
            excluded_items.update([
                get_wordlist_name(DeltaWordList.RagingPassionateMelody),
                get_wordlist_name(ThetaWordList.SoftSolitaryTriPansy),
                get_wordlist_name(DeltaWordList.HideousDestroyersFarThunder),
                get_wordlist_name(ThetaWordList.BeautifulSomeonesTreasureGem),
                CharacterNames.Sanjuro.value,
                CharacterNames.Gardenia.value,
                CharacterNames.Natsume.value,
            ])

        for item_name in starting_items:
            item = self.create_item(item_name)
            self.multiworld.push_precollected(item)

        v_data = VOLUME_DATA[self.options.volume.value]

        for item in v_data.items:
            if item.name in excluded_items:
                self.logger.debug(f"Excluding Item: {item.name}")
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
            self.options.monster_hunt = slot_data.get(APHelper.monster_hunt.value, [])
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
        slot_data[APHelper.excluded_locations.value] = self.excluded_locations
        return slot_data

    def generate_output(self, directory: str):
        datas = {
            "slot_data": self.fill_slot_data()
        }
