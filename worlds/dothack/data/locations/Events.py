from enum import Enum
from typing import TypedDict
from worlds.dothack.data.Addresses import MonsterNames



class InfectionEventAttributes(TypedDict):
    address: int
    bits: int
    volumes: list[int]


class InfectionEventBase(Enum):
    _value_: InfectionEventAttributes

    @classmethod
    def from_address(self, address: int):
        for member in self:
            if member.value["address"] == address:
                return member
        return None


class InfectionStoryEvents(InfectionEventBase):
    FirstDataBug = {"address": 0xa44f39, "bits": 0b00000100, "volumes": [1]}
    LearnGateHacking = {"address": 0xa44f52, "bits": 0b00000010, "volumes": [1]}
    SavedPiros = {"address": 0xa44f41, "bits": 0b00000001, "volumes": [1]}
    BoardProtected = {"address": 0xa44f5a, "bits": 0b00010000, "volumes": [1]}
    BlackRoseDungeon = {"address": 0xa44f6a, "bits": 0b00000100, "volumes": [1]}
    ElkMiaFavorite = {"address": 0xa44f71, "bits": 0b10000000, "volumes": [1]}
    PirosDiary = {"address": 0xa44f7b, "bits": 0b00100000, "volumes": [1]}
    MistralMeetUp = {"address": 0xa44f90, "bits": 0b00000001, "volumes": [1]}
    Epitaph00 = {"address": 0xa44f92, "bits": 0b00000001, "volumes": [1]}
    DescendentsOfFianna = {"address": 0xa44fa8, "bits": 0b00000001, "volumes": [1]}
    EpitaphQ = {"address": 0xa44fb0, "bits": 0b00000001, "volumes": [1]}
    MetMeg = {"address": 0xa44fb8, "bits": 0b00000001, "volumes": [1]}


class CompletionConditions(InfectionEventBase):
    SkeithDefeated = {"address": 0xa44fc0, "bits": 0b00000001, "volumes": [1]}
    ParasiteDragonDefeated = {"address": 0xa450b8, "bits": 0b00010000, "volumes": [1]}


class InfectionGoldenGoblins(InfectionEventBase):
    Stehony = {"address": 0xa45059, "bits": 0b00000001, "volumes": [1]}
    Jonue = {"address": 0xa45061, "bits": 0b00000001, "volumes": [1]}
    Zyan = {"address": 0xa45069, "bits": 0b00000001, "volumes": [1]}
    Albert = {"address": 0xa45071, "bits": 0b00000001, "volumes": [1]}
    Martina = {"address": 0xa45079, "bits": 0b00000001, "volumes": [1]}


class InfectionOptionalPartyMembers(InfectionEventBase):
    Sanjuro = {"address": 0xa45099, "bits": 0b00000001, "volumes": [1]}
    Gardenia = {"address": 0xa450a2, "bits": 0b00000100, "volumes": [1]}
    Natsume = {"address": 0xa450b0, "bits": 0b10000000, "volumes": [1]}
    GracefulBook = {"address": 0xa450a9, "bits": 0b00000001, "volumes": [1]}


class MonsterHunt1(InfectionEventBase):
    Razine1 = {"address": 0xa46287, "bits": 0b00000001, "volumes": [1]}
    Swordmanoid2 = {"address": 0xa46288, "bits": 0b00000001, "volumes": [1]}

    Ochimusha4 = {"address": 0xa4628a,"bits": 0b00000001, "volumes": [1]}
    HeavyMetal6 = {"address": 0xa4628c, "bits": 0b00000001, "volumes": [1]}


    GeneralArmor13 = {"address": 0xa46293, "bits": 0b00000001, "volumes": [1]}
    Porolin14 = {"address": 0xa46294, "bits": 0b00000001, "volumes": [1]}
    MummyRipper15 = {"address": 0xa46295, "bits": 0b00000001, "volumes": [1]}
    CadetValkyrie20 = {"address": 0xa4629A, "bits": 0b00000001, "volumes": [1]}


    Flamer36 = {"address": 0xa462AA, "bits": 0b00000001, "volumes": [1]}
    FireWitch37 = {"address": 0xa462AB, "bits": 0b00000001, "volumes": [1]}
    WaterWitch38 = {"address": 0xa462AC, "bits": 0b00000001, "volumes": [1]}
    DarkWitch39 = {"address": 0xa462AD, "bits": 0b00000001, "volumes": [1]}
    Kakasinger49 = {"address": 0xa462B7, "bits": 0b00000001, "volumes": [1]}
    Guardian50 = {"address": 0xa462B8, "bits": 0b00000001, "volumes": [1]}
    MetalEmperor52 = {"address": 0xa462BA, "bits": 0b00000001, "volumes": [1]}

    Pippy67 = {"address": 0xa462C9, "bits": 0b00000001, "volumes": [1]}
    ChickenHand68 = {"address": 0xa462CA, "bits": 0b00000001, "volumes": [1]}
    WoodHarpy69 = {"address": 0xa462CB, "bits": 0b00000001, "volumes": [1]}

    MonkeyCrab80 = {"address": 0xa462D6, "bits": 0b00000001, "volumes": [1]}
    SnipSnap81 = {"address": 0xa462D7, "bits": 0b00000001, "volumes": [1]}
    CrabTurtle82 = {"address": 0xa462D8, "bits": 0b00000001, "volumes": [1]}

    SquillaDemon84 = {"address": 0xa462DA, "bits": 0b00000001, "volumes": [1]}

    ShieldMan91 = {"address": 0xa462E1, "bits": 0b00000001, "volumes": [1]}
    Moai105 = {"address": 0xa462EF, "bits": 0b00000001, "volumes": [1]}
    RockHead106 = {"address": 0xa462F0, "bits": 0b00000001, "volumes": [1]}

    StoneTuttle114 = {"address": 0xa462F8, "bits": 0b00000001, "volumes": [1]}
    StoneTuttleDataBug116 = {"address": 0xa462FA, "bits": 0b00000001, "volumes": [1]}
    Minnow117 = {"address": 0xa462FB, "bits": 0b00000001, "volumes": [1]}
    SkyFish118 = {"address": 0xa462FC, "bits": 0b00000001, "volumes": [1]}
    ArrowFish119 = {"address": 0xa462FD, "bits": 0b00000001, "volumes": [1]}
    CycloShark123 = {"address": 0xa46301, "bits": 0b00000001, "volumes": [1]}

    Gremlin130 = {"address": 0xa46308, "bits": 0b00000001, "volumes": [1]}
    Goblin131 = {"address": 0xa46309, "bits": 0b00000001, "volumes": [1]}
    Stehoney132 = {"address": 0xa4630A, "bits": 0b00000001, "volumes": [1]}
    Jonue133 = {"address": 0xa4630B, "bits": 0b00000001, "volumes": [1]}
    HobGoblin140 = {"address": 0xa46312, "bits": 0b00000001, "volumes": [1]}
    Zyan141 = {"address": 0xa46313, "bits": 0b00000001, "volumes": [1]}
    GoblinNight145 = {"address": 0xa46317, "bits": 0b00000001, "volumes": [1]}

    Albert148 = {"address": 0xa4631A, "bits": 0b00000001, "volumes": [1]}
    MagicalGoblin152 = {"address": 0xa4631E, "bits": 0b00000001, "volumes": [1]}
    GoblinWiz153 = {"address": 0xa4631F, "bits": 0b00000001, "volumes": [1]}
    Martina155 = {"address": 0xa46321, "bits": 0b00000001, "volumes": [1]}

    LittleDoggie168 = {"address": 0xa4632E, "bits": 0b00000001, "volumes": [1]}
    SledDog169 = {"address": 0xa4632F, "bits": 0b00000001, "volumes": [1]}
    HellDoberman172 = {"address": 0xa46332, "bits": 0b00000001, "volumes": [1]}

    FlameHeads176 = {"address": 0xa46336, "bits": 0b00000001, "volumes": [1]}
    WiggleSnake179 = {"address": 0xa46339, "bits": 0b00000001, "volumes": [1]}
    Menhir180 = {"address": 0xa4633A, "bits": 0b00000001, "volumes": [1]}

    FiendMenhir184 = {"address": 0xa4633E, "bits": 0b00000001, "volumes": [1]}
    LimpKnife185 = {"address": 0xa4633F, "bits": 0b00000001, "volumes": [1]}
    DiscoKnife186 = {"address": 0xa46340, "bits": 0b00000001, "volumes": [1]}
    LambadaKnife187 = {"address": 0xa46341, "bits": 0b00000001, "volumes": [1]}
    DustCurse188 = {"address": 0xa46342, "bits": 0b00000001, "volumes": [1]}

    SwordofChaos190 = {"address": 0xa46344, "bits": 0b00000001, "volumes": [1]}

    DragonPuppy194 = {"address": 0xa46348, "bits": 0b00000001, "volumes": [1]}
    Snakoid195 = {"address": 0xa46349, "bits": 0b00000001, "volumes": [1]}

    RedWyrm200 = {"address": 0xa4634E, "bits": 0b00000001, "volumes": [1]}
    RedWyrmDataBug202 = {"address": 0xa46350, "bits": 0b00000001, "volumes": [1]}
    ParasiteDragon215 = {"address": 0xa4635D, "bits": 0b00000001, "volumes": [1]}
    TwinkleGrass219 = {"address": 0xa46361, "bits": 0b00000001, "volumes": [1]}
    MadGrass220 = {"address": 0xa46362, "bits": 0b00000001, "volumes": [1]}
    HungryGrass221 = {"address": 0xa46363, "bits": 0b00000001, "volumes": [1]}

    ThousandTrees224 = {"address": 0xa46366, "bits": 0b00000001, "volumes": [1]}
    WoodStockDataBug225 = {"address": 0xa46367, "bits": 0b00000001, "volumes": [1]}
    ScarletKing227 = {"address": 0xa46369, "bits": 0b00000001, "volumes": [1]}
    MushroomKing229 = {"address": 0xa4636A, "bits": 0b00000001, "volumes": [1]}
    Charmer230 = {"address": 0xa4636C, "bits": 0b00000001, "volumes": [1]}
    LamiaFighter231 = {"address": 0xa4636D, "bits": 0b00000001, "volumes": [1]}

    KillerSnaker234 = {"address": 0xa46370, "bits": 0b00000001, "volumes": [1]}
    KillerSnakerDataBug236 = {"address": 0xa46372, "bits": 0b00000001, "volumes": [1]}
    FakeMoney240 = {"address": 0xa46377, "bits": 0b00000001, "volumes": [1]}
    Mimic241 = {"address": 0xa46378, "bits": 0b00000001, "volumes": [1]}

    DeathHead246 = {"address": 0xa4637C, "bits": 0b00000001, "volumes": [1]}
    NomadicBones247 = {"address": 0xa4637D, "bits": 0b00000001, "volumes": [1]}

    Headhunter253 = {"address": 0xa46383, "bits": 0b00000001, "volumes": [1]}
    HeadhunterDataBug256 = {"address": 0xa46386, "bits": 0b00000001, "volumes": [1]}
    Wiggly268 = {"address": 0xa46392, "bits": 0b00000001, "volumes": [1]}
    DeadlyMoth269 = {"address": 0xa46393, "bits": 0b00000001, "volumes": [1]}
    PhantomWing270 = {"address": 0xa46394, "bits": 0b00000001, "volumes": [1]}
    BeeArmy272 = {"address": 0xa46396, "bits": 0b00000001, "volumes": [1]}

    Odoro280 = {"address": 0xa4639E, "bits": 0b00000001, "volumes": [1]}
    Ectoplasm281 = {"address": 0xa46398, "bits": 0b00000001, "volumes": [1]}
    NoisyWisp282 = {"address": 0xa463A0, "bits": 0b00000001, "volumes": [1]}

    ShiningEyes288 = {"address": 0xa463A6, "bits": 0b00000001, "volumes": [1]}

class MonsterHunt2(InfectionEventBase):
    Gladiator3 = {"address": 0xa46289, "bits": 0b00000001, "volumes": [1]}
    DarkRider8 = {"address": 0xa4628E, "bits": 0b00000001, "volumes": [1]}
    TetraArmor11 = {"address": 0xa46291, "bits": 0b00000001, "volumes": [1]}
    FreshValkyrie21 = {"address": 0xa4629B, "bits": 0b00000001, "volumes": [1]}
    LongLived23 = {"address": 0xa4629D, "bits": 0b00000001, "volumes": [1]}
    GrandMage24 = {"address": 0xa4629E, "bits": 0b00000001, "volumes": [1]}
    MuGuardian57 = {"address": 0xa462BF, "bits": 0b00000001, "volumes": [1]}
    PhoenixQueen72 = {"address": 0xa462CE, "bits": 0b00000001, "volumes": [1]}
    RedScissors83 = {"address": 0xa462D9, "bits": 0b00000001, "volumes": [1]}
    Mantis86 = {"address": 0xa462DC, "bits": 0b00000001, "volumes": [1]}
    MysteryRock107 = {"address": 0xa462F1, "bits": 0b00000001, "volumes": [1]}
    HammerShark124 = {"address": 0xa46302, "bits": 0b00000001, "volumes": [1]}
    MetalGoblin146 = {"address": 0xa46318, "bits": 0b00000001, "volumes": [1]}
    Cannibal159 = {"address": 0xa46325, "bits": 0b00000001, "volumes": [1]}
    Ogre161 = {"address": 0xa46327, "bits": 0b00000001, "volumes": [1]}
    IronBallFreak163 = {"address": 0xa46329, "bits": 0b00000001, "volumes": [1]}
    HellHound173 = {"address": 0xa46333, "bits": 0b00000001, "volumes": [1]}
    GoilMenhir181 = {"address": 0xa4633B, "bits": 0b00000001, "volumes": [1]}
    CursedBlades189 = {"address": 0xa46343, "bits": 0b00000001, "volumes": [1]}
    ArmorShogun191 = {"address": 0xa46345, "bits": 0b00000001, "volumes": [1]}
    LeadSnakoid196 = {"address": 0xa4634A, "bits": 0b00000001, "volumes": [1]}
    SnappyGrass222 = {"address": 0xa46364, "bits": 0b00000001, "volumes": [1]}
    WoodStock223 = {"address": 0xa46365, "bits": 0b00000001, "volumes": [1]}
    LamiaHunter232 = {"address": 0xa4636E, "bits": 0b00000001, "volumes": [1]}
    HellBox242 = {"address": 0xa46379, "bits": 0b00000001, "volumes": [1]}
    LivingDead250 = {"address": 0xa46380, "bits": 0b00000001, "volumes": [1]}
    BeeAssault273 = {"address": 0xa46397, "bits": 0b00000001, "volumes": [1]}
    BabyWorm275 = {"address": 0xa46399, "bits": 0b00000001, "volumes": [1]}
    Halloween283 = {"address": 0xa463A1, "bits": 0b00000001, "volumes": [1]}

class MonsterHunt2List:
    Gladiator3 = 1
    DarkRider8 = 2
    TetraArmor11 = 3
    FreshValkyrie21 = 4
    LongLived23 = 5
    GrandMage24 = 6
    MuGuardian57 = 7
    PhoenixQueen72 = 8
    RedScissors83 = 9
    Mantis86 = 10
    MysteryRock107 = 11
    HammerShark124 = 12
    MetalGoblin146 = 13
    Cannibal159 = 14
    Ogre161 = 15
    IronBallFreak163 = 16
    HellHound173 = 17
    GoilMenhir181 = 18
    CursedBlades189 = 19
    ArmorShogun191 = 20
    LeadSnakoid196 = 21
    SnappyGrass222 = 22
    WoodStock223 = 23
    LamiaHunter232 = 24
    HellBox242 = 25
    LivingDead250 = 26
    BeeAssault273 = 27
    BabyWorm275 = 28
    Halloween283 = 29

MONSTER_ADDRESS_MAP = {
    MonsterHunt2List.Gladiator3: MonsterNames.Gladiator3,
    MonsterHunt2List.DarkRider8: MonsterNames.DarkRider8,
    MonsterHunt2List.TetraArmor11: MonsterNames.TetraArmor11,
    MonsterHunt2List.FreshValkyrie21: MonsterNames.FreshValkyrie21,
    MonsterHunt2List.LongLived23: MonsterNames.LongLived23,
    MonsterHunt2List.GrandMage24: MonsterNames.GrandMage24,
    MonsterHunt2List.MuGuardian57: MonsterNames.MuGuardian57,
    MonsterHunt2List.PhoenixQueen72: MonsterNames.PhoenixQueen72,
    MonsterHunt2List.RedScissors83: MonsterNames.RedScissors83,
    MonsterHunt2List.Mantis86: MonsterNames.Mantis86,
    MonsterHunt2List.MysteryRock107: MonsterNames.MysteryRock107,
    MonsterHunt2List.HammerShark124: MonsterNames.HammerShark124,
    MonsterHunt2List.MetalGoblin146: MonsterNames.MetalGoblin146,
    MonsterHunt2List.Cannibal159: MonsterNames.Cannibal159,
    MonsterHunt2List.Ogre161: MonsterNames.Ogre161,
    MonsterHunt2List.IronBallFreak163: MonsterNames.IronBallFreak163,
    MonsterHunt2List.HellHound173: MonsterNames.HellHound173,
    MonsterHunt2List.GoilMenhir181: MonsterNames.GoilMenhir181,
    MonsterHunt2List.CursedBlades189: MonsterNames.CursedBlades189,
    MonsterHunt2List.ArmorShogun191: MonsterNames.ArmorShogun191,
    MonsterHunt2List.LeadSnakoid196: MonsterNames.LeadSnakoid196,
    MonsterHunt2List.SnappyGrass222: MonsterNames.SnappyGrass222,
    MonsterHunt2List.WoodStock223: MonsterNames.WoodStock223,
    MonsterHunt2List.LamiaHunter232: MonsterNames.LamiaHunter232,
    MonsterHunt2List.HellBox242: MonsterNames.HellBox242,
    MonsterHunt2List.LivingDead250: MonsterNames.LivingDead250,
    MonsterHunt2List.BeeAssault273: MonsterNames.BeeAssault273,
    MonsterHunt2List.BabyWorm275: MonsterNames.BabyWorm275,
    MonsterHunt2List.Halloween283: MonsterNames.Halloween283,
}