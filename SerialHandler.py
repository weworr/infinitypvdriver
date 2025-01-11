import time
import serial

from mocks.MockSerial import MockSerial

global error


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

            cls.__instance = serial.Serial(
                port,
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )

            time.sleep(2)

        return cls.__instance

    @classmethod
    def is_initialized(cls) -> bool:
        return cls.__instance is not None


def module_decorator(func: callable) -> callable:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            serial_handler = SerialHandler().get_instance()
            if 'serialHandler' in globals() and isinstance(serial_handler, serial.Serial) and serial_handler.is_open:
                serial_handler.close()

            raise e

    return wrapper


@module_decorator
def close_connection() -> str:
    SerialHandler().get_instance().close()

    return 'Closed'
