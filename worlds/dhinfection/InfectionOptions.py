from dataclasses import dataclass
from typing import Iterable, Any

from Options import OptionGroup, Toggle, DefaultOnToggle, Choice, PerGameCommonOptions, DeathLink, Visibility, \
    Range, OptionList, OptionSet, NamedRange
from .data.Strings import APHelper


class AlwaysOnlinePartyMembers(Toggle):
    """
    Choose if party members should always be available.
    Default: Disabled
    """
    display_name = "Always Online Party Members"


class CompletionCondition(Choice):
    """
    Choose the completion condition for the game.
    Default: Defeat Skeith
    """
    display_name = "Completion Condition"
    option_defeat_skeith = 0
    option_defeat_parasite_dragon = 1
    default = 0


class IncludeSideQuests(Toggle):
    """
    Include side quests (Golden Goblins, Parasite Dragon, and party members incl. Gardenia's quest) in the randomizer.
    Default: Disabled
    """
    display_name = "Include Side Quests"


class AutomaticallyReadEmails(Toggle):
    """
    Automatically read emails.
    Default: Disabled
    """
    display_name = "Automatically Read Emails"


class OpenedPortals(Range):
    """
    Include opened dungeon/field portals in the randomizer.
    Default: 100
    """
    display_name = "Include Opened Portals"
    range_start = 0
    range_end = 100
    default = 100


class ClearedPortals(Range):
    """
    Include fully cleared dungeons/fields in the randomizer.
    Default: 10
    """
    display_name = "Include Cleared Dungeons and Fields"
    range_start = 0
    range_end = 30
    default = 10


class GottTreasures(Range):
    """
    Include Gott Treasures in the randomizer.
    Default: 10
    """
    display_name = "Include Gott Treasures"
    range_start = 0
    range_end = 30
    default = 10


class AreasVisited(Range):
    """
    Include areas visited in the randomizer.
    Default: 10
    """
    display_name = "Areas Visited"
    range_start = 0
    range_end = 30
    default = 10


class Chests(Range):
    """
    Include chests in the randomizer.
    Default: 200
    """
    display_name = "Chests"
    range_start = 0
    range_end = 400
    default = 200


class Breakables(Range):
    """
    Include breakable items in the randomizer.
    Default: 200
    """
    display_name = "Breakables"
    range_start = 0
    range_end = 400
    default = 200


class SymbolsActivated(Range):
    """
    Include symbols activated in the randomizer.
    Default: 10
    """
    display_name = "Symbols Activated"
    range_start = 0
    range_end = 30
    default = 10


class DataDrains(Range):
    """
    Include data drains in the randomizer.
    Default: 30
    """
    display_name = "Data Drains"
    range_start = 0
    range_end = 100
    default = 30


class KiteLevels(Range):
    """
    Include Kite's level in the randomizer.
    Default: 25
    """
    display_name = "Kite Levels"
    range_start = 20
    range_end = 30
    default = 25


infection_option_groups: dict[str, list] = {
    "Sync Options": [
        DeathLink,
    ],
    "Quest Options": [
        IncludeSideQuests,
        CompletionCondition,
    ],
    "Quality of Life Options": [
        AlwaysOnlinePartyMembers,
        AutomaticallyReadEmails,
    ],
    "Ryu Book Options": [
        AreasVisited,
        OpenedPortals,
        ClearedPortals,
        GottTreasures,
        Chests,
        Breakables,
        SymbolsActivated,
        DataDrains,
        KiteLevels,
    ],
}


@dataclass
class InfectionOptions(PerGameCommonOptions):
    always_online_party_members: AlwaysOnlinePartyMembers
    include_side_quests: IncludeSideQuests
    automatically_read_emails: AutomaticallyReadEmails
    completion_condition: CompletionCondition
    opened_portals: OpenedPortals
    cleared_portals: ClearedPortals
    gott_treasures: GottTreasures
    areas_visited: AreasVisited
    chests: Chests
    breakables: Breakables
    symbols_activated: SymbolsActivated
    data_drains: DataDrains
    kite_levels: KiteLevels
    death_link: DeathLink


def create_option_groups() -> list[OptionGroup]:
    groups: list[OptionGroup] = []
    for group, options in infection_option_groups.items():
        groups.append(OptionGroup(group, options))
    return groups


def slot_data_options() -> list[str]:
    return [
        APHelper.always_online_party_members.value,
        APHelper.include_side_quests.value,
        APHelper.automatically_read_emails.value,
        APHelper.completion_condition.value,
        APHelper.opened_portals.value,
        APHelper.cleared_portals.value,
        APHelper.gott_treasures.value,
        APHelper.areas_visited.value,
        APHelper.chests.value,
        APHelper.breakables.value,
        APHelper.symbols_activated.value,
        APHelper.data_drains.value,
        APHelper.kite_levels.value,
        APHelper.death_link.value,
    ]
