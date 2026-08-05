from enum import Enum
from typing import TypedDict


class InfectionSanityAttributes(TypedDict):
    address: int
    bits: int
    volumes: list[int]


class InfectionSanityBase(Enum):
    _value_: InfectionSanityAttributes

    @classmethod
    def from_address(cls, address: int):
        for member in cls:
            if member.value["address"] == address:
                return member
        return None


class InfectionShopsanity(InfectionSanityBase):
    #Mac Anu AP Items
    MAWS1 = {"address": 0xa47e05, "bits": 0b00000001, "volumes": [1]}
    MAWS2 = {"address": 0xa47e05, "bits": 0b00000010, "volumes": [1]}
    MAWS3 = {"address": 0xa47E05, "bits": 0b00000100, "volumes": [1]}
    MAWS4 = {"address": 0xa47E05, "bits": 0b00001000, "volumes": [1]}
    MAWS5 = {"address": 0xa47E05, "bits": 0b00010000, "volumes": [1]}
    MAIS1 = {"address": 0xa47E05, "bits": 0b00100000, "volumes": [1]}
    MAIS2 = {"address": 0xa47E05, "bits": 0b01000000, "volumes": [1]}
    MAIS3 = {"address": 0xa47E05, "bits": 0b10000000, "volumes": [1]}
    MAIS4 = {"address": 0xa47E06, "bits": 0b00000001, "volumes": [1]}
    MAIS5 = {"address": 0xa47E06, "bits": 0b00000010, "volumes": [1]}
    MAMS1 = {"address": 0xa47E06, "bits": 0b00000100, "volumes": [1]}
    MAMS2 = {"address": 0xa47E06, "bits": 0b00001000, "volumes": [1]}
    MAMS3 = {"address": 0xa47E06, "bits": 0b00010000, "volumes": [1]}
    MAMS4 = {"address": 0xa47E06, "bits": 0b00100000, "volumes": [1]}
    MAMS5 = {"address": 0xa47E06, "bits": 0b01000000, "volumes": [1]}
    #Dun Loireag AP Items
    DLWS1 = {"address": 0xa47e07, "bits": 0b00000001, "volumes": [1]}
    DLWS2 = {"address": 0xa47e07, "bits": 0b00000010, "volumes": [1]}
    DLWS3 = {"address": 0xa47E07, "bits": 0b00000100, "volumes": [1]}
    DLWS4 = {"address": 0xa47E07, "bits": 0b00001000, "volumes": [1]}
    DLWS5 = {"address": 0xa47E07, "bits": 0b00010000, "volumes": [1]}
    DLIS1 = {"address": 0xa47E07, "bits": 0b00100000, "volumes": [1]}
    DLIS2 = {"address": 0xa47E07, "bits": 0b01000000, "volumes": [1]}
    DLIS3 = {"address": 0xa47E07, "bits": 0b10000000, "volumes": [1]}
    DLIS4 = {"address": 0xa47E08, "bits": 0b00000001, "volumes": [1]}
    DLIS5 = {"address": 0xa47E08, "bits": 0b00000010, "volumes": [1]}
    DLMS1 = {"address": 0xa47E08, "bits": 0b00000100, "volumes": [1]}
    DLMS2 = {"address": 0xa47E08, "bits": 0b00001000, "volumes": [1]}
    DLMS3 = {"address": 0xa47E08, "bits": 0b00010000, "volumes": [1]}
    DLMS4 = {"address": 0xa47E08, "bits": 0b00100000, "volumes": [1]}
    DLMS5 = {"address": 0xa47E08, "bits": 0b01000000, "volumes": [1]}
