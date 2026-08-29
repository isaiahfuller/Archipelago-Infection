from enum import Enum
import struct

from ...pcsx2_interface.pine import Pine


class DataType(Enum):
    BYTE = 1
    SHORT = 2
    INT = 4
    FLOAT = 5
    LONG = 8
    STRING = 9
    POINTER = 10


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


class PinePointer:
    def __init__(self, pine: Pine, address: int, data_type: DataType, depth: int = 1, size: int = 0):
        self._pine: Pine = pine
        self.address: int = address
        self.data_type: DataType = data_type
        self.depth: int = depth
        self.size: int = size

    def __getitem__(self, item):
        # only take first index
        if isinstance(item, tuple):
            item = item[0]

        if self.depth > 1:
            data_size = 4
        else:
            data_size = 1
            match self.data_type:
                case DataType.BYTE:
                    data_size = 1
                case DataType.SHORT:
                    data_size = 2
                case DataType.INT:
                    data_size = 4
                case DataType.LONG:
                    data_size = 8
                case DataType.FLOAT:
                    data_size = 4
                case DataType.STRING:
                    data_size = 1
                case DataType.POINTER:
                    data_size = 4
                case _:
                    raise Exception("Unsupported data type")

        return PinePointer(self._pine, self.address + data_size * item, self.data_type, self.depth, self.size)

    def __add__(self, num):
        return PinePointer(self._pine, self.address + num, self.data_type, self.depth, self.size)

    def __sub__(self, num):
        return PinePointer(self._pine, self.address - num, self.data_type, self.depth, self.size)

    @property
    def value(self):
        if self.depth > 1:
            return PinePointer(self._pine, self._pine.read_int32(self.address), self.data_type, self.depth-1, self.size)

        match self.data_type:
            case DataType.BYTE:
                return self._pine.read_int8(self.address)
            case DataType.SHORT:
                return self._pine.read_int16(self.address)
            case DataType.INT:
                return self._pine.read_int32(self.address)
            case DataType.LONG:
                return self._pine.read_int64(self.address)
            case DataType.FLOAT:
                return read_float(self._pine, self.address)
            case DataType.STRING:
                return until_zero(self._pine.read_bytes(self.address, self.size)).decode("shift-jis")
            case _:
                raise Exception("Unsupported data type")

    @value.setter
    def value(self, value):
        if self.depth > 1:
            self._pine.write_int32(self.address, value)
            return

        match self.data_type:
            case DataType.BYTE:
                self._pine.write_int8(self.address, value)
            case DataType.SHORT:
                self._pine.write_int16(self.address, value)
            case DataType.INT:
                self._pine.write_int32(self.address, value)
            case DataType.LONG:
                self._pine.write_int64(self.address, value)
            case DataType.FLOAT:
                self._pine.write_float(self.address, value)
            case DataType.STRING:
                self._pine.write_bytes(self.address, encode_string(value, self.size, "shift-jis"))
            case _:
                raise Exception("Unsupported data type")


def encode_string(text: str, max_length: int, encoding: str) -> bytes:
    text_bytes = bytes([*text.encode(encoding), 0])
    if len(text_bytes) > max_length:
        print(f"text too long ({len(text_bytes)} bytes)")
        return bytes(0)
    else:
        return text_bytes


def until_zero(x):
    return x[:x.index(0)]


def read_float(pine: Pine, address) -> float:
    request = Pine._create_request(Pine.IPCCommand.READ32, address, 9)
    return struct.unpack("<f", pine._send_request(request)[-4:])[0]


def StructField(offset: int, data_type: DataType, size: int = 0, pointer_type: type[StructInterface] | DataType = None, pointer_depth: int = 1):
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
            getter = lambda _self: read_float(_self._pine, _self._base_addr + offset)
            setter = lambda _self, value: _self._pine.write_float(_self._base_addr + offset, value)
        case DataType.STRING:
            getter = lambda _self: until_zero(_self._pine.read_bytes(_self._base_addr + offset, size)).decode("shift-jis")
            setter = lambda _self, value: _self._pine.write_bytes(_self._base_addr + offset, encode_string(value, size, "shift-jis"))
        case DataType.POINTER:
            if isinstance(pointer_type, DataType):
                getter = lambda _self: PinePointer(_self._pine, _self._pine.read_int32(_self._base_addr + offset), pointer_type, pointer_depth, size)
                setter = lambda _self, value: _self._pine.write_int32(_self._base_addr + offset, value)
            else:
                getter = lambda _self: pointer_type(_self._pine, _self._pine.read_int32(_self._base_addr + offset))
                setter = lambda _self, value: _self._pine.write_int32(_self._base_addr + offset, value)
        case _:
            raise Exception("Unsupported data type")
    return property(fget=getter, fset=setter)
