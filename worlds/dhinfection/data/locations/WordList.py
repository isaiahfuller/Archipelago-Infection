from enum import Enum
from BaseClasses import Item, ItemClassification
from ..items.AreaWords import InfectionAreaWords as AreaWords
from ..Strings import InfectionAreaWordNames as AreaWordNames

ADDRESS = 0xa44c47


class InfectionWordListBase(Enum):
    @classmethod
    def from_address(self, address: int):
        for member in self:
            if member.value["address"] == address:
                return member
        return None


def get_wordlist_name(wordlist: InfectionWordListBase) -> str:
    words = []
    for word in wordlist.value["words"]:
        words.append(AreaWordNames[word.name].value)
    return " ".join(words)


class InfectionDeltaWordList(InfectionWordListBase):
    BurstingPassedOverAquaField = {"address": 0x0e, "words": [
        AreaWords.Bursting, AreaWords.PassedOver, AreaWords.AquaField
    ],
    "importance": ItemClassification.progression
    }
    HiddenForbiddenHolyGround = {"address": 0x0f, "words": [
        AreaWords.Hidden, AreaWords.Forbidden, AreaWords.HolyGround
    ],
    "importance": ItemClassification.progression
    }
    HideousSomeonesGiant = {"address": 0x10, "words": [
        AreaWords.Hideous, AreaWords.Someones, AreaWords.Giant
    ],
    "importance": ItemClassification.useful
    }
    ExpansiveHauntedSeaOfSand = {"address": 0x11, "words": [
        AreaWords.Expansive, AreaWords.Haunted, AreaWords.SeaOfSand
    ],
    "importance": ItemClassification.progression
    }
    BoundlessCorruptedFortWalls = {"address": 0x12, "words": [
        AreaWords.Boundless, AreaWords.Corrupted, AreaWords.FortWalls
    ],
    "importance": ItemClassification.progression
    }
    ClosedObliviousTwinHills = {"address": 0x13, "words": [
        AreaWords.Closed, AreaWords.Oblivious, AreaWords.TwinHills
    ],
    "importance": ItemClassification.progression
    }
    DetestableGoldenSunnyDemon = {"address": 0x1c, "words": [
        AreaWords.Detestable, AreaWords.Golden, AreaWords.SunnyDemon
    ],
    "importance": ItemClassification.progression
    }
    DiscoveredPrimitiveTouchstone = {"address": 0x1d, "words": [
        AreaWords.Discovered, AreaWords.Primitive, AreaWords.Touchstone
    ],
    "importance": ItemClassification.progression
    }
    IndiscreetGluttonousPilgrimage = {"address": 0x1e, "words": [
        AreaWords.Indiscreet, AreaWords.Gluttonous, AreaWords.Pilgrimage
    ],
    "importance": ItemClassification.progression
    }
    DetestableGoldenMessenger = {"address": 0x27, "words": [
        AreaWords.Detestable, AreaWords.Golden, AreaWords.Messenger
    ],
    "importance": ItemClassification.progression
    }
    RagingPassionateMelody = {"address": 0x23, "words": [
        AreaWords.Raging, AreaWords.Passionate, AreaWords.Melody
    ],
    "importance": ItemClassification.progression
    }
    PlenteousSmilingHypha = {"address": 0x15, "words": [
        AreaWords.Plenteous, AreaWords.Smiling, AreaWords.Hypha
    ],
    "importance": ItemClassification.progression
    }
    DetestableGoldenScent = {"address": 0x28, "words": [
        AreaWords.Detestable, AreaWords.Golden, AreaWords.Scent
    ],
    "importance": ItemClassification.progression
    }
    HideousDestroyersFarThunder = {"address": 0x20, "words": [
        AreaWords.Hideous, AreaWords.Destroyers, AreaWords.FarThunder
    ],
    "importance": ItemClassification.progression
    }
    PutridHotbloodedScaffold = {"address": 0x1f, "words": [
        AreaWords.Putrid, AreaWords.HotBlooded, AreaWords.Scaffold
    ],
    "importance": ItemClassification.progression
    }
    DetestableGoldenNewTruth = {"address": 0x29, "words": [
        AreaWords.Detestable, AreaWords.Golden, AreaWords.NewTruth
    ],
    "importance": ItemClassification.progression
    }
    BuriedPaganFierySands = {"address": 0x18, "words": [
        AreaWords.Buried, AreaWords.Pagan, AreaWords.FierySands
    ],
    "importance": ItemClassification.progression
    }
    LonelySilentGreatSeal = {"address": 0x19, "words": [
        AreaWords.Lonely, AreaWords.Silent, AreaWords.GreatSeal
    ],
    "importance": ItemClassification.progression
    }
    DetestableGoldenGate = {"address": 0x2a, "words": [
        AreaWords.Detestable, AreaWords.Golden, AreaWords.Gate
    ],
    "importance": ItemClassification.progression
    }


class InfectionThetaWordList(InfectionWordListBase):
    QuietEternalWhiteDevil = {"address": 0x14, "words": [
        AreaWords.Quiet, AreaWords.Eternal, AreaWords.WhiteDevil
    ],
    "importance": ItemClassification.progression
    }
    SoftSolitaryTriPansy = {"address": 0x21, "words": [
        AreaWords.Soft, AreaWords.Solitary, AreaWords.TriPansy
    ],
    "importance": ItemClassification.progression
    }
    CollapsedMomentarySpiral = {"address": 0x16, "words": [
        AreaWords.Collapsed, AreaWords.Momentary, AreaWords.Spiral
    ],
    "importance": ItemClassification.progression
    }
    BeautifulSomeonesTreasureGem = {"address": 0x22, "words": [
        AreaWords.Beautiful, AreaWords.Someones, AreaWords.TreasureGem
    ],
    "importance": ItemClassification.progression
    }
    CursedDespairedParadise = {"address": 0x17, "words": [
        AreaWords.Cursed, AreaWords.Despaired, AreaWords.Paradise
    ],
    "importance": ItemClassification.progression
    }
    GreatDistantFertileLand = {"address": 0x1a, "words": [
        AreaWords.Great, AreaWords.Distant, AreaWords.FertileLand
    ],
    "importance": ItemClassification.progression
    }
    ChosenHopelessNothingness = {"address": 0x1b, "words": [
        AreaWords.Chosen, AreaWords.Hopeless, AreaWords.Nothingness
    ],
    "importance": ItemClassification.progression
    }
