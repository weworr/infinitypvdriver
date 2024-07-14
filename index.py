import time
import serial
from SerialHandler import SerialHandler

global error


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
def send_command() -> str:
    packet = bytearray()
    packet.append(0x66)
    packet.append(0x10)
    packet.append(0x00)
    packet.append(0x00)
    packet.append(0x00)
    packet.append(0x34)

    serialHandler.write(packet)

    return ''.join([str(int(byte)) for byte in bytearray(serialHandler.readline())])


@module_decorator
def close_connection() -> str:
    serialHandler.close()

    return 'Closed'


def wait() -> None:
    time.sleep(10)


create_instance()
