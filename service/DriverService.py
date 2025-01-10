from enums.CommandEnum import CommandEnum
from ParameterStateSingleton import ParameterStateSingleton
from SerialHandler import SerialHandler
from enums.ModeEnum import ModeEnum
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
    def init_driver():
        ParameterStateSingleton.set_active_channel(1)

        for instance in ParameterStateSingleton.get_all_instances():
            instance.regenerate_soft_values()

            q_limits = DriverService.send_command(CommandEnum.GET_Q_LIMITS)[3:7]
            instance.q_limits_v_min = q_limits[0]
            instance.q_limits_v_max = q_limits[1]
            instance.q_limits_c_min = q_limits[2]
            instance.q_limits_c_max = q_limits[3]

    @staticmethod
    def active_unit(channel: int) -> None:
        if 0 > channel or channel > 7:
            raise Exception("Channel must be between 0 and 7.")

        DriverService.send_command(CommandEnum.ACTIVE_UNIT, data_lsb=channel)

        # TODO Powinniśmy trzymać konfiurację per channel. Jakby mieli się przełączać to chyba nie zmieni się konfiguracja co?
        #   Trzeba to będzie też testnąć. ;)

        ParameterStateSingleton.set_active_channel(channel)

    @staticmethod
    def get_v_min() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.v_min is None:
            NumeralSystemUtils.merge_bytes_as_decimal_command_result(
                DriverService.send_command(CommandEnum.GET_V_MIN)
            )

        return p.v_min

    @staticmethod
    def get_v_max() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.v_max is None:
            p.v_max = NumeralSystemUtils.merge_bytes_as_decimal_command_result(
                DriverService.send_command(CommandEnum.GET_V_MAX)
            )

        return p.v_max

    @staticmethod
    def get_c_min() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.c_min is None:
            p.c_min = NumeralSystemUtils.merge_bytes_as_decimal_command_result(
                DriverService.send_command(CommandEnum.GET_C_MIN)
            )

        return p.c_min

    @staticmethod
    def get_c_max() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.c_max is None:
            p.c_max = NumeralSystemUtils.merge_bytes_as_decimal_command_result(
                DriverService.send_command(CommandEnum.GET_C_MAX)
            )

        return p.c_max

    @staticmethod
    def get_q_limits() -> dict:
        p = ParameterStateSingleton.get_instance()

        if (
                p.q_limits_v_min is None
                or p.q_limits_v_max is None
                or p.q_limits_c_min is None
                or p.q_limits_c_max is None
        ):
            DriverService.__set_q_limits()

        return {
            'v_min': p.q_limits_v_min,
            'v_max': p.q_limits_v_max,
            'c_min': p.q_limits_c_min,
            'c_max': p.q_limits_c_max
        }

    @staticmethod
    def get_q_limits_v_min() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.q_limits_v_min is None:
            DriverService.__set_q_limits()

        return p.q_limits_v_min

    @staticmethod
    def get_q_limits_v_max() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.q_limits_v_max is None:
            DriverService.__set_q_limits()

        return p.q_limits_v_max

    @staticmethod
    def get_q_limits_c_min() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.q_limits_c_min is None:
            DriverService.__set_q_limits()

        return p.q_limits_c_min

    @staticmethod
    def get_q_limits_c_max() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.q_limits_c_max is None:
            DriverService.__set_q_limits()

        return p.q_limits_c_max

    @staticmethod
    def __set_q_limits() -> None:
        p = ParameterStateSingleton.get_instance()

        q_limits = DriverService.send_command(CommandEnum.GET_Q_LIMITS)[3:7]
        p.q_limits_v_min = q_limits[0]
        p.q_limits_v_max = q_limits[1]
        p.q_limits_c_min = q_limits[2]
        p.q_limits_c_max = q_limits[3]

    @staticmethod
    def get_v_pga() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.v_pga is None:
            p.v_pga = NumeralSystemUtils.merge_bytes_as_decimal_command_result(
                DriverService.send_command(CommandEnum.GET_V_PGA)
            )

        return p.v_pga

    @staticmethod
    def get_c_pga() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.c_pga is None:
            p.c_pga = NumeralSystemUtils.merge_bytes_as_decimal_command_result(
                DriverService.send_command(CommandEnum.GET_C_PGA)
            )

        return p.c_pga

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
    def get_v_slope() -> float:
        p = ParameterStateSingleton.get_instance()

        if p.v_slope is None:
            p.v_slope = NumeralSystemUtils.merge_bytes_as_decimal_with_fractional_bits(
                *DriverService.send_command(CommandEnum.GET_V_SLOPE)[3:7],
                fractional_bits=DriverService.get_current_q_v_slope()
            )

        return p.v_slope

    @staticmethod
    def get_v_inter() -> float:
        p = ParameterStateSingleton.get_instance()

        if p.v_inter is None:
            p.v_inter = NumeralSystemUtils.merge_bytes_as_decimal_with_fractional_bits(
                *DriverService.send_command(CommandEnum.GET_V_INTER)[3:7],
                fractional_bits=DriverService.get_current_q_v_inter()
            )

        return p.v_inter

    @staticmethod
    def get_c_slope() -> float:
        p = ParameterStateSingleton.get_instance()

        if p.c_slope is None:
            p.c_slope = NumeralSystemUtils.merge_bytes_as_decimal_with_fractional_bits(
                *DriverService.send_command(CommandEnum.GET_C_SLOPE)[3:7],
                fractional_bits=DriverService.get_current_q_c_slope()
            )

        return p.c_slope

    @staticmethod
    def get_c_inter() -> float:
        p = ParameterStateSingleton.get_instance()

        if p.c_inter is None:
            p.c_inter = NumeralSystemUtils.merge_bytes_as_decimal_with_fractional_bits(
                *DriverService.send_command(CommandEnum.GET_C_INTER)[3:7],
                fractional_bits=DriverService.get_current_q_c_inter()
            )

        return p.c_inter

    @staticmethod
    def get_q_v_slope() -> list:
        p = ParameterStateSingleton.get_instance()

        if not p.q_v_slope:
            p.q_v_slope = DriverService.send_command(CommandEnum.GET_Q_V_SLOPE)[3:7]

        return p.q_v_slope

    @staticmethod
    def get_current_q_v_slope() -> int:
        return DriverService.get_q_v_slope()[NumeralSystemUtils.calculate_byte_to_read_index(DriverService.get_v_pga())]

    @staticmethod
    def get_q_c_slope() -> list:
        p = ParameterStateSingleton.get_instance()

        if not p.q_c_slope:
            p.q_c_slope = DriverService.send_command(CommandEnum.GET_Q_C_SLOPE)[3:7]

        return p.q_c_slope

    @staticmethod
    def get_current_q_c_slope() -> int:
        return DriverService.get_q_c_slope()[NumeralSystemUtils.calculate_byte_to_read_index(DriverService.get_c_pga())]

    @staticmethod
    def get_q_v_inter() -> list:
        p = ParameterStateSingleton.get_instance()

        if not p.q_v_inter:
            p.q_v_inter = DriverService.send_command(CommandEnum.GET_Q_V_INTER)[3:7]

        return p.q_v_inter

    @staticmethod
    def get_current_q_v_inter() -> int:
        return DriverService.get_q_v_inter()[NumeralSystemUtils.calculate_byte_to_read_index(DriverService.get_v_pga())]

    @staticmethod
    def get_q_c_inter() -> list:
        p = ParameterStateSingleton.get_instance()

        if not p.q_c_inter:
            p.q_c_inter = DriverService.send_command(CommandEnum.GET_Q_C_INTER)[3:7]

        return p.q_c_inter

    @staticmethod
    def get_current_q_c_inter() -> int:
        return DriverService.get_q_c_inter()[NumeralSystemUtils.calculate_byte_to_read_index(DriverService.get_c_pga())]

    @staticmethod
    def set_mode(mode: str) -> None:
        p = ParameterStateSingleton.get_instance()

        match mode:
            case ModeEnum.VFIX.name:
                mode_enum = ModeEnum.VFIX
            case ModeEnum.MPPT.name:
                mode_enum = ModeEnum.MPPT
            case _:
                raise Exception("Unsupported working mode. Available working modes are 'VFIX' and 'MPPT'.")

        DriverService.send_command(CommandEnum.SET_MODE, mode_enum.value)
        p.mode = mode_enum.name

    @staticmethod
    def get_mode() -> str:
        p = ParameterStateSingleton.get_instance()

        if p.mode is None:
            p.mode = NumeralSystemUtils.merge_bytes_as_decimal_command_result(
                DriverService.send_command(CommandEnum.SET_MODE)
            )

        return p.mode

    @staticmethod
    def set_v_ref(v_ref: int) -> None:
        DriverService.send_command(
            CommandEnum.SET_V_REF,
            v_ref
        )

        ParameterStateSingleton.get_instance().v_ref = v_ref

    @staticmethod
    def get_voltage_and_current() -> dict:
        raw_voltage_and_current = DriverService.send_command(CommandEnum.GET_VOLTAGE_AND_CURRENT)

        # TODO może dodać voltage i current do state'a? Jakby się odpytywać o to bez przesunięcia vref to bez sensu obliczać jeszcze raz.
        raw_voltage = NumeralSystemUtils.merge_bytes_as_decimal(*raw_voltage_and_current[3:5])
        raw_current = NumeralSystemUtils.merge_bytes_as_decimal(*raw_voltage_and_current[5:7])

        return {
            'voltage': (
                           DriverService.calculate_adc_from_raw_value(raw_voltage, DriverService.get_v_pga())
                           * DriverService.get_v_slope()
                       ) + DriverService.get_v_inter(),
            'current': (
                           DriverService.calculate_adc_from_raw_value(raw_current, DriverService.get_c_pga())
                           * DriverService.get_c_slope()
                       ) + DriverService.get_c_inter(),
        }
