from BaseClasses import LocationProgressType
from abc import ABC

from BaseClasses import Location

from .items.AreaWords import AreaWords
from .locations.Events import InfectionStoryEvents, InfectionGoldenGoblins, InfectionOptionalPartyMembers, CompletionConditions, InfectionMonsters
from .locations.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList, WordListBase, get_wordlist_name
from .locations.PlayStats import PlayStats
from .Strings import Meta, AreaWordNames, EventNames, PlayStatNames, MonsterNames
from .Addresses import InfectionAddresses as Addresses
from .DataManager import VOLUME_DATA


class InfectionLocation(Location):
    game: str = str(Meta.game.value)


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

    def __init__(self, word: AreaWords):
        self.name = AreaWordNames[word.name].value
        self.location_id = word.value["id"]*10 + Addresses.AreaWords
        self.word = word


class InfectionWordListLocation(InfectionLocationMeta):
    wordlist: WordListBase

    def __init__(self, wordlist: WordListBase):
        self.name = get_wordlist_name(wordlist)
        self.location_id = Addresses.WordLists * 10 + wordlist.value["address"]
        self.wordlist = wordlist
        self.progress_type = LocationProgressType.DEFAULT


class InfectionEventLocation(InfectionLocationMeta):
    event: InfectionStoryEvents
    bitflags: int
    progress_type: LocationProgressType

    def __init__(self, name: str, location_id: int, event, bitflags: int):
        self.name = name
        self.location_id = location_id
        self.event = event
        self.bitflags = bitflags
        self.progress_type = LocationProgressType.DEFAULT


class InfectionPlayStatLocation(InfectionLocationMeta):
    stat: PlayStats

    def __init__(self, name: str, stat: PlayStats, progress: int, progress_type: LocationProgressType):
        self.name = name
        self.location_id = (stat.value["addr"] * 500) + progress
        self.stat = stat
        self.progress_type = progress_type

class InfectionMonsterLocation(InfectionLocationMeta):
    monster: InfectionMonsters

    def __init__(self, name: str, monster: InfectionMonsters):
        self.name = name
        self.location_id = (monster.value["address"] * 400)
        self.monster = monster
        self.progress_type = LocationProgressType.DEFAULT


def area_word_gen(enum) -> list[InfectionAreaWordLocation]:
    res = []
    for word in enum:
        res.append(InfectionAreaWordLocation(
            word
        ))
    return res


def wordlist_gen(enum, volume: int) -> list[InfectionWordListLocation]:
    res = []
    for wordlist in enum:
        volumes = wordlist.value.get("volumes", [])
        if isinstance(volumes, list) and volume in volumes:
            res.append(InfectionWordListLocation(
                wordlist
            ))
    return res


def event_gen(enum, volume: int) -> list[InfectionEventLocation]:
    res = []
    for event in enum:
        volumes = event.value.get("volumes", [])
        if isinstance(volumes, list) and volume in volumes:
            name = EventNames[event.name].value
            res.append(InfectionEventLocation(
                name=name,
                location_id=event.value["address"],
                event=event,
                bitflags=event.value["bits"]
            ))
    return res

def hunt_gen(enum, volume: int) -> list[InfectionMonsterLocation]:
    res = []
    for monster in enum:
        volumes = monster.value.get("volumes", [])
        if isinstance(volumes, list) and volume in volumes:
            name = MonsterNames[monster.name].value
            res.append(InfectionMonsterLocation(
                name=name,
                monster=monster
            ))
    return res

PlayStatLocsList: list[InfectionPlayStatLocation]


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
            PlayStatNames.GoldenEgg.name: 20,
            PlayStatNames.GruntMints.name: 20,
            PlayStatNames.TwilightOnion.name: 20,
            PlayStatNames.SnakyCactus.name: 20,
            PlayStatNames.OhNoMelon.name: 20,
            PlayStatNames.Cordyceps.name: 20,
            PlayStatNames.WhiteCherry.name: 20,
            PlayStatNames.RootVegetable.name: 20,
            PlayStatNames.LaPumpkin.name: 20,
            PlayStatNames.Mushroom.name: 20,
            PlayStatNames.Mandragora.name: 20,
            PlayStatNames.PineyApple.name: 20,
            PlayStatNames.ImmatureEgg.name: 20,
            PlayStatNames.BearCatEgg.name: 20,
            PlayStatNames.InvisibleEgg.name: 20,
            PlayStatNames.BloodyEgg.name: 20


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


AreaWordLocations = area_word_gen(AreaWords)
PlayStatLocsList = playstat_gen()


def generate_volume_locations(volume: int):
    v_data = VOLUME_DATA[volume]
    v_data.wordlist_locations = [
        *wordlist_gen(DeltaWordList, volume),
        *wordlist_gen(ThetaWordList, volume)
    ]
    v_data.event_locations = [
        *event_gen(InfectionStoryEvents, volume),
        *event_gen(InfectionGoldenGoblins, volume),
        *event_gen(InfectionOptionalPartyMembers, volume),
        *event_gen(CompletionConditions, volume),
    ]
    v_data.monster_locations = [
        *hunt_gen(InfectionMonsters, volume)
    ]


for v in VOLUME_DATA:
    generate_volume_locations(v)

WordListLocations: list[InfectionWordListLocation] = []
EventLocations: list[InfectionEventLocation] = []
StoryEvents: list[InfectionEventLocation] = []
GoldenGoblins: list[InfectionEventLocation] = []
OptionalPartyMembers: list[InfectionEventLocation] = []
Monsters: list[InfectionEventLocation] = []
CompletionEvents: list[InfectionEventLocation] = []

for v_data in VOLUME_DATA.values():
    for loc in v_data.wordlist_locations:
        if loc.name not in [l.name for l in WordListLocations]:
            WordListLocations.append(loc)
    for loc in v_data.event_locations:
        if loc.name not in [l.name for l in EventLocations]:
            EventLocations.append(loc)
            if isinstance(loc.event, InfectionStoryEvents):
                StoryEvents.append(loc)
            elif isinstance(loc.event, InfectionGoldenGoblins):
                GoldenGoblins.append(loc)
            elif isinstance(loc.event, InfectionOptionalPartyMembers):
                OptionalPartyMembers.append(loc)
            elif isinstance(loc.event, CompletionConditions):
                CompletionEvents.append(loc)
    for loc in v_data.monster_locations:
        if loc.name not in [l.name for l in Monsters]:
            Monsters.append(loc)

PlayStatLocations: list[InfectionPlayStatLocation] = [
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


def generate_location_groups() -> dict[str, set[str]]:
    groups: dict[str, set[str]] = {}

    groups.update({
        "Story Events": {el.name for el in StoryEvents},
        "Golden Goblins": {el.name for el in GoldenGoblins},
        "Optional Party Members": {el.name for el in OptionalPartyMembers},
        "Play Stats": {el.name for el in PlayStatLocations},
        "Area Words": {el.name for el in AreaWordLocations},
        "Word Lists": {el.name for el in WordListLocations},
        "Monsters": {el.name for el in Monsters}
    })
    return groups
