from typing import Sequence
from dataclasses import dataclass
from abc import ABC
import copy

from BaseClasses import Location

from .locations.Events import InfectionStoryEvents, InfectionGoldenGoblins, InfectionOptionalPartyMembers, InfectionOtherSideQuests
from .locations.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList, ADDRESS as WordListAddress, InfectionWordListBase
from .Strings import Meta, InfectionAreaWordNames as AreaWordNames, InfectionEventNames as EventNames


class InfectionLocation(Location):
    game: str = Meta.game.value


class InfectionLocationMeta(ABC):
    name: str
    location_id: int
    address: int


class InfectionWordListLocation(InfectionLocationMeta):
    wordlist: InfectionWordListBase
    address: int = WordListAddress

    def __init__(self, wordlist: InfectionWordListBase) -> InfectionLocation:
        self.name = wordlist.name
        self.location_id = wordlist.value["address"]
        self.wordlist = wordlist

    def to_location(self, player: int) -> Location:
        return Location(player, self.name, self.location_id + self.address, parent)


class InfectionEventLocation(InfectionLocationMeta):
    event: InfectionStoryEvents
    bitflags: int

    def __init__(self, name: str, location_id: int, event, bitflags: int) -> InfectionLocation:
        self.name = name
        self.location_id = location_id
        self.event = event
        self.bitflags = bitflags

    def to_location(self, player: int) -> Location:
        return Location(player, self.name, self.location_id + self.address, parent)


def wordlist_gen(enum) -> list[InfectionWordListLocation]:
    res = []
    for wordlist in enum:
        # words = []
        # for word in wordlist.value["words"]:
        #     words.append(AreaWordNames[word.name].value)
        # name = " ".join(words)
        res.append(InfectionWordListLocation(
            wordlist
        ))
    return res


def event_gen(enum) -> list[InfectionEventLocation]:
    res = []
    for event in enum:
        name = EventNames[event.name].value
        res.append(InfectionEventLocation(
            name=name,
            location_id=event.value["address"],
            event=event,
            bitflags=event.value["bits"]
        ))
    return res


DeltaListLocations = wordlist_gen(DeltaWordList)
ThetaListLocations = wordlist_gen(ThetaWordList)


StoryEvents: InfectionEventLocation = event_gen(InfectionStoryEvents)
GoldenGoblins: InfectionEventLocation = event_gen(InfectionGoldenGoblins)
SideQuests: InfectionEventLocation = event_gen(InfectionOtherSideQuests)
OptionalPartyMembers: InfectionEventLocation = event_gen(
    InfectionOptionalPartyMembers)

WordListLocations: InfectionWordListLocation = [
    *DeltaListLocations,
    *ThetaListLocations
]

EventLocations: InfectionEventLocation = [
    *StoryEvents,
    *GoldenGoblins,
    *SideQuests,
    *OptionalPartyMembers
]

def generate_name_to_id() -> dict[str, int]:
    name_to_id: dict[str, int] = {wl.name: wl.location_id for wl in WordListLocations}
    name_to_id.update({el.name: el.location_id for el in EventLocations})
    return name_to_id


def generate_location_groups() -> dict[str, int]:
    groups: dict[str: set[str]] = {}

    groups.update({
        "Story Events": {el.name: el.location_id for el in StoryEvents},
        "Golden Goblins": {el.name: el.location_id for el in GoldenGoblins},
        "Side Quests": {el.name: el.location_id for el in SideQuests},
        "Optional Party Members": {el.name: el.location_id for el in OptionalPartyMembers},
        "Word List Locations": {wl.name: wl.location_id for wl in WordListLocations}
    })
    return groups
