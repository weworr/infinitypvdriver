import time
import serial

from tests.mocks.MockSerial import MockSerial


MOCK = True


class SerialHandler:
    __instance: serial.Serial | MockSerial | None = None

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls, port: str | None = 'COM11') -> serial.Serial:
        if cls.__instance is None:
            if port is None:
                raise RuntimeError('Port must be specified before serial handler initialisation.')

            if MOCK:
                cls.__instance = MockSerial()
                return cls.__instance

            try:
                cls.__instance = serial.Serial(
                    port,
                    baudrate=9600,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1
                )
            except Exception as e:
                cls.__close_connection()

                raise e
            finally:
                time.sleep(2)

        return cls.__instance

    @classmethod
    def is_initialized(cls) -> bool:
        return cls.__instance is not None

    @classmethod
    def __close_connection(cls) -> str:
        if cls.__instance is not None:
            cls.__instance.close()
            cls.__instance = None

        return 'Closed'
