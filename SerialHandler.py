import time
import serial

global error

class SerialHandler:
    __instance: serial.Serial|None = None

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls, port: str|None = None) -> serial.Serial:
        if cls.__instance is None:
            if port is None:
                raise RuntimeError("Port must be specified before serial handler initialisation")

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


def module_decorator(func: callable) -> callable:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:  
            if 'serialHandler' in globals() and isinstance(serialHandler, serial.Serial) and serialHandler.is_open:
                serialHandler.close()

            raise e

    return wrapper


@module_decorator
def create_instance() -> str:
    global serialHandler
    serialHandler = SerialHandler().get_instance()

    return 'Open'

@module_decorator
def close_connection() -> str:
    serialHandler.close()

    return 'Closed'


def wait() -> None:
    time.sleep(10)
