from dataclasses import dataclass
from typing import List


@dataclass
class FieldInfo:
    """
    Represents a single data field with its associated
    offset and index for memory address calculation.
    """
    name: str
    offset: int
    index: int

    @property
    def absolute_address(self) -> int:
        """Calculates the absolute memory address for the specific field."""
        base_address = 0x315564
        size = 0x54
        return base_address + (self.index * size + 0x4C)

    @property
    def entry_base_address(self) -> int:
        """Calculates the base address for the field entry."""
        return 0x315564 + (self.index * 0x54)


class FieldRegistry:
    """
    A utility registry that manages the mapping of field IDs
    to their respective offsets and indices.
    """

    # Data mapping: { "FieldID": (offset, index) }
    DATA = {
        "BPOAF1": (0xE, 0),
        "HFHG2": (0xF, 1),
        "EHSS3": (0x11, 2),
        "BCFW4": (0x12, 3),
        "COTH5": (0x13, 4),
        "QEWD6": (0x14, 5),
        "PSH7": (0x15, 6),
        "CMS8": (0x16, 7),
        "CDP9": (0x17, 8),
        "BPFS10": (0x18, 9),
        "LSGS11": (0x19, 10),
        "GDFLS12": (0x1A, 11),
        "CHN13": (0x1B, 12),
        "HSG14": (0x10, 13),
        "DGSD15": (0x1C, 14),
        "DPT16": (0x1D, 15),
        "IGP17": (0x1E, 16),
        "PHBS18": (0x1F, 17),
        "HDFT19": (0x20, 18),
        "SSTP20": (0x21, 19),
        "BSTG21": (0x22, 20),
        "RPM22": (0x23, 21),
        "DGM26": (0x27, 25),
        "DGS27": (0x28, 26),
        "DGNT28": (0x29, 27),
        "DGG29": (0x2A, 28),
    }

    @classmethod
    def get_all_fields(cls) -> List[FieldInfo]:
        """
        Converts the internal DATA dictionary into a list of FieldInfo objects.
        This allows other classes (like FieldLocking) to iterate over all fields.
        """
        return [
            FieldInfo(name=field_id, offset=offset, index=index)
            for field_id, (offset, index) in cls.DATA.items()
        ]

    @classmethod
    def get_field(cls, field_id: str) -> FieldInfo:
        """
        Retrieves a specific FieldInfo object by its ID.
        Throws a KeyError if the ID is not found in DATA.
        """
        offset, index = cls.DATA[field_id]
        return FieldInfo(name=field_id, offset=offset, index=index)