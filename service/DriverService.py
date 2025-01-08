from CommandEnum import CommandEnum
from ParameterStateSingleton import ParameterStateSingleton
from SerialHandler import SerialHandler
from utils.NumeralSystemUtils import NumeralSystemUtils


class DriverService:
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
        ParameterStateSingleton.set_active_channel(1)

        for instance in ParameterStateSingleton.get_all_instances():
            instance.regenerate_soft_values()
            instance.q_limits = DriverService.send_command(CommandEnum.GET_Q_LIMITS)

    @staticmethod
    def calculate_range(value_q: int, q: int):
        if value_q <= (2 ** 31) - 1:
            return value_q * 2 ** (-q)

        return - ((2 ** 32) - value_q) * 2 ** (-q)

    @staticmethod
    def get_ranges(for_voltage: bool = True) -> dict:
        p = ParameterStateSingleton.get_instance()

        return {
            'v_min' if for_voltage else 'c_min': DriverService.calculate_range(
                p.v_min if for_voltage else p.c_min,
                p.q_limits[3 if for_voltage else 5]
            ),
            'v_max' if for_voltage else 'c_max': DriverService.calculate_range(
                p.v_max if for_voltage else p.c_max,
                p.q_limits[4 if for_voltage else 6]
            ),
        }

    @staticmethod
    def calculate_adc_from_raw_value(raw_adc: float, gain: int) -> float:
        if raw_adc < 2 ** 15:
            return (1 / gain) * (62.5 * 10 ** (-6)) * raw_adc

        return (-1 * (2 ** 16 - raw_adc)) * (1 / gain) * (62.5 * 10 ** (-6))

    @staticmethod
    def active_unit(channel: int) -> None:
        if 0 > channel or channel > 7:
            raise Exception("Channel must be between 0 and 7.")

        DriverService.send_command(CommandEnum.ACTIVE_UNIT, data_lsb=channel)

        # TODO Powinniśmy trzymać konfiurację per channel. Jakby mieli się przełączać to chyba nie zmieni się konfiguracja co?
        # Trzeba to będzie też testnąć. ;)

        ParameterStateSingleton.set_active_channel(channel)

    @staticmethod
    def get_v_min() -> int:
        return NumeralSystemUtils.merge_bytes_as_decimal_command_result(
            DriverService.send_command(CommandEnum.GET_V_MIN))

    @staticmethod
    def get_v_max() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.v_max is None:
            p.v_max = NumeralSystemUtils.merge_bytes_as_decimal_command_result(
                DriverService.send_command(CommandEnum.GET_V_MAX)
            )

        return p.v_max

    @staticmethod
    def get_v_slope() -> float:
        p = ParameterStateSingleton.get_instance()

        return NumeralSystemUtils.merge_bytes_as_decimal_with_fractional_bits(
            *DriverService.send_command(CommandEnum.GET_V_SLOPE)[3:7],
            fractional_bits=DriverService.send_command(CommandEnum.GET_Q_V_SLOPE)[
                NumeralSystemUtils.calculate_byte_to_read_index(p.v_pga)]
        )

    @staticmethod
    def get_v_inter() -> float:
        p = ParameterStateSingleton.get_instance()

        return NumeralSystemUtils.merge_bytes_as_decimal_with_fractional_bits(
            *DriverService.send_command(CommandEnum.GET_V_INTER)[3:7],
            fractional_bits=DriverService.send_command(CommandEnum.GET_Q_V_INTER)[
                NumeralSystemUtils.calculate_byte_to_read_index(p.v_pga)]
        )

    @staticmethod
    def get_c_min() -> int:
        return NumeralSystemUtils.merge_bytes_as_decimal_command_result(
            DriverService.send_command(CommandEnum.GET_C_MIN))

    @staticmethod
    def get_c_max() -> int:
        return NumeralSystemUtils.merge_bytes_as_decimal_command_result(
            DriverService.send_command(CommandEnum.GET_C_MAX))

    @staticmethod
    def get_c_slope() -> float:
        p = ParameterStateSingleton.get_instance()

        return NumeralSystemUtils.merge_bytes_as_decimal_with_fractional_bits(
            *DriverService.send_command(CommandEnum.GET_C_SLOPE)[3:7],
            fractional_bits=DriverService.send_command(CommandEnum.GET_Q_C_SLOPE)[
                NumeralSystemUtils.calculate_byte_to_read_index(p.c_pga)]
        )

    @staticmethod
    def get_c_inter() -> float:
        p = ParameterStateSingleton.get_instance()

        return NumeralSystemUtils.merge_bytes_as_decimal_with_fractional_bits(
            *DriverService.send_command(CommandEnum.GET_C_INTER)[3:7],
            fractional_bits=DriverService.send_command(CommandEnum.GET_Q_C_INTER)[
                NumeralSystemUtils.calculate_byte_to_read_index(p.c_pga)]
        )

    @staticmethod
    def set_v_pga(pga: int) -> None:
        if pga not in [1, 2, 4, 8]:
            raise Exception("Unacceptable parameter PGA value. Acceptable values: 1, 2, 4, 8.")

        DriverService.send_command(CommandEnum.SET_V_PGA, data_lsb=pga)
        ParameterStateSingleton.get_instance().v_pga = pga

    @staticmethod
    def set_c_pga(pga: int) -> None:
        if pga not in [1, 2, 4, 8]:
            raise Exception("Unacceptable parameter PGA value. Acceptable values: 1, 2, 4, 8.")

        DriverService.send_command(CommandEnum.SET_C_PGA, data_lsb=pga)
        ParameterStateSingleton.get_instance().c_pga = pga

    @staticmethod
    def get_voltage_and_current() -> dict:
        voltage_and_current = DriverService.send_command(CommandEnum.GET_VOLTAGE_AND_CURRENT)

        voltage = NumeralSystemUtils.merge_bytes_as_decimal(*voltage_and_current[3:5])
        current = NumeralSystemUtils.merge_bytes_as_decimal(*voltage_and_current[5:7])

        p = ParameterStateSingleton().get_instance()

        return {
            'voltage': (DriverService.calculate_adc_from_raw_value(voltage, p.v_pga) * p.v_slope) + p.v_inter,
            'current': (DriverService.calculate_adc_from_raw_value(current, p.c_pga) * p.c_slope) + p.c_inter,
        }
