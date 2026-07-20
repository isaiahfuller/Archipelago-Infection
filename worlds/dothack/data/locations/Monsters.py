from enum import Enum
from typing import TypedDict

from ..items.Servers import Servers
from ..Addresses import MonsterNames

class MonsterAttributes(TypedDict):
    address: int
    bits: int
    volumes: list[int]
    server: Servers


class MonsterBase(Enum):
    _value_: MonsterAttributes

    @classmethod
    def from_address(self, address: int):
        for member in self:
            if member.value["address"] == address:
                return member
        return None

class InfectionMonsters(MonsterBase):
    Razine1 = {"address": 0xa46287, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Swordmanoid2 = {"address": 0xa46288, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    Ochimusha4 = {"address": 0xa4628a,"bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    HeavyMetal6 = {"address": 0xa4628c, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}


    GeneralArmor13 = {"address": 0xa46293, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Porolin14 = {"address": 0xa46294, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    MummyRipper15 = {"address": 0xa46295, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    CadetValkyrie20 = {"address": 0xa4629A, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}


    Flamer36 = {"address": 0xa462AA, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    FireWitch37 = {"address": 0xa462AB, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    WaterWitch38 = {"address": 0xa462AC, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    DarkWitch39 = {"address": 0xa462AD, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Kakasinger49 = {"address": 0xa462B7, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Guardian50 = {"address": 0xa462B8, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    MetalEmperor52 = {"address": 0xa462BA, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    Pippy67 = {"address": 0xa462C9, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    ChickenHand68 = {"address": 0xa462CA, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    WoodHarpy69 = {"address": 0xa462CB, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    MonkeyCrab80 = {"address": 0xa462D6, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    SnipSnap81 = {"address": 0xa462D7, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    CrabTurtle82 = {"address": 0xa462D8, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    SquillaDemon84 = {"address": 0xa462DA, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    ShieldMan91 = {"address": 0xa462E1, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Moai105 = {"address": 0xa462EF, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    RockHead106 = {"address": 0xa462F0, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    StoneTuttle114 = {"address": 0xa462F8, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    StoneTuttleDataBug116 = {"address": 0xa462FA, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Minnow117 = {"address": 0xa462FB, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    SkyFish118 = {"address": 0xa462FC, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    ArrowFish119 = {"address": 0xa462FD, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    CycloShark123 = {"address": 0xa46301, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    Gremlin130 = {"address": 0xa46308, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Goblin131 = {"address": 0xa46309, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Stehoney132 = {"address": 0xa4630A, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Jonue133 = {"address": 0xa4630B, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    HobGoblin140 = {"address": 0xa46312, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Zyan141 = {"address": 0xa46313, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    GoblinNight145 = {"address": 0xa46317, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    Albert148 = {"address": 0xa4631A, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    MagicalGoblin152 = {"address": 0xa4631E, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    GoblinWiz153 = {"address": 0xa4631F, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Martina155 = {"address": 0xa46321, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    LittleDoggie168 = {"address": 0xa4632E, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    SledDog169 = {"address": 0xa4632F, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    HellDoberman172 = {"address": 0xa46332, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    FlameHeads176 = {"address": 0xa46336, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    WiggleSnake179 = {"address": 0xa46339, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Menhir180 = {"address": 0xa4633A, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    FiendMenhir184 = {"address": 0xa4633E, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    LimpKnife185 = {"address": 0xa4633F, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    DiscoKnife186 = {"address": 0xa46340, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    LambadaKnife187 = {"address": 0xa46341, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    DustCurse188 = {"address": 0xa46342, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    SwordofChaos190 = {"address": 0xa46344, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    DragonPuppy194 = {"address": 0xa46348, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Snakoid195 = {"address": 0xa46349, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    RedWyrm200 = {"address": 0xa4634E, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    RedWyrmDataBug202 = {"address": 0xa46350, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    ParasiteDragon215 = {"address": 0xa4635D, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    TwinkleGrass219 = {"address": 0xa46361, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    MadGrass220 = {"address": 0xa46362, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    HungryGrass221 = {"address": 0xa46363, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    ThousandTrees224 = {"address": 0xa46366, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    WoodStockDataBug225 = {"address": 0xa46367, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    ScarletKing227 = {"address": 0xa46369, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    MushroomKing229 = {"address": 0xa4636A, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Charmer230 = {"address": 0xa4636C, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    LamiaFighter231 = {"address": 0xa4636D, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    KillerSnaker234 = {"address": 0xa46370, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    KillerSnakerDataBug236 = {"address": 0xa46372, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    FakeMoney240 = {"address": 0xa46377, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Mimic241 = {"address": 0xa46378, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    DeathHead246 = {"address": 0xa4637C, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    NomadicBones247 = {"address": 0xa4637D, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    Headhunter253 = {"address": 0xa46383, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    HeadhunterDataBug256 = {"address": 0xa46386, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Wiggly268 = {"address": 0xa46392, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    DeadlyMoth269 = {"address": 0xa46393, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    PhantomWing270 = {"address": 0xa46394, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    BeeArmy272 = {"address": 0xa46396, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    Odoro280 = {"address": 0xa4639E, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    Ectoplasm281 = {"address": 0xa46398, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    NoisyWisp282 = {"address": 0xa463A0, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    ShiningEyes288 = {"address": 0xa463A6, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}

    Gladiator3 = {"address": 0xa46289, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    DarkRider8 = {"address": 0xa4628E, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    TetraArmor11 = {"address": 0xa46291, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    FreshValkyrie21 = {"address": 0xa4629B, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    LongLived23 = {"address": 0xa4629D, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    GrandMage24 = {"address": 0xa4629E, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    MuGuardian57 = {"address": 0xa462BF, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    PhoenixQueen72 = {"address": 0xa462CE, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    RedScissors83 = {"address": 0xa462D9, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    Mantis86 = {"address": 0xa462DC, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    MysteryRock107 = {"address": 0xa462F1, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    HammerShark124 = {"address": 0xa46302, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    MetalGoblin146 = {"address": 0xa46318, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    Cannibal159 = {"address": 0xa46325, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    Ogre161 = {"address": 0xa46327, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    IronBallFreak163 = {"address": 0xa46329, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    HellHound173 = {"address": 0xa46333, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    GoilMenhir181 = {"address": 0xa4633B, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    CursedBlades189 = {"address": 0xa46343, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    ArmorShogun191 = {"address": 0xa46345, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    LeadSnakoid196 = {"address": 0xa4634A, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    SnappyGrass222 = {"address": 0xa46364, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    WoodStock223 = {"address": 0xa46365, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    LamiaHunter232 = {"address": 0xa4636E, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    HellBox242 = {"address": 0xa46379, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    LivingDead250 = {"address": 0xa46380, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    BeeAssault273 = {"address": 0xa46397, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    BabyWorm275 = {"address": 0xa46399, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    Halloween283 = {"address": 0xa463A1, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}

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