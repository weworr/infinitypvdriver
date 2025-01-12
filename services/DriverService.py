from SerialHandler import SerialHandler
from enums.CommandEnum import CommandEnum
from ParameterStateSingleton import ParameterStateSingleton
from enums.ModeEnum import ModeEnum
from logger.LoggerDecorator import command_logger
from utils.NumericUtils import NumericUtils


class DriverService:
    @command_logger
    @staticmethod
    def __send_command(
            command: CommandEnum,
            data_msb: int = 0x00,
            data_lsb: int = 0x00
    ) -> list:
        handler = SerialHandler.get_instance()

        handler.write(
            bytearray([0x66, command.value, data_msb, data_lsb, 0x00, 0x34])
        )

        return [byte for byte in bytearray(handler.readline())]

    @staticmethod
    def __calculate_value_from_q_format(command: CommandEnum, q: int) -> float:
        return NumericUtils.calculate_value_from_q_format(
            NumericUtils.merge_bytes_as_decimal_command_result(
                DriverService.__send_command(command)
            ),
            q
        )

    @staticmethod
    def __set_q_limits() -> None:
        p = ParameterStateSingleton.get_instance()

        q_limits = DriverService.__send_command(CommandEnum.GET_Q_LIMITS)[3:7]
        p.q_limits_v_min = q_limits[0]
        p.q_limits_v_max = q_limits[1]
        p.q_limits_c_min = q_limits[2]
        p.q_limits_c_max = q_limits[3]

    @staticmethod
    def init_driver():
        ParameterStateSingleton.set_active_channel(1)

        for instance in ParameterStateSingleton.get_all_instances():
            instance.regenerate_soft_values()

            q_limits = DriverService.__send_command(CommandEnum.GET_Q_LIMITS)[3:7]
            instance.q_limits_v_min = q_limits[0]
            instance.q_limits_v_max = q_limits[1]
            instance.q_limits_c_min = q_limits[2]
            instance.q_limits_c_max = q_limits[3]

    @staticmethod
    def get_internal_idn() -> int:
        return NumericUtils.merge_bytes_as_decimal(
            *DriverService.__send_command(CommandEnum.GET_INTERNAL_IDN)[3:7],
        )

    @staticmethod
    def active_unit(channel: int) -> None:
        if channel < 0 or channel > 7:
            raise Exception('Channel must be between 0 and 7.')

        DriverService.__send_command(CommandEnum.ACTIVE_UNIT, data_lsb=channel)

        # TODO Do weryfikacji. Powinniśmy trzymać konfiurację per channel.
        #  Jakby mieli się przełączać to chyba nie zmieni się konfiguracja co?
        #  Trzeba to będzie też testnąć. ;)

        ParameterStateSingleton.set_active_channel(channel)

    @staticmethod
    def get_unit_idn() -> int:
        return NumericUtils.merge_bytes_as_decimal(*DriverService.__send_command(CommandEnum.GET_UNIT_IDN)[3:7])

    @staticmethod
    def get_v_min() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.v_min is None:
            p.v_min = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_V_MIN,
                DriverService.get_q_limits_v_min()
            )

        return p.v_min

    @staticmethod
    def get_v_max() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.v_max is None:
            p.v_max = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_V_MAX,
                DriverService.get_q_limits_v_max()
            )

        return p.v_max

    @staticmethod
    def get_c_min() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.c_min is None:
            p.c_min = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_C_MIN,
                DriverService.get_q_limits_c_min()
            )

        return p.c_min

    @staticmethod
    def get_c_max() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.c_max is None:
            p.c_max = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_C_MAX,
                DriverService.get_q_limits_c_max()
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
    def get_v_pga() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.v_pga is None:
            p.v_pga = NumericUtils.merge_bytes_as_decimal_command_result(
                DriverService.__send_command(CommandEnum.GET_V_PGA)
            )

        return p.v_pga

    @staticmethod
    def get_c_pga() -> int:
        p = ParameterStateSingleton.get_instance()

        if p.c_pga is None:
            p.c_pga = NumericUtils.merge_bytes_as_decimal_command_result(
                DriverService.__send_command(CommandEnum.GET_C_PGA)
            )

        return p.c_pga

    @staticmethod
    def set_v_pga(pga: int) -> None:
        if pga not in [1, 2, 4, 8]:
            raise Exception('Unacceptable parameter PGA value. Acceptable values: 1, 2, 4, 8.')

        DriverService.__send_command(CommandEnum.SET_V_PGA, data_lsb=pga)
        ParameterStateSingleton.get_instance().v_pga = pga

    @staticmethod
    def set_c_pga(pga: int) -> None:
        if pga not in [1, 2, 4, 8]:
            raise Exception('Unacceptable parameter PGA value. Acceptable values: 1, 2, 4, 8.')

        DriverService.__send_command(CommandEnum.SET_C_PGA, data_lsb=pga)
        ParameterStateSingleton.get_instance().c_pga = pga

    @staticmethod
    def get_v_slope() -> float:
        p = ParameterStateSingleton.get_instance()

        if p.v_slope is None:
            p.v_slope = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_V_SLOPE,
                DriverService.get_current_q_v_slope()
            )

        return p.v_slope

    @staticmethod
    def get_v_inter() -> float:
        p = ParameterStateSingleton.get_instance()

        if p.v_inter is None:
            p.v_inter = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_V_INTER,
                DriverService.get_current_q_v_inter()
            )

        return p.v_inter

    @staticmethod
    def get_c_slope() -> float:
        p = ParameterStateSingleton.get_instance()

        if p.c_slope is None:
            p.c_slope = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_C_SLOPE,
                DriverService.get_current_q_c_slope()
            )

        return p.c_slope

    @staticmethod
    def get_c_inter() -> float:
        p = ParameterStateSingleton.get_instance()

        if p.c_inter is None:
            p.c_inter = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_C_INTER,
                DriverService.get_current_q_c_inter()
            )

        return p.c_inter

    @staticmethod
    def get_q_v_slope() -> list:
        p = ParameterStateSingleton.get_instance()

        if not p.q_v_slope:
            p.q_v_slope = DriverService.__send_command(CommandEnum.GET_Q_V_SLOPE)[3:7]

        return p.q_v_slope

    @staticmethod
    def get_current_q_v_slope() -> int:
        return DriverService.get_q_v_slope()[NumericUtils.calculate_byte_to_read_index(DriverService.get_v_pga())]

    @staticmethod
    def get_q_c_slope() -> list:
        p = ParameterStateSingleton.get_instance()

        if not p.q_c_slope:
            p.q_c_slope = DriverService.__send_command(CommandEnum.GET_Q_C_SLOPE)[3:7]

        return p.q_c_slope

    @staticmethod
    def get_current_q_c_slope() -> int:
        return DriverService.get_q_c_slope()[NumericUtils.calculate_byte_to_read_index(DriverService.get_c_pga())]

    @staticmethod
    def get_q_v_inter() -> list:
        p = ParameterStateSingleton.get_instance()

        if not p.q_v_inter:
            p.q_v_inter = DriverService.__send_command(CommandEnum.GET_Q_V_INTER)[3:7]

        return p.q_v_inter

    @staticmethod
    def get_current_q_v_inter() -> int:
        return DriverService.get_q_v_inter()[NumericUtils.calculate_byte_to_read_index(DriverService.get_v_pga())]

    @staticmethod
    def get_q_c_inter() -> list:
        p = ParameterStateSingleton.get_instance()

        if not p.q_c_inter:
            p.q_c_inter = DriverService.__send_command(CommandEnum.GET_Q_C_INTER)[3:7]

        return p.q_c_inter

    @staticmethod
    def get_current_q_c_inter() -> int:
        return DriverService.get_q_c_inter()[NumericUtils.calculate_byte_to_read_index(DriverService.get_c_pga())]

    @staticmethod
    def set_mode(mode: str) -> None:
        p = ParameterStateSingleton.get_instance()

        try:
            mode_enum = ModeEnum[mode]
        except KeyError:
            raise Exception('Unsupported working mode. Available working modes are "VFIX" and "MPPT".')

        DriverService.__send_command(CommandEnum.SET_MODE, mode_enum.value)
        p.mode = mode_enum.name

    @staticmethod
    def get_mode() -> str:
        p = ParameterStateSingleton.get_instance()

        if p.mode is None:
            p.mode = NumericUtils.merge_bytes_as_decimal_command_result(
                DriverService.__send_command(CommandEnum.GET_MODE)
            )

        return p.mode

    @staticmethod
    def set_v_ref_by_dac(dac: int) -> None:
        DriverService.__send_command(
            CommandEnum.SET_V_REF,
            dac
        )

        ParameterStateSingleton.get_instance().v_ref = dac

    @staticmethod
    def set_v_ref_by_voltage(voltage: float) -> None:
        dac: int = NumericUtils.calculate_dac(voltage)
        DriverService.__send_command(
            CommandEnum.SET_V_REF,
            dac
        )

        ParameterStateSingleton.get_instance().v_ref = dac

    @staticmethod
    def get_voltage_and_current() -> dict:
        raw_voltage_and_current = DriverService.__send_command(CommandEnum.GET_VOLTAGE_AND_CURRENT)

        raw_voltage = NumericUtils.merge_bytes_as_decimal(*raw_voltage_and_current[3:5])
        raw_current = NumericUtils.merge_bytes_as_decimal(*raw_voltage_and_current[5:7])

        return {
            'voltage': (
                               NumericUtils.calculate_adc_from_raw_value(raw_voltage, DriverService.get_v_pga())
                               * DriverService.get_v_slope()
                       ) + DriverService.get_v_inter(),
            'current': (
                               NumericUtils.calculate_adc_from_raw_value(raw_current, DriverService.get_c_pga())
                               * DriverService.get_c_slope()
                       ) + DriverService.get_c_inter(),
        }
