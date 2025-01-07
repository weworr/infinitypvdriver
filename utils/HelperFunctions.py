from CommandEnum import CommandEnum
from ParameterStateSingleton import ParameterStateSingleton
from SerialHandler import SerialHandler
from math import log2

BYTE_SIZE = 8


class Helper:
    @staticmethod
    def send_command(
        command: CommandEnum,
        data_msb: int = 0x00,
        data_lsb: int = 0x00
    ) -> list:
        print(f'-------------------%s-------------------' % hex(command.value))
        handler = SerialHandler.get_instance()

        handler.write(
            bytearray([0x66, command.value, data_msb, data_lsb, 0x00, 0x34])
        )

        return [byte for byte in bytearray(handler.readline())]

    @staticmethod
    def init_driver():
        p = ParameterStateSingleton.get_instance()

        p.c_pga = 1
        p.v_pga = 1
        p.q_limits = Helper.send_command(CommandEnum.GET_Q_LIMITS)

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
        return Helper.merge_bytes_as_decimal(*command_result[3: 3 + (command_result[2] * 2)])

    @staticmethod
    def calculate_range(value_q: int, q: int):
        if value_q <= (2 ** 31) - 1:
            return value_q * 2 ** (-q)

        return - ((2 ** 32) - value_q) * 2 ** (-q)

    @staticmethod
    def get_ranges(for_voltage: bool = True) -> dict:
        p = ParameterStateSingleton.get_instance()

        return {
            'v_min' if for_voltage else 'c_min': Helper.calculate_range(
                p.v_min if for_voltage else p.c_min,
                p.q_limits[3 if for_voltage else 5]
            ),
            'v_max' if for_voltage else 'c_max': Helper.calculate_range(
                p.v_max if for_voltage else p.c_max,
                p.q_limits[4 if for_voltage else 6]
            ),
        }

    @staticmethod
    def calculate_byte_to_read_index(pga_configuration: int) -> int:
        """
        Służy do obliczenia indexu bajtu, który trzeba odczytać z funkcji [0x3F - 0x42]
        """
        return int(3 + log2(pga_configuration))

    @staticmethod
    def calculate_adc_from_raw_value(raw_adc: float, gain: int) -> float:
        if raw_adc < 2 ** 15:
            return (1 / gain) * (62.5 * 10 ** (-6)) * raw_adc

        return (-1 * (2 ** 16 - raw_adc)) * (1 / gain) * (62.5 * 10 ** (-6))

    @staticmethod
    def active_unit(channel: int) -> None:
        if 0 > channel or channel > 7:
            raise Exception("Channel must be between 0 and 7.")

        Helper.send_command(CommandEnum.ACTIVE_UNIT, data_lsb=channel)

        # TODO Powinniśmy trzymać konfiurację per channel. Jakby mieli się przełączać to chyba nie zmieni się konfiguracja co?
        # Trzeba to będzie też testnąć. ;)

        ParameterStateSingleton.get_instance().active_channel = channel

    @staticmethod
    def get_v_min() -> int:
        return Helper.merge_bytes_as_decimal_command_result(Helper.send_command(CommandEnum.GET_V_MIN))

    @staticmethod
    def get_v_max() -> int:
        return Helper.merge_bytes_as_decimal_command_result(Helper.send_command(CommandEnum.GET_V_MAX))

    @staticmethod
    def get_v_slope() -> float:
        p = ParameterStateSingleton.get_instance()

        return Helper.merge_bytes_as_decimal_with_fractional_bits(
            *Helper.send_command(CommandEnum.GET_V_SLOPE)[3:7],
            fractional_bits=Helper.send_command(CommandEnum.GET_Q_V_SLOPE)[Helper.calculate_byte_to_read_index(p.v_pga)]
        )

    @staticmethod
    def get_v_inter() -> float:
        p = ParameterStateSingleton.get_instance()

        return Helper.merge_bytes_as_decimal_with_fractional_bits(
            *Helper.send_command(CommandEnum.GET_V_INTER)[3:7],
            fractional_bits=Helper.send_command(CommandEnum.GET_Q_V_INTER)[Helper.calculate_byte_to_read_index(p.v_pga)]
        )

    @staticmethod
    def get_c_min() -> int:
        return Helper.merge_bytes_as_decimal_command_result(Helper.send_command(CommandEnum.GET_C_MIN))

    @staticmethod
    def get_c_max() -> int:
        return Helper.merge_bytes_as_decimal_command_result(Helper.send_command(CommandEnum.GET_C_MAX))

    @staticmethod
    def get_c_slope() -> float:
        p = ParameterStateSingleton.get_instance()

        return Helper.merge_bytes_as_decimal_with_fractional_bits(
            *Helper.send_command(CommandEnum.GET_C_SLOPE)[3:7],
            fractional_bits=Helper.send_command(CommandEnum.GET_Q_C_SLOPE)[Helper.calculate_byte_to_read_index(p.c_pga)]
        )

    @staticmethod
    def get_c_inter() -> float:
        p = ParameterStateSingleton.get_instance()

        return Helper.merge_bytes_as_decimal_with_fractional_bits(
            *Helper.send_command(CommandEnum.GET_C_INTER)[3:7],
            fractional_bits=Helper.send_command(CommandEnum.GET_Q_C_INTER)[Helper.calculate_byte_to_read_index(p.c_pga)]
        )

    @staticmethod
    def set_v_pga(pga: int) -> None:
        if pga not in [1, 2, 4, 8]:
            raise Exception("Unacceptable parameter PGA value. Acceptable values: 1, 2, 4, 8.")

        Helper.send_command(CommandEnum.SET_V_PGA, data_lsb=pga)
        ParameterStateSingleton.get_instance().v_pga = pga

    @staticmethod
    def set_c_pga(pga: int) -> None:
        if pga not in [1, 2, 4, 8]:
            raise Exception("Unacceptable parameter PGA value. Acceptable values: 1, 2, 4, 8.")

        Helper.send_command(CommandEnum.SET_C_PGA, data_lsb=pga)
        ParameterStateSingleton.get_instance().c_pga = pga

    @staticmethod
    def get_voltage_and_current() -> dict:
        voltage_and_current = Helper.send_command(CommandEnum.GET_VOLTAGE_AND_CURRENT)

        voltage = Helper.merge_bytes_as_decimal(*voltage_and_current[3:5])
        current = Helper.merge_bytes_as_decimal(*voltage_and_current[5:7])

        p = ParameterStateSingleton().get_instance()

        return {
            'voltage': (Helper.calculate_adc_from_raw_value(voltage, p.v_pga) * p.v_slope) + p.v_inter,
            'current': (Helper.calculate_adc_from_raw_value(current, p.c_pga) * p.c_slope) + p.c_inter,
        }
