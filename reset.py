import serial
import sys

def main() -> None:
    serial_handler = serial.Serial(
        sys.argv[1],
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

    packet = bytearray()
    packet.append(0x66)
    packet.append(0x10)
    packet.append(0x00)
    packet.append(0x00)
    packet.append(0x00)
    packet.append(0x34)

    serial_handler.write(packet)


if __name__ == '__main__':
    main()
