from CommandEnum import CommandEnum


class MockSerial:
    def __init__(self):
        self.__data = bytearray()

    def write(self, data: bytes) -> None:
        self.__data = data

    def readline(self) -> bytes:
        if self.__data == bytearray([0x66, CommandEnum.GET_INTERNAL_IDN.value, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 2, 0, 142, 247, 64, 0, 44, 52])

        if self.__data == bytearray([0x66, 0x2C, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 2, 0, 142, 247, 64, 0, 44, 52])

        if self.__data == bytearray([0x66, 0x3C, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 1, 0, 1, 0, 0, 0, 60, 52])

        if self.__data == bytearray([0x66, 0x38, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 2, 125, 240, 194, 48, 0, 56, 52])

        if self.__data == bytearray([0x66, 0x3F, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 2, 30, 30, 30, 29, 0, 63, 52])

        if self.__data == bytearray([0x66, 0x39, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 2, 255, 163, 64, 33, 0, 57, 52])

        if self.__data == bytearray([0x66, 0x41, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 2, 31, 31, 31, 31, 0, 65, 52])

        if self.__data == bytearray([0x66, 0x3D, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 1, 0, 1, 0, 0, 0, 61, 52])

        if self.__data == bytearray([0x66, 0x3A, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 2, 78, 228, 26, 25, 0, 58, 52])

        if self.__data == bytearray([0x66, 0x40, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 2, 26, 26, 26, 26, 0, 64, 52])

        if self.__data == bytearray([0x66, 0x3B, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 2, 255, 91, 116, 80, 0, 59, 52])

        if self.__data == bytearray([0x66, 0x42, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 2, 31, 31, 31, 31, 0, 66, 52])

        if self.__data == bytearray([0x66, 0x43, 0, 1, 0x00, 0x34]):
            return bytes([102, 1, 1, 0, 1, 0, 0, 0, 67, 52])

        if self.__data == bytearray([0x66, 0x36, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 2, 192, 0, 0, 0, 0, 54, 52])

        if self.__data == bytearray([0x66, 0x37, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 2, 80, 197, 155, 50, 0, 55, 52])

        if self.__data == bytearray([0x66, 0x3E, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 2, 28, 28, 30, 25, 0, 62, 52])

        if self.__data == bytearray([0x66, 0x34, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 2, 191, 235, 254, 226, 0, 52, 52])

        if self.__data == bytearray([0x66, 0x35, 0, 0, 0x00, 0x34]):
            return bytes([102, 1, 2, 63, 120, 83, 223, 0, 53, 52])
