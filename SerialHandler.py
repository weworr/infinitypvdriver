import serial


class SerialHandler:
    __instance = None

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls) -> serial.Serial:
        if cls.__instance is None:
            cls.instance = serial.Serial(
                'COM11',
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )

        return cls.__instance
