from SerialHandler import SerialHandler
from io import TextIOWrapper

BYTE_SIZE = 8

class Helper:
    @staticmethod
    def merge_with_fractional_bits(*numbers: int, fractional_bits: int, signed: bool = False) -> float:
        result = 0.0

        sign = numbers[0] >> BYTE_SIZE - 1
        starting_pow = (len(numbers) * BYTE_SIZE - fractional_bits) - 1
        current_pow = starting_pow

        for number in numbers:
            for bit in bin(number)[2:].zfill(8):
                result += int(bit) * 2 ** current_pow
                current_pow -= 1

        if signed and sign:
            result -= 2 * 2 ** starting_pow

        return result

    @staticmethod
    def merge(*numbers: int, signed: bool = False) -> int:
        result = 0

        sign = numbers[0] >> BYTE_SIZE - 1

        for number in numbers:
            result = (result << BYTE_SIZE) | number

        if signed and sign:
            value = 1 << (len(numbers) * BYTE_SIZE - 1)
            result = result - (2 * value)

        return result

    @staticmethod
    def merge_command_result(command_result: list, signed: bool = False) -> int:
        return Helper.merge(*command_result[3: 3 + (command_result[2] * 2)], signed=signed)

    @staticmethod
    def send_command(
        file: TextIOWrapper,
        command: int,
        data_msb: int = 0x00,
        data_lsb: int = 0x00
    ) -> list:
        print(f'-------------------%s-------------------' % hex(command))
        handler = SerialHandler.get_instance()

        packet = bytearray([0x66, command, data_msb, data_lsb, 0x00, 0x34])
        # packet.append(0x66)
        # packet.append(command)
        # packet.append(data_msb)
        # packet.append(data_lsb)
        # packet.append(0x00)
        # packet.append(0x34)

        handler.write(packet)

        raw_response = bytearray(handler.readline())

        print([hex(byte) for byte in raw_response[3:7]])

        response = [byte for byte in raw_response]

        print(response)
        file.write(f"command: {command}, data_msb {data_msb}, data_lsb {data_lsb}, response {response}\n")

        return response

    @staticmethod
    def calculate_range(value_q: int, q: int):
        if value_q <= (2 ** 31) - 1:
            return value_q * 2 ** (-q)

        return - ((2 ** 32) - value_q) * 2 ** (-q)

    @staticmethod
    def get_ranges(file: TextIOWrapper, for_voltage: bool = True) -> dict:
        min = Helper.merge_command_result(Helper.send_command(file, 0x34 if for_voltage else 0x36), True)
        max = Helper.merge_command_result(Helper.send_command(file, 0x35 if for_voltage else 0x37), True)
        q_limits = Helper.send_command(file, 0x3E)

        return {
            'v_min' if for_voltage else 'c_min': Helper.calculate_range(
                min,
                q_limits[3 if for_voltage else 5]
            ),
            'v_max' if for_voltage else 'c_max': Helper.calculate_range(
                max,
                q_limits[4 if for_voltage else 6]
            ),
        }

    @staticmethod
    def calculate_adc_from_raw_value(raw_adc: float, gain: int) -> float:
        print(f"rawadc {raw_adc}")
        if raw_adc < 2 ** 15:
            return (1 / gain) * (62.5 * 10 ** (-6)) * raw_adc

        return (-1 * (2 ** 16 - raw_adc)) * (1 / gain) * (62.5 * 10 ** (-6))
