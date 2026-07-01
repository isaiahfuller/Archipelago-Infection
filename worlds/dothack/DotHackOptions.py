from dataclasses import dataclass

from Options import OptionGroup, Toggle, Choice, PerGameCommonOptions, DeathLink, Range
from .data.Strings import APHelper


class Volume(Choice):
    """
    Choose the volume of the game.
    Default: 1
    """
    display_name = "Volume"
    option_infection = 1
    default = 1


class KiteClass(Choice):
    """
        Choose the main character's class.
        Default: Twin Blade
        """
    display_name = "Kite's Class"
    option_twin_blade = 0
    option_blademaster = 1
    option_heavy_blade = 2
    option_heavy_axeman = 3
    option_long_arm = 4
    option_wavemaster = 5
    default = 0


class CompletionCondition(Choice):
    """
    Choose the completion condition for the game.
    Default: Defeat Skeith
    """
    display_name = "Completion Condition"
    option_defeat_skeith = 0
    option_defeat_parasite_dragon = 1
    default = 0

class MonsterHunt(Toggle):
    """
    Gain a check for each new monster you fight. NONFUNCTIONAL
    """
    display_name = "Monster Hunt"


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
    display_name = "Opened Portals"
    range_start = 0
    range_end = 100
    default = 100


class ClearedPortals(Range):
    """
    Include fully cleared dungeons/fields in the randomizer.
    Default: 10
    """
    display_name = "Cleared Dungeons and Fields"
    range_start = 0
    range_end = 30
    default = 10


class GottTreasures(Range):
    """
    Include Gott Treasures in the randomizer.
    Default: 10
    """
    display_name = "Gott Treasures"
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
    "Quest Options": [
        Volume,
        KiteClass,
        CompletionCondition,
        MonsterHunt
    ],
    "Quality of Life Options": [
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
    "Sync Options": [
        DeathLink,
    ],
}


@dataclass
class DotHackOptions(PerGameCommonOptions):
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
    volume: Volume
    kite_class: KiteClass
    monster_hunt: MonsterHunt


def create_option_groups() -> list[OptionGroup]:
    groups: list[OptionGroup] = []
    for group, options in infection_option_groups.items():
        groups.append(OptionGroup(group, options))
    return groups


def slot_data_options() -> list[str]:
    return [
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
        APHelper.volume.value,
        APHelper.kite_class.value,
        APHelper.monster_hunt.value,
    ]