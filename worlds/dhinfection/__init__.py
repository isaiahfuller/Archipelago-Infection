from BaseClasses import ItemClassification
from worlds.dhinfection.data.Locations import InfectionLocation
from copy import deepcopy
from typing import ClassVar, List, Optional, TextIO
import logging

from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, launch_subprocess, Type
from worlds.generic.Rules import add_rule, set_rule
from BaseClasses import MultiWorld, Tutorial, Location, Region
from .data.Strings import APConsole, Meta, InfectionEventNames as Ev, InfectionAreaWordNames as AreaWordNames, InfectionCharacterNames as CharacterNames, InfectionPlayStatNames as PlayStatNames, InfectionServerNames as ServerNames
from .InfectionOptions import create_option_groups
from .data import Locations, Items
from .data.Items import InfectionItem, InfectionItemMeta, ITEMS_MASTER
from .data.Locations import EventLocations, WordListLocations, RyuBookI, RyuBookII, RyuBookVI, RyuBookVII, OtherStats, CharacterLevels
from .data.items.PartyMembers import InfectionPartyMembers as PartyMembers
from .data.items.AreaWords import InfectionAreaWords as AreaWords
from .data.items.Servers import InfectionServers as Servers
from .data.locations.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList, get_wordlist_name
from .InfectionOptions import InfectionOptions
import settings


# Identifier ffor Archipelago to recognize and run the client
def run_client():
    from .InfectionClient import launch
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
    game = Meta.game.value
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
        main_region = Region("Menu", self.player, self.multiworld)
        # self.multiworld.regions.append(menu_region)

        # main_region = Region("Main", self.player, self.multiworld)
        self.multiworld.regions.append(main_region)
        main_region.add_locations(self.location_name_to_id, InfectionLocation)
        main_region.add_event(Ev.InfectionBeat.value)
        # for wl in WordListLocations:
        #     main_region.add_event(wl.name)
        #     words = [AreaWordNames[w.name].value for w in wl.wordlist.value["words"]]
        #     add_rule(self.multiworld.get_location(wl.name, self.player), lambda state: all(state.has(word, self.player) for word in words))
                


    def create_item(self, item: str) -> InfectionItem:
        for itm in ITEMS_MASTER:
            if isinstance(itm, InfectionItemMeta):
                if itm.name == item:
                    return itm.to_item(self.player)
        return None

    def create_items(self):
        # Define items
        items = []
        starting_items = [
            Servers.Delta.name,
            AreaWordNames.Bursting.value,
            AreaWordNames.AquaField.value,
            AreaWordNames.PassedOver.value,
            AreaWordNames.Hidden.value,
            AreaWordNames.Forbidden.value,
            AreaWordNames.HolyGround.value,
            CharacterNames.BlackRose.value,
            CharacterNames.Orca.value,
            get_wordlist_name(DeltaWordList.HiddenForbiddenHolyGround),
            get_wordlist_name(DeltaWordList.BurstingPassedOverAquaField),
        ]
        for item in ITEMS_MASTER:
            if item.name in starting_items:
                continue
            else:
                items.append(item.to_item(self.player))
        self.item_pool.extend(items)
        self.multiworld.itempool += self.item_pool

    def set_list_rules(self, location, wordlist):
        # words = [AreaWordNames[w.name].value for w in wordlist.value["words"]]
        # add_rule(self.multiworld.get_location(location, self.player), lambda state: all(state.has(word, self.player) for word in words))
        add_rule(self.multiworld.get_location(location, self.player), lambda state: state.has(get_wordlist_name(wordlist), self.player))
        return

    def set_stats_rules(self, stats):
        for i in range(len(stats)-1):
            if stats[1-i].name.split('-')[0] != stats[1-(i+1)].name.split('-')[0]:
                continue
            # print(stats[1-i].name, stats[1-(i+1)].name)
            add_rule(self.multiworld.get_location(stats[1-i].name, self.player), lambda state: state.can_reach_location(stats[1-(i+1)].name, self.player))

    def set_rules(self):
        self.set_stats_rules(CharacterLevels)
        self.set_stats_rules(OtherStats)
        self.set_stats_rules(RyuBookI)
        self.set_stats_rules(RyuBookII)
        self.set_stats_rules(RyuBookVI)
        self.set_stats_rules(RyuBookVII)
        
        # Set completion condition
        self.multiworld.completion_condition[self.player] = lambda state: state.has(Ev.InfectionBeat.value, self.player)
        add_rule(self.multiworld.get_location(Ev.ParasiteDragon.value, self.player), lambda state: state.has(Ev.InfectionBeat.value, self.player))

        # Story missions
        self.set_list_rules(Ev.FirstDataBug.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        
        self.set_list_rules(Ev.LearnGateHacking.value, DeltaWordList.BoundlessCorruptedFortWalls)
        add_rule(self.multiworld.get_location(Ev.LearnGateHacking.value, self.player), lambda state: state.can_reach_location(Ev.FirstDataBug.value, self.player))

        self.set_list_rules(Ev.SavedPiros.value, DeltaWordList.IndiscreetGluttonousPilgrimage)
        add_rule(self.multiworld.get_location(Ev.SavedPiros.value, self.player), lambda state: state.can_reach_location(Ev.LearnGateHacking.value, self.player))
            
        self.set_list_rules(Ev.BoardProtected.value, DeltaWordList.ClosedObliviousTwinHills)
        add_rule(self.multiworld.get_location(Ev.BoardProtected.value, self.player), lambda state: state.has(CharacterNames.Mia.value, self.player) and state.has(CharacterNames.Elk.value, self.player))
        add_rule(self.multiworld.get_location(Ev.BoardProtected.value, self.player), lambda state: state.can_reach_location(Ev.SavedPiros.value, self.player))
        add_rule(self.multiworld.get_location(Ev.BoardProtected.value, self.player), lambda state: state.can_reach_location(PlayStatNames.KiteLevel.value + "5", self.player))


        self.set_list_rules(Ev.BlackRoseDungeon.value, ThetaWordList.CollapsedMomentarySpiral)
        # add_rule(self.multiworld.get_location(Ev.BlackRoseDungeon.value, self.player), lambda state: state.has(CharacterNames.BlackRose.value, self.player))
        add_rule(self.multiworld.get_location(Ev.BlackRoseDungeon.value, self.player), lambda state: state.can_reach_location(Ev.BoardProtected.value, self.player))
        add_rule(self.multiworld.get_location(Ev.BlackRoseDungeon.value, self.player), lambda state: state.has(ServerNames.Theta.value, self.player))
        add_rule(self.multiworld.get_location(Ev.BlackRoseDungeon.value, self.player), lambda state: state.can_reach_location(PlayStatNames.KiteLevel.value + "15", self.player))

        self.set_list_rules(Ev.ElkMiaFavorite.value, DeltaWordList.PlenteousSmilingHypha)
        add_rule(self.multiworld.get_location(Ev.ElkMiaFavorite.value, self.player), lambda state: state.has(CharacterNames.Elk.value, self.player) and state.has(CharacterNames.Mia.value, self.player))
        add_rule(self.multiworld.get_location(Ev.ElkMiaFavorite.value, self.player), lambda state: state.can_reach_location(Ev.BlackRoseDungeon.value, self.player))

        self.set_list_rules(Ev.PirosDiary.value, DeltaWordList.PutridHotbloodedScaffold)
        add_rule(self.multiworld.get_location(Ev.PirosDiary.value, self.player), lambda state: state.has(CharacterNames.Piros.value, self.player))
        add_rule(self.multiworld.get_location(Ev.PirosDiary.value, self.player), lambda state: state.can_reach_location(Ev.ElkMiaFavorite.value, self.player))

        self.set_list_rules(Ev.MistralMeetUp.value, ThetaWordList.CollapsedMomentarySpiral)
        add_rule(self.multiworld.get_location(Ev.MistralMeetUp.value, self.player), lambda state: state.has(CharacterNames.Mistral.value, self.player))
        add_rule(self.multiworld.get_location(Ev.MistralMeetUp.value, self.player), lambda state: state.can_reach_location(Ev.PirosDiary.value, self.player))

        self.set_list_rules(Ev.Epitaph00.value, ThetaWordList.CursedDespairedParadise)
        add_rule(self.multiworld.get_location(Ev.Epitaph00.value, self.player), lambda state: state.can_reach_location(Ev.MistralMeetUp.value, self.player))

        self.set_list_rules(Ev.DescendentsOfFianna.value, DeltaWordList.BuriedPaganFierySands)
        add_rule(self.multiworld.get_location(Ev.DescendentsOfFianna.value, self.player), lambda state: state.can_reach_location(Ev.Epitaph00.value, self.player))

        self.set_list_rules(Ev.EpitaphQ.value, DeltaWordList.LonelySilentGreatSeal)
        add_rule(self.multiworld.get_location(Ev.EpitaphQ.value, self.player), lambda state: state.can_reach_location(Ev.DescendentsOfFianna.value, self.player))

        self.set_list_rules(Ev.MeetAlf.value, ThetaWordList.GreatDistantFertileLand)
        add_rule(self.multiworld.get_location(Ev.MeetAlf.value, self.player), lambda state: state.can_reach_location(Ev.EpitaphQ.value, self.player))

        self.set_list_rules(Ev.InfectionBeat.value, ThetaWordList.ChosenHopelessNothingness)
        add_rule(self.multiworld.get_location(Ev.InfectionBeat.value, self.player), lambda state: state.can_reach_location(Ev.MeetAlf.value, self.player))
        add_rule(self.multiworld.get_location(Ev.InfectionBeat.value, self.player), lambda state: state.can_reach_location(PlayStatNames.KiteLevel.value + "20", self.player))

        # Gardenia's quest
        self.set_list_rules(Ev.GracefulBook.value, ThetaWordList.BeautifulSomeonesTreasureGem)
        add_rule(self.multiworld.get_location(Ev.GracefulBook.value, self.player), lambda state: state.has(CharacterNames.Gardenia.value, self.player))

        # Golden Goblin quest
        self.set_list_rules(Ev.Stehony.value, DeltaWordList.DetestableGoldenSunnyDemon)

        self.set_list_rules(Ev.Jonue.value, DeltaWordList.DetestableGoldenMessenger)
        add_rule(self.multiworld.get_location(Ev.Jonue.value, self.player), lambda state: state.can_reach_location(Ev.Stehony.value, self.player))
        add_rule(self.multiworld.get_location(Ev.Jonue.value, self.player), lambda state: state.can_reach_location(Ev.BoardProtected.value, self.player))

        self.set_list_rules(Ev.Zyan.value, DeltaWordList.DetestableGoldenScent)
        add_rule(self.multiworld.get_location(Ev.Zyan.value, self.player), lambda state: state.can_reach_location(Ev.Jonue.value, self.player))
        add_rule(self.multiworld.get_location(Ev.Zyan.value, self.player), lambda state: state.can_reach_location(Ev.ElkMiaFavorite.value, self.player))

        self.set_list_rules(Ev.Albert.value, DeltaWordList.DetestableGoldenNewTruth)
        add_rule(self.multiworld.get_location(Ev.Albert.value, self.player), lambda state: state.can_reach_location(Ev.Zyan.value, self.player))
        add_rule(self.multiworld.get_location(Ev.Albert.value, self.player), lambda state: state.can_reach_location(Ev.MistralMeetUp.value, self.player))

        self.set_list_rules(Ev.Martina.value, DeltaWordList.DetestableGoldenGate)
        add_rule(self.multiworld.get_location(Ev.Martina.value, self.player), lambda state: state.can_reach_location(Ev.Albert.value, self.player))
        add_rule(self.multiworld.get_location(Ev.Martina.value, self.player), lambda state: state.can_reach_location(Ev.InfectionBeat.value, self.player))

    def pre_fill(self):
        from BaseClasses import CollectionState
        state = CollectionState(self.multiworld)
        # state.add_item(Servers.Delta.name, self.player)
        # state.add_item(AreaWordNames.Bursting.value, self.player)
        # state.add_item(AreaWordNames.AquaField.value, self.player)
        # state.add_item(AreaWordNames.PassedOver.value, self.player)
        # state.add_item(AreaWordNames.Hidden.value, self.player)
        # state.add_item(AreaWordNames.Forbidden.value, self.player)
        # state.add_item(AreaWordNames.HolyGround.value, self.player)
        # state.add_item(CharacterNames.BlackRose.value, self.player)
        # state.add_item(CharacterNames.Orca.value, self.player)
        # state.add_item(get_wordlist_name(DeltaWordList.HiddenForbiddenHolyGround), self.player)
        # state.add_item(get_wordlist_name(DeltaWordList.BurstingPassedOverAquaField), self.player)
        
    def prepare_ut(self):
        return False