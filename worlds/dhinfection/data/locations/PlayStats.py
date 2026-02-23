from enum import IntEnum, IntFlag


class InfectionRyuBookI(IntEnum):
    _value_: int
    AreasVisited = 0xa46232


class InfectionRyuBookII(IntEnum):
    _value_: int
    PortalsOpened = 0xa46234
    AllFieldPortalsOpened = 0xa46236
    AllDungeonPortalsOpened = 0xa46238


class InfectionAffection(IntEnum):
    _value_: int
    Orca = 0xa470ea
    Sanjuro = 0xa472a2
    Piros = 0xa47612
    Natsume = 0xa478a6
    Gardenia = 0xa47a5e
    BlackRose = 0xa47c16
    Mistral = 0xa47cf2


class InfectionOtherStats(IntEnum):
    _value_: int
    TotalDataDrains = 0xa4622e
