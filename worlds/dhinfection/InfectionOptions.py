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


class IncludeSideQuests(Toggle):
    """
    Include side quests in the randomizer.
    Default: Disabled
    """
    display_name = "Include Side Quests"


class AutomaticallyReadEmails(Toggle):
    """
    Automatically read emails.
    Default: Disabled
    """
    display_name = "Automatically Read Emails"


infection_option_groups: dict[str, list] = {
    "Sync Options": [DeathLink],
    "Preferences": [AlwaysOnlinePartyMembers,
                    IncludeSideQuests,
                    AutomaticallyReadEmails]
}


@dataclass
class InfectionOptions(PerGameCommonOptions):
    always_online_party_members: AlwaysOnlinePartyMembers
    include_side_quests: IncludeSideQuests
    automatically_read_emails: AutomaticallyReadEmails


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
    ]
