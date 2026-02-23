from enum import Enum
from ..items.AreaWords import InfectionAreaWords as AreaWords

ADDRESS = 0xa44c47


class InfectionWordListBase(Enum):
    @classmethod
    def from_address(self, address: int):
        for member in self:
            if member.value["address"] == address:
                return member
        return None


class InfectionDeltaWordList(InfectionWordListBase):
    BurstingPassedOverAquaField = {"address": 0x0e, "words": [
        AreaWords.Bursting, AreaWords.PassedOver, AreaWords.AquaField
    ]}
    HiddenForbiddenHolyGround = {"address": 0x0f, "words": [
        AreaWords.Hidden, AreaWords.Forbidden, AreaWords.HolyGround
    ]}
    HideousSomeonesGiant = {"address": 0x10, "words": [
        AreaWords.Hideous, AreaWords.Someones, AreaWords.Giant
    ]}
    ExpansiveHauntedSeaOfSand = {"address": 0x11, "words": [
        AreaWords.Expansive, AreaWords.Haunted, AreaWords.SeaOfSand
    ]}
    BoundlessCorruptedFortWalls = {"address": 0x12, "words": [
        AreaWords.Boundless, AreaWords.Corrupted, AreaWords.FortWalls
    ]}
    ClosedObliviousTwinHills = {"address": 0x13, "words": [
        AreaWords.Closed, AreaWords.Oblivious, AreaWords.TwinHills
    ]}
    DetestableGoldenSunnyDemon = {"address": 0x1c, "words": [
        AreaWords.Detestable, AreaWords.Golden, AreaWords.SunnyDemon
    ]}
    DiscoveredPrimitiveTouchstone = {"address": 0x1d, "words": [
        AreaWords.Discovered, AreaWords.Primitive, AreaWords.Touchstone
    ]}
    IndiscreetGluttonousPilgrimage = {"address": 0x1e, "words": [
        AreaWords.Indiscreet, AreaWords.Gluttonous, AreaWords.Pilgrimage
    ]}
    DetestableGoldenMessenger = {"address": 0x27, "words": [
        AreaWords.Detestable, AreaWords.Golden, AreaWords.Messenger
    ]}
    RagingPassionateMelody = {"address": 0x23, "words": [
        AreaWords.Raging, AreaWords.Passionate, AreaWords.Melody
    ]}
    PlenteousSmilingHypha = {"address": 0x15, "words": [
        AreaWords.Plenteous, AreaWords.Smiling, AreaWords.Hypha
    ]}
    DetestableGoldenScent = {"address": 0x28, "words": [
        AreaWords.Detestable, AreaWords.Golden, AreaWords.Scent
    ]}
    HideousDestroyersFarThunder = {"address": 0x20, "words": [
        AreaWords.Hideous, AreaWords.Destroyers, AreaWords.FarThunder
    ]}
    PutridHotbloodedScaffold = {"address": 0x1f, "words": [
        AreaWords.Putrid, AreaWords.HotBlooded, AreaWords.Scaffold
    ]}
    DetestableGoldenNewTruth = {"address": 0x29, "words": [
        AreaWords.Detestable, AreaWords.Golden, AreaWords.NewTruth
    ]}
    BuriedPaganFierySands = {"address": 0x18, "words": [
        AreaWords.Buried, AreaWords.Pagan, AreaWords.FierySands
    ]}
    LonelySilentGreatSeal = {"address": 0x19, "words": [
        AreaWords.Lonely, AreaWords.Silent, AreaWords.GreatSeal
    ]}
    DetestableGoldenGate = {"address": 0x2a, "words": [
        AreaWords.Detestable, AreaWords.Golden, AreaWords.Gate
    ]}


class InfectionThetaWordList(InfectionWordListBase):
    QuietEternalWhiteDevil = {"address": 0x14, "words": [
        AreaWords.Quiet, AreaWords.Eternal, AreaWords.WhiteDevil
    ]}
    SoftSolitaryTriPansy = {"address": 0x21, "words": [
        AreaWords.Soft, AreaWords.Solitary, AreaWords.TriPansy
    ]}
    CollapsedMomentarySpiral = {"address": 0x16, "words": [
        AreaWords.Collapsed, AreaWords.Momentary, AreaWords.Spiral
    ]}
    BeautifulSomeonesTreasureGem = {"address": 0x22, "words": [
        AreaWords.Beautiful, AreaWords.Someones, AreaWords.TreasureGem
    ]}
    CursedDespairedParadise = {"address": 0x17, "words": [
        AreaWords.Cursed, AreaWords.Despaired, AreaWords.Paradise
    ]}
    GreatDistantFertileLand = {"address": 0x1a, "words": [
        AreaWords.Great, AreaWords.Distant, AreaWords.FertileLand
    ]}
    ChosenHopelessNothingness = {"address": 0x1b, "words": [
        AreaWords.Chosen, AreaWords.Hopeless, AreaWords.Nothingness
    ]}
