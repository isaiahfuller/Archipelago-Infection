from .Interface import StructInterface, StructField, DataType
from ..BaseStats import charData
from ...pcsx2_interface.pine import Pine


class BattleAbility(StructInterface):
    _length = 0x10

    attack = StructField(0x0, DataType.SHORT)
    defense = StructField(0x2, DataType.SHORT)
    accuracy = StructField(0x4, DataType.SHORT)
    evasion = StructField(0x6, DataType.SHORT)
    magic_attack = StructField(0x8, DataType.SHORT)
    magic_defense = StructField(0xa, DataType.SHORT)
    magic_accuracy = StructField(0xc, DataType.SHORT)
    magic_evasion = StructField(0xe, DataType.SHORT)


class Attribute(StructInterface):
    _length = 0xc

    earth = StructField(0x0, DataType.SHORT)
    water = StructField(0x2, DataType.SHORT)
    fire = StructField(0x4, DataType.SHORT)
    wood = StructField(0x6, DataType.SHORT)
    light = StructField(0x8, DataType.SHORT)
    dark = StructField(0xa, DataType.SHORT)


class Tolerance(StructInterface):
    _length = 0x4

    soul = StructField(0x0, DataType.SHORT)
    body = StructField(0x2, DataType.SHORT)


class CharParamElement(StructInterface):
    _length = 0x20

    def __init__(self, pine: Pine | object, addr: int):
        super().__init__(pine, addr)
        self.battleAbility = BattleAbility(self, 0x0)
        self.attribute = Attribute(self, 0x10)
        self.tolerance = Tolerance(self, 0x1c)


class Equipment(StructInterface):
    _length = 0xc

    head = StructField(0x0, DataType.SHORT)
    body = StructField(0x2, DataType.SHORT)
    arms = StructField(0x4, DataType.SHORT)
    legs = StructField(0x6, DataType.SHORT)
    weapon = StructField(0x8, DataType.SHORT)
    _unused = StructField(0xa, DataType.SHORT)


class SpcParam(StructInterface):
    _length = 0xdc

    name = StructField(0x0, DataType.POINTER, size=32, pointer_type=DataType.STRING)
    model = StructField(0x4, DataType.POINTER, size=32, pointer_type=DataType.STRING)
    flags = StructField(0x8, DataType.INT)
    char_id = StructField(0xc, DataType.SHORT)
    level = StructField(0xe, DataType.SHORT)
    GP = StructField(0x14, DataType.INT)
    height = StructField(0x18, DataType.FLOAT)
    width = StructField(0x1c, DataType.FLOAT)
    base_msg = StructField(0x20, DataType.INT)
    max_hp = StructField(0x24, DataType.SHORT)
    max_sp = StructField(0x26, DataType.SHORT)
    #base_charParamElement = StructField(0x28, 0x20)
    #total_charParamElement = StructField(0x48, 0x20)
    #equipment_charParamElements = StructField(0x68, 0x20)
    #status_charParamElements = StructField(0x88, 0x20)
    #other_charParamElements = StructField(0xa8, 0x20)
    #equipment = StructField(0xc8, 0xc)

    char_class = StructField(0xd8, DataType.SHORT)
    friendship = StructField(0xda, DataType.SHORT)

    def __init__(self, pine: Pine | object, addr: int):
        super().__init__(pine, addr)
        self.base_stats = CharParamElement(self, 0x28)
        self.total_stats = CharParamElement(self, 0x48)
        self.equipment_stats = CharParamElement(self,0x68)
        self.status_stats = CharParamElement(self,0x88)
        self.other_stats = CharParamElement(self,0xa8)
        self.equipment = Equipment(self, 0xc8)

    def set_level(self, level):
        if self.level == level:
            return
        stats = charData[self.char_id].get_stats_at_level(level)

        self.level = level

        self.max_hp = stats.max_hp
        self.max_sp = stats.max_sp
        self.base_stats.battleAbility.attack = stats.attack
        self.base_stats.battleAbility.defense = stats.defense
        self.base_stats.battleAbility.accuracy = stats.accuracy
        self.base_stats.battleAbility.evasion = stats.evasion
        self.base_stats.battleAbility.magic_attack = stats.magic_attack
        self.base_stats.battleAbility.magic_defense = stats.magic_defense
        self.base_stats.battleAbility.magic_accuracy = stats.magic_accuracy
        self.base_stats.battleAbility.magic_evasion = stats.magic_evasion
        self.base_stats.attribute.earth = stats.earth
        self.base_stats.attribute.water = stats.water
        self.base_stats.attribute.fire = stats.fire
        self.base_stats.attribute.wood = stats.wood
        self.base_stats.attribute.light = stats.light
        self.base_stats.attribute.dark = stats.dark
        self.base_stats.tolerance.soul = stats.soul
        self.base_stats.tolerance.body = stats.body


#class LevelUpParam(StructInterface):
#    _length = 0x24
#
#    hp = StructField(0x0, DataType.SHORT)
#    sp = StructField(0x2, DataType.SHORT)
#
#    def __init__(self, pine: Pine | object, addr: int):
#        super().__init__(pine, addr)
#        self.battleAbility = BattleAbility(self, 0x4)
#        self.attribute = Attribute(self, 0x14)
#        self.tolerance = Tolerance(self, 0x20)
