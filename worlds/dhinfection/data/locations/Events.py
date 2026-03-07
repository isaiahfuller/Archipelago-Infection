from enum import IntEnum, auto, Enum


class InfectionEventBase(Enum):
    @classmethod
    def from_address(self, address: int):
        for member in self:
            if member.value["address"] == address:
                return member
        return None


class InfectionStoryEvents(InfectionEventBase):
    # CharacterCreation = {"address": 0xa44ed7, "bits": 0b11000000}
    # FirstLogin = {"address": 0xa44ed8, "bits": 0b00000111}
    # BattleTutorial = {"address": 0xa44ee0, "bits": 0b00100101}
    # DungeonTutorial = {"address": 0xa44ee8, "bits": 0b11110100}
    # FirstAura = {"address": 0xa44ee9, "bits": 0b00000011}
    # FirstAuraScene2 = {"address": 0xa44eef, "bits": 0b10000000}
    # Coma = {"address": 0xa44ee7, "bits": 0b01000000}
    # MetBlackRose = {"address": 0xa44f20, "bits": 0b11010101}
    # Cathedral = {"address": 0xa44f22, "bits": 0b01010100}
    # BookOfTwilight = {"address": 0xa44f23, "bits": 0b00000001}
    FirstDataBug = {"address": 0xa44f39, "bits": 0b00000100}
    LearnGateHacking = {"address": 0xa44f52, "bits": 0b00000010}
    SavedPiros = {"address": 0xa44f41, "bits": 0b00000001}
    # YoureWinner = {"address": 0xa44f48, "bits": 0b00010000}
    BoardProtected = {"address": 0xa44f5a, "bits": 0b00010000}
    BlackRoseDungeon = {"address": 0xa44f6a, "bits": 0b00000100}
    ElkMiaFavorite = {"address": 0xa44f71, "bits": 0b10000000}
    PirosDiary = {"address": 0xa44f7b, "bits": 0b00100000}
    MistralMeetUp = {"address": 0xa44f90, "bits": 0b00000001}
    Epitaph00 = {"address": 0xa44f92, "bits": 0b00000001}
    DescendentsOfFianna = {"address": 0xa44fa8, "bits": 0b00000001}
    EpitaphQ = {"address": 0xa44fb0, "bits": 0b00000001}
    MeetAlf = {"address": 0xa44fb8, "bits": 0b00000001}
    # InfectionBeat = {"address": 0xa44fc0, "bits": 0b00000001}


class InfectionGoldenGoblins(InfectionEventBase):
    Stehony = {"address": 0xa45059, "bits": 0b00000001}
    Jonue = {"address": 0xa45061, "bits": 0b00000001}
    Zyan = {"address": 0xa45069, "bits": 0b00000001}
    Albert = {"address": 0xa45071, "bits": 0b00000001}
    Martina = {"address": 0xa45079, "bits": 0b00000001}


class InfectionOptionalPartyMembers(InfectionEventBase):
    Sanjuro = {"address": 0xa45099, "bits": 0b00000001}
    Gardenia = {"address": 0xa450a2, "bits": 0b00000100}
    Natsume = {"address": 0xa450b0, "bits": 0b10000000}


class InfectionOtherSideQuests(InfectionEventBase):
    GracefulBook = {"address": 0xa450a9, "bits": 0b00000001}
    ParasiteDragon = {"address": 0xa450b8, "bits": 0b00010000}
