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


infection_option_groups: dict[str, list] = {
    "Sync Options": [DeathLink],
    "Preferences": [AlwaysOnlinePartyMembers]
}


@dataclass
class InfectionOptions(PerGameCommonOptions):
    always_online_party_members: AlwaysOnlinePartyMembers


def create_option_groups() -> list[OptionGroup]:
    groups: list[OptionGroup] = []
    for group, options in infection_option_groups.items():
        groups.append(OptionGroup(group, options))
    return groups
