from .Interface import StructInterface, StructField, DataType


class APMessage(StructInterface):
    _length = 0x46

    status = StructField(0x0, DataType.BYTE)
    queue_pos = StructField(0x1, DataType.BYTE)
    color = StructField(0x2, DataType.BYTE)
    type = StructField(0x3, DataType.BYTE)
    time = StructField(0x4, DataType.SHORT)
    text = StructField(0x6, DataType.STRING, 64)
