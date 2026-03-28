from BaseClasses import LocationProgressType
from typing import Sequence
from dataclasses import dataclass
from abc import ABC
import copy

from BaseClasses import Location

from .items.AreaWords import InfectionAreaWords as AreaWords, ADDRESS as AreaWordAddress
from .locations.Events import InfectionStoryEvents, InfectionGoldenGoblins, InfectionOptionalPartyMembers, InfectionOtherSideQuests
from .locations.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList, ADDRESS as WordListAddress, InfectionWordListBase, get_wordlist_name
from .locations.PlayStats import PlayStats
from .Strings import Meta, InfectionAreaWordNames as AreaWordNames, InfectionEventNames as EventNames, InfectionPlayStatNames as PlayStatNames


class InfectionLocation(Location):
    game: str = Meta.game.value


class InfectionLocationMeta(ABC):
    name: str
    location_id: int
    address: int

    def to_location(self, player: int, parent) -> InfectionLocation:
        loc = InfectionLocation(player, self.name, self.location_id, parent)
        loc.progress_type = getattr(self, "progress_type", LocationProgressType.DEFAULT)
        return loc


class InfectionAreaWordLocation(InfectionLocationMeta):
    word: AreaWords

    def __init__(self, word: AreaWords) -> InfectionLocation:
        self.name = AreaWordNames[word.name].value
        self.location_id = word.value["id"]*10 + AreaWordAddress
        self.word = word


class InfectionWordListLocation(InfectionLocationMeta):
    wordlist: InfectionWordListBase

    def __init__(self, wordlist: InfectionWordListBase) -> InfectionLocation:
        self.name = get_wordlist_name(wordlist)
        self.location_id = WordListAddress * 10 + wordlist.value["address"]
        self.wordlist = wordlist
        self.progress_type = LocationProgressType.DEFAULT


class InfectionEventLocation(InfectionLocationMeta):
    event: InfectionStoryEvents
    bitflags: int

    def __init__(self, name: str, location_id: int, event, bitflags: int) -> InfectionLocation:
        self.name = name
        self.location_id = location_id
        self.event = event
        self.bitflags = bitflags
        self.progress_type = LocationProgressType.PRIORITY


class InfectionPlayStatLocation(InfectionLocationMeta):
    stat: PlayStats

    def __init__(self, name: str, stat: PlayStats, progress: int, progress_type: LocationProgressType) -> InfectionLocation:
        self.name = name
        self.location_id = (stat.value["addr"] * 500) + progress
        self.stat = stat
        self.progress_type = progress_type


def area_word_gen(enum) -> list[InfectionAreaWordLocation]:
    res = []
    for word in enum:
        res.append(InfectionAreaWordLocation(
            word
        ))
    return res


def wordlist_gen(enum) -> list[InfectionWordListLocation]:
    res = []
    for wordlist in enum:
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


PlayStatLocsList: InfectionPlayStatLocation


def playstat_gen(stats: dict[str, int] | None = None) -> list[InfectionPlayStatLocation]:
    res = []
    if stats is None:
        stats = {
            PlayStatNames.AreasVisited.name: 30,
            PlayStatNames.KiteLevel.name: 30,
            PlayStatNames.PortalsOpened.name: 100,
            PlayStatNames.AllFieldPortalsOpened.name: 30,
            PlayStatNames.AllDungeonPortalsOpened.name: 30,
            PlayStatNames.GottOpened.name: 30,
            PlayStatNames.ChestsOpened.name: 400,
            PlayStatNames.BreakablesBroken.name: 400,
            PlayStatNames.SymbolsActivated.name: 30,
            PlayStatNames.TotalDataDrains.name: 100,
        }

    def append_stat(name: str, stat: PlayStats, progress: int, max_progress: int):
        progress_type = LocationProgressType.EXCLUDED if progress > max_progress else LocationProgressType.DEFAULT
        res.append(InfectionPlayStatLocation(
            name=name,
            stat=stat,
            progress=progress,
            progress_type=progress_type
        ))

    for name, value in stats.items():
        stat = PlayStats[name]
        name = PlayStatNames[name].value
        if stat.value["scale"] == "list":
            for i in stat.value["values"]:
                append_stat(name + str(i), stat, i, value)
        elif stat.value["scale"] == "range":
            for i in range(stat.value["values"][0], stat.value["values"][1]):
                append_stat(name + str(i), stat, i, value)
    return res


DeltaListLocations = wordlist_gen(DeltaWordList)
ThetaListLocations = wordlist_gen(ThetaWordList)
AreaWordLocations = area_word_gen(AreaWords)

StoryEvents: InfectionEventLocation = event_gen(InfectionStoryEvents)
GoldenGoblins: InfectionEventLocation = event_gen(InfectionGoldenGoblins)
SideQuests: InfectionEventLocation = event_gen(InfectionOtherSideQuests)
OptionalPartyMembers: InfectionEventLocation = event_gen(
    InfectionOptionalPartyMembers)
PlayStatLocsList = playstat_gen()

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

PlayStatLocations: InfectionPlayStatLocation = [
    *PlayStatLocsList
]


def generate_event_name_to_id() -> dict[str, int]:
    name_to_id: dict[str, int] = {el.name: el.location_id for el in EventLocations}
    name_to_id.update({el.name: el.location_id for el in WordListLocations})
    return name_to_id


def generate_playstat_name_to_id(locs: list[InfectionPlayStatLocation] = PlayStatLocations) -> dict[str, int]:
    name_to_id: dict[str, int] = {el.name: el.location_id for el in locs}
    return name_to_id


def generate_name_to_id() -> dict[str, int]:
    name_to_id = generate_event_name_to_id()
    name_to_id.update(generate_playstat_name_to_id())
    return name_to_id


def generate_location_groups() -> dict[str, int]:
    groups: dict[str: set[str]] = {}

    groups.update({
        "Story Events": {el.name: el.location_id for el in StoryEvents},
        "Golden Goblins": {el.name: el.location_id for el in GoldenGoblins},
        "Side Quests": {el.name: el.location_id for el in SideQuests},
        "Optional Party Members": {el.name: el.location_id for el in OptionalPartyMembers},
        "Play Stats": {el.name: el.location_id for el in PlayStatLocations},
        "Area Words": {el.name: el.location_id for el in AreaWordLocations},
        "Word Lists": {el.name: el.location_id for el in WordListLocations}
    })
    return groups
