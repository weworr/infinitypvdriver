from math import log2

BYTE_SIZE = 8


class NumeralSystemUtils:
    @staticmethod
    def merge_bytes_as_decimal(*numbers: int, signed: bool = True) -> int:
        result = 0
        sign = numbers[0] >> BYTE_SIZE - 1

        for number in numbers:
            result = (result << BYTE_SIZE) | number

        if signed and sign:
            value = 1 << (len(numbers) * BYTE_SIZE - 1)
            result = result - (2 * value)

        return result

    @staticmethod
    def merge_bytes_as_decimal_with_fractional_bits(*numbers: int, fractional_bits: int) -> float:
        result = 0.0

        sign = numbers[0] >> BYTE_SIZE - 1
        starting_pow = (len(numbers) * BYTE_SIZE - fractional_bits) - 1
        current_pow = starting_pow

        for number in numbers:
            for bit in bin(number)[2:].zfill(8):
                result += int(bit) * 2 ** current_pow
                current_pow -= 1

        if sign:
            result -= 2 * 2 ** starting_pow

        return result

    @staticmethod
    def merge_bytes_as_decimal_command_result(command_result: list) -> int:
        return NumeralSystemUtils.merge_bytes_as_decimal(*command_result[3: 3 + (command_result[2] * 2)])

    @staticmethod
    def calculate_byte_to_read_index(pga_configuration: int) -> int:
        """
        Służy do obliczenia indeksu bajtu, który trzeba odczytać z funkcji [0x3F - 0x42]
        """
        return int(3 + log2(pga_configuration))
