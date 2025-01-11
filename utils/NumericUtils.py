import math
from math import log2

BYTE_SIZE = 8


class NumericUtils:
    @staticmethod
    def merge_bytes_as_decimal(*numbers: int) -> int:
        result = 0
        sign = numbers[0] >> BYTE_SIZE - 1

        for number in numbers:
            result = (result << BYTE_SIZE) | number

        if sign:
            value = 1 << (len(numbers) * BYTE_SIZE - 1)
            result = result - (2 * value)

        return result

    @staticmethod
    def merge_bytes_as_decimal_command_result(command_result: list) -> int:
        """
        Zwraca oznakowaną liczbę całkowitą będącą rezultatem połączenia otrzymanych bajtów.
        Bajty wyliczane są na podstawie drugiego bajtu paczki otrzymanej od urządzenia - N_DATA.
        N_DATA zawiera informacje ile bajtów danych zostało zwróconych przez urządzenie (0, 1, 2).

        :param command_result: Rezultant komendy wysłanej do urządzenia.
        :return: Oznakowana liczba całkowita.
        """
        return NumericUtils.merge_bytes_as_decimal(*command_result[3: 3 + (command_result[2] * 2)])

    @staticmethod
    def calculate_value_from_q_format(value_q: int, q: int) -> float:
        if value_q <= (2 ** 31) - 1:
            return value_q * 2 ** (-q)

        return - ((2 ** 32) - value_q) * 2 ** (-q)

    @staticmethod
    def calculate_adc_from_raw_value(raw_adc: float, gain: int) -> float:
        if raw_adc < 2 ** 15:
            return (1 / gain) * (62.5 * 10 ** (-6)) * raw_adc

        return (-1 * (2 ** 16 - raw_adc)) * (1 / gain) * (62.5 * 10 ** (-6))

    @staticmethod
    def calculate_byte_to_read_index(pga_configuration: int) -> int:
        """
        Służy do obliczenia indeksu bajtu, który trzeba odczytać z funkcji [0x3F - 0x42]
        """
        return int(log2(pga_configuration))

    @staticmethod
    def calculate_dac(voltage: float) -> int:
        from services.DriverService import DriverService

        # TODO Sobijanek - nie podoba mi się to, że jest tutaj DriverService wpięty. xd
        return math.floor(
            4095 * (voltage - DriverService.get_v_min()) / (DriverService.get_v_max() - DriverService.get_v_min())
        )

    @staticmethod
    def calculate_voltage_from_dac(dac: int, v_min: float, v_max: float) -> float:
        
