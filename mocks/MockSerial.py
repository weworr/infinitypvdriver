from enums.CommandEnum import CommandEnum


class MockSerial:
    def __init__(self):
        self.__data = bytearray()

    def write(self, data: bytes) -> None:
        self.__data = data

    def readline(self) -> bytes:
        print(self.__data[1])
        match self.__data[1]:
            case CommandEnum.GET_INTERNAL_IDN.value:
                return bytes([102, 1, 2, 0, 142, 247, 64, 0, 44, 52])

            case CommandEnum.ACTIVE_UNIT.value:
                return bytes([102, 1, 1, 0, self.__data[4], 0, 0, 0, 41, 52])

            case CommandEnum.GET_UNIT_IDN.value:
                return bytes([102, 1, 1, 0, 142, 247, 64, 0, 41, 52])

            case CommandEnum.GET_V_MIN.value:
                return bytes([102, 1, 2, 191, 235, 254, 226, 0, 52, 52])

            case CommandEnum.GET_V_MAX.value:
                return bytes([102, 1, 2, 63, 120, 83, 223, 0, 53, 52])

            case CommandEnum.GET_C_MIN.value:
                return bytes([102, 1, 2, 192, 0, 0, 0, 0, 54, 52])

            case CommandEnum.GET_C_MAX.value:
                return bytes([102, 1, 2, 80, 197, 155, 50, 0, 55, 52])

            case CommandEnum.GET_Q_LIMITS.value:
                return bytes([102, 1, 2, 28, 28, 30, 25, 0, 62, 52])

            case CommandEnum.GET_V_PGA.value:
                return bytes([102, 1, 1, 0, 1, 0, 0, 0, 60, 52])  # Powinno zwracać 1, 2, 4 lub 8

            case CommandEnum.GET_C_PGA.value:
                return bytes([102, 1, 1, 0, 1, 0, 0, 0, 61, 52])  # Powinno zwracać 1, 2, 4 lub 8

            case CommandEnum.SET_V_PGA.value:
                return bytes([102, 1, 1, 0, self.__data[4], 0, 0, 0, 67, 52])

            case CommandEnum.SET_C_PGA.value:
                return bytes([102, 1, 2, 0, 0, 0, 0, 0, 44, 52])  # Invalid

            case CommandEnum.GET_V_SLOPE.value:
                return bytes([102, 1, 2, 125, 240, 194, 48, 0, 56, 52])

            case CommandEnum.GET_V_INTER.value:
                return bytes([102, 1, 2, 255, 163, 64, 33, 0, 57, 52])

            case CommandEnum.GET_C_SLOPE.value:
                return bytes([102, 1, 2, 78, 228, 26, 25, 0, 58, 52])

            case CommandEnum.GET_C_INTER.value:
                return bytes([102, 1, 2, 255, 91, 116, 80, 0, 59, 52])

            case CommandEnum.GET_Q_V_SLOPE.value:
                return bytes([102, 1, 2, 30, 30, 30, 29, 0, 63, 52])

            case CommandEnum.GET_Q_C_SLOPE.value:
                return bytes([102, 1, 2, 26, 26, 26, 26, 0, 64, 52])

            case CommandEnum.GET_Q_V_INTER.value:
                return bytes([102, 1, 2, 31, 31, 31, 31, 0, 65, 52])

            case CommandEnum.GET_Q_C_INTER.value:
                return bytes([102, 1, 2, 31, 31, 31, 31, 0, 66, 52])

            case CommandEnum.SET_MODE.value:
                return bytes([102, 1, 2, 0, 0, 0, 0, 0, 44, 52])  # Invalid

            case CommandEnum.GET_MODE.value:
                return bytes([102, 1, 2, 0, 0, 0, 0, 0, 44, 52])  # Invalid

            case CommandEnum.SET_V_REF.value:
                return bytes([102, 1, 2, 0, 0, 0, 0, 0, 44, 52])  # Invalid

            case CommandEnum.GET_VOLTAGE_AND_CURRENT.value:
                return bytes([102, 1, 2, 0, 142, 247, 64, 0, 44, 52])
