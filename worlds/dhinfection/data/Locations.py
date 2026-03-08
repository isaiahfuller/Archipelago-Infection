from typing import Sequence
from dataclasses import dataclass
from abc import ABC
import copy

from BaseClasses import Location

from .items.AreaWords import InfectionAreaWords as AreaWords, ADDRESS as AreaWordAddress
from .locations.Events import InfectionStoryEvents, InfectionGoldenGoblins, InfectionOptionalPartyMembers, InfectionOtherSideQuests
from .locations.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList, ADDRESS as WordListAddress, InfectionWordListBase, get_wordlist_name
from .locations.PlayStats import PlayStats, RyuBookI, RyuBookII, RyuBookVI, RyuBookVII, Affection, OtherStats, CharacterLevels as CharacterLevelStats
from .Strings import Meta, InfectionAreaWordNames as AreaWordNames, InfectionEventNames as EventNames, InfectionPlayStatNames as PlayStatNames  


class InfectionLocation(Location):
    game: str = Meta.game.value


class InfectionLocationMeta(ABC):
    name: str
    location_id: int
    address: int

class InfectionAreaWordLocation(InfectionLocationMeta):
    word: AreaWords

    def __init__(self, word: AreaWords) -> InfectionLocation:
        self.name = AreaWordNames[word.name].value
        self.location_id = word.value["id"]*10 + AreaWordAddress
        self.word = word

    def to_location(self, player: int) -> Location:
        return Location(player, self.name, self.location_id, parent)

class InfectionWordListLocation(InfectionLocationMeta):
    wordlist: InfectionWordListBase

    def __init__(self, wordlist: InfectionWordListBase) -> InfectionLocation:
        self.name = get_wordlist_name(wordlist)
        self.location_id = WordListAddress * 10 + wordlist.value["address"]
        self.wordlist = wordlist

    def to_location(self, player: int) -> Location:
        return Location(player, self.name, self.location_id, parent)


class InfectionEventLocation(InfectionLocationMeta):
    event: InfectionStoryEvents
    bitflags: int

    def __init__(self, name: str, location_id: int, event, bitflags: int) -> InfectionLocation:
        self.name = name
        self.location_id = location_id
        self.event = event
        self.bitflags = bitflags

    def to_location(self, player: int) -> Location:
        return Location(player, self.name, self.location_id, parent)

class InfectionPlayStatLocation(InfectionLocationMeta):
    stat: PlayStats

    def __init__(self, name: str, stat: PlayStats, progress: int) -> InfectionLocation:
        self.name = name
        self.location_id = (stat.value * 500) + progress
        self.stat = stat

    def to_location(self, player: int) -> Location:
        return Location(player, self.name, self.location_id, parent)

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

def playstat_gen(enum, progress: list[int] | None = None, r: tuple[int, int] | None = None) -> list[InfectionPlayStatLocation]:
    res = []
    for stat in enum:
        if progress:
            for i in progress:
                res.append(InfectionPlayStatLocation(
                    name=PlayStatNames[stat.name].value + str(i),
                    stat=stat,
                    progress=i
                ))
        elif r:
            for i in range(r[0], r[1]):
                res.append(InfectionPlayStatLocation(
                    name=PlayStatNames[stat.name].value + str(i),
                    stat=stat,
                    progress=i
                ))
    return res

DeltaListLocations = wordlist_gen(DeltaWordList)
ThetaListLocations = wordlist_gen(ThetaWordList)
AreaWordLocations = area_word_gen(AreaWords)

StoryEvents: InfectionEventLocation = event_gen(InfectionStoryEvents)
GoldenGoblins: InfectionEventLocation = event_gen(InfectionGoldenGoblins)
SideQuests: InfectionEventLocation = event_gen(InfectionOtherSideQuests)
OptionalPartyMembers: InfectionEventLocation = event_gen(
    InfectionOptionalPartyMembers)
RyuBookI: InfectionPlayStatLocation = playstat_gen(RyuBookI, r=(1,31))
RyuBookII: InfectionPlayStatLocation = playstat_gen(RyuBookII, [5, 10, 25, 50, 75, 100])
RyuBookVI: InfectionPlayStatLocation = playstat_gen(RyuBookVI, [5, 10, 25, 50, 75, 100, 150, 200, 300, 400])
RyuBookVII: InfectionPlayStatLocation = playstat_gen(RyuBookVII, [5, 10, 25, 50, 75, 100])
OtherStats: InfectionPlayStatLocation = playstat_gen(OtherStats, [5, 10, 25, 50, 75, 100])
CharacterLevels: InfectionPlayStatLocation = playstat_gen(CharacterLevelStats, r=(1, 31))

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
    *RyuBookI,
    *RyuBookII,
    *RyuBookVI,
    *RyuBookVII,
    *OtherStats,
    *CharacterLevels
]

def generate_name_to_id() -> dict[str, int]:
    name_to_id: dict[str, int] = {el.name: el.location_id for el in EventLocations}
    name_to_id.update({el.name: el.location_id for el in PlayStatLocations})
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
        # "Word Lists": {el.name: el.location_id for el in WordListLocations}
    })
    return groups
