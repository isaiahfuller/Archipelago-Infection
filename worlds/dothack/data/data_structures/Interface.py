from enum import Enum

from ...pcsx2_interface.pine import Pine


class DataType(Enum):
    BYTE = 1
    SHORT = 2
    INT = 4
    FLOAT = 5
    LONG = 8


class StructInterface:
    _length: int = 0

    def __init__(self, parent_or_pine: "Pine | StructInterface", addr: int):
        self._parent_or_pine: Pine | StructInterface = parent_or_pine
        self._base_addr: int = addr

    def __getitem__(self, item):
        # only take first index
        if isinstance(item, tuple):
            item = item[0]

        return self.__class__(self._parent_or_pine, self.__base_addr + self._length * item)

    @property
    def _pine(self):
        if isinstance(self._parent_or_pine, Pine):
            return self._parent_or_pine
        else:
            return self._parent_or_pine._pine

    @_pine.setter
    def _pine(self, value):
        if isinstance(self._parent_or_pine, Pine):
            self._parent_or_pine = value

    @property
    def _base_addr(self):
        if isinstance(self._parent_or_pine, Pine):
            return self.__base_addr
        else:
            return self._parent_or_pine._base_addr + self.__base_addr

    @_base_addr.setter
    def _base_addr(self, value):
        self.__base_addr = value


def StructField(offset: int, data_type: DataType):
    match data_type:
        case DataType.BYTE:
            getter = lambda _self: _self._pine.read_int8(_self._base_addr + offset)
            setter = lambda _self, value: _self._pine.write_int8(_self._base_addr + offset, value)
        case DataType.SHORT:
            getter = lambda _self: _self._pine.read_int16(_self._base_addr + offset)
            setter = lambda _self, value: _self._pine.write_int16(_self._base_addr + offset, value)
        case DataType.INT:
            getter = lambda _self: _self._pine.read_int32(_self._base_addr + offset)
            setter = lambda _self, value: _self._pine.write_int32(_self._base_addr + offset, value)
        case DataType.LONG:
            getter = lambda _self: _self._pine.read_int64(_self._base_addr + offset)
            setter = lambda _self, value: _self._pine.write_int64(_self._base_addr + offset, value)
        case DataType.FLOAT:
            getter = lambda _self: _self._pine.read_float
        case _:
            raise Exception("Unsupported size")
    return property(fget=getter, fset=setter)
