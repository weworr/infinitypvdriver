from serialHandlers.SerialHandler import SerialHandler
import serial

from parameters.ParameterState import ParameterState
from enums.CommandEnum import CommandEnum
from parameters.ParameterStateSingleton import ParameterStateSingleton
from enums.ModeEnum import ModeEnum
from loggers.LoggerDecorator import command_logger
from utils.NumericUtils import NumericUtils


MIN_DAC: int = 0
MAX_DAC: int = 4095


class DriverService:
    @staticmethod
    @command_logger
    def __send_command(
            command: CommandEnum,
            data_msb: int = 0x00,
            data_lsb: int = 0x00
    ) -> list[int]:
        handler: serial.Serial = SerialHandler.get_instance()

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
        p: ParameterState = ParameterStateSingleton.get_instance()

        q_limits: list[int] = DriverService.__send_command(CommandEnum.GET_Q_LIMITS)[3:7]
        p.q_limits_v_min = q_limits[0]
        p.q_limits_v_max = q_limits[1]
        p.q_limits_c_min = q_limits[2]
        p.q_limits_c_max = q_limits[3]

    @staticmethod
    def __validate_dac(dac: int) -> None:
        if dac < MIN_DAC or dac > MAX_DAC:
            raise Exception(f'DAC must be between 0 and 4095, currently: {dac}')

    @staticmethod
    def init_driver():
        for instance in ParameterStateSingleton.get_all_instances():
            DriverService.active_unit(instance.channel)
            instance.regenerate_soft_values(False)

        DriverService.active_unit(0)

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
    def get_v_min(regenerate: bool = False) -> float:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if regenerate or p.v_min is None:
            p.v_min = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_V_MIN,
                DriverService.get_q_limits_v_min()
            )

        return p.v_min

    @staticmethod
    def get_v_max(regenerate: bool = False) -> float:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if regenerate or p.v_max is None:
            p.v_max = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_V_MAX,
                DriverService.get_q_limits_v_max()
            )

        return p.v_max

    @staticmethod
    def get_c_min(regenerate: bool = False) -> float:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if regenerate or p.c_min is None:
            p.c_min = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_C_MIN,
                DriverService.get_q_limits_c_min()
            )

        return p.c_min

    @staticmethod
    def get_c_max(regenerate: bool = False) -> float:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if regenerate or p.c_max is None:
            p.c_max = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_C_MAX,
                DriverService.get_q_limits_c_max()
            )

        return p.c_max

    @staticmethod
    def get_q_limits(regenerate: bool = False) -> dict[str, int]:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if (
                regenerate
                or p.q_limits_v_min is None
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
        p: ParameterState = ParameterStateSingleton.get_instance()

        if p.q_limits_v_min is None:
            DriverService.__set_q_limits()

        return p.q_limits_v_min

    @staticmethod
    def get_q_limits_v_max() -> int:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if p.q_limits_v_max is None:
            DriverService.__set_q_limits()

        return p.q_limits_v_max

    @staticmethod
    def get_q_limits_c_min() -> int:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if p.q_limits_c_min is None:
            DriverService.__set_q_limits()

        return p.q_limits_c_min

    @staticmethod
    def get_q_limits_c_max() -> int:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if p.q_limits_c_max is None:
            DriverService.__set_q_limits()

        return p.q_limits_c_max

    @staticmethod
    def get_v_pga() -> int:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if p.v_pga is None:
            p.v_pga = NumericUtils.merge_bytes_as_decimal_command_result(
                DriverService.__send_command(CommandEnum.GET_V_PGA)
            )

        return p.v_pga

    @staticmethod
    def get_c_pga() -> int:
        p: ParameterState = ParameterStateSingleton.get_instance()

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
    def get_v_slope(regenerate: bool = False) -> float:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if regenerate or p.v_slope is None:
            p.v_slope = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_V_SLOPE,
                DriverService.get_current_q_v_slope()
            )

        return p.v_slope

    @staticmethod
    def get_v_inter(regenerate: bool = False) -> float:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if regenerate or p.v_inter is None:
            p.v_inter = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_V_INTER,
                DriverService.get_current_q_v_inter()
            )

        return p.v_inter

    @staticmethod
    def get_c_slope(regenerate: bool = False) -> float:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if regenerate or p.c_slope is None:
            p.c_slope = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_C_SLOPE,
                DriverService.get_current_q_c_slope()
            )

        return p.c_slope

    @staticmethod
    def get_c_inter(regenerate: bool = False) -> float:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if regenerate or p.c_inter is None:
            p.c_inter = DriverService.__calculate_value_from_q_format(
                CommandEnum.GET_C_INTER,
                DriverService.get_current_q_c_inter()
            )

        return p.c_inter

    @staticmethod
    def get_q_v_slope() -> list[int]:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if not p.q_v_slope:
            p.q_v_slope = DriverService.__send_command(CommandEnum.GET_Q_V_SLOPE)[3:7]

        return p.q_v_slope

    @staticmethod
    def get_current_q_v_slope() -> int:
        return DriverService.get_q_v_slope()[NumericUtils.calculate_byte_to_read_index(DriverService.get_v_pga())]

    @staticmethod
    def get_q_c_slope() -> list[int]:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if not p.q_c_slope:
            p.q_c_slope = DriverService.__send_command(CommandEnum.GET_Q_C_SLOPE)[3:7]

        return p.q_c_slope

    @staticmethod
    def get_current_q_c_slope() -> int:
        return DriverService.get_q_c_slope()[NumericUtils.calculate_byte_to_read_index(DriverService.get_c_pga())]

    @staticmethod
    def get_q_v_inter() -> list[int]:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if not p.q_v_inter:
            p.q_v_inter = DriverService.__send_command(CommandEnum.GET_Q_V_INTER)[3:7]

        return p.q_v_inter

    @staticmethod
    def get_current_q_v_inter() -> int:
        return DriverService.get_q_v_inter()[NumericUtils.calculate_byte_to_read_index(DriverService.get_v_pga())]

    @staticmethod
    def get_q_c_inter() -> list[int]:
        p: ParameterState = ParameterStateSingleton.get_instance()

        if not p.q_c_inter:
            p.q_c_inter = DriverService.__send_command(CommandEnum.GET_Q_C_INTER)[3:7]

        return p.q_c_inter

    @staticmethod
    def get_current_q_c_inter() -> int:
        return DriverService.get_q_c_inter()[NumericUtils.calculate_byte_to_read_index(DriverService.get_c_pga())]

    @staticmethod
    def set_mode(mode: str) -> None:
        try:
            mode_enum: ModeEnum = ModeEnum[mode]
        except KeyError:
            raise Exception('Unsupported working mode. Available working modes are "VFIX" and "MPPT".')

        DriverService.__send_command(CommandEnum.SET_MODE, mode_enum.value)
        ParameterStateSingleton.get_instance().mode = mode_enum.name

    @staticmethod
    def get_mode() -> str:
        return ParameterStateSingleton.get_instance().mode

    @staticmethod
    def set_v_ref_by_dac(dac: int) -> None:
        DriverService.__validate_dac(dac)

        dac_bytes: bytes = dac.to_bytes(2)

        DriverService.__send_command(
            CommandEnum.SET_V_REF,
            dac_bytes[0],
            dac_bytes[1]
        )

        ParameterStateSingleton.get_instance().v_ref = dac

    @staticmethod
    def set_v_ref_by_voltage(voltage: float) -> None:
        dac: int = NumericUtils.calculate_dac(
            voltage,
            DriverService.get_v_min(),
            DriverService.get_v_max()
        )

        DriverService.set_v_ref_by_dac(dac)

    @staticmethod
    def get_current_v_ref_as_dac() -> int:
        return ParameterStateSingleton.get_instance().v_ref

    @staticmethod
    def get_current_v_ref_as_v() -> float:
        return NumericUtils.calculate_voltage_from_dac(
            DriverService.get_current_v_ref_as_dac(),
            DriverService.get_v_min(),
            DriverService.get_v_max()
        )

    # TODO Do wywalenia ten ascending. xd
    @staticmethod
    def set_v_ref_step(dac_step: int) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()

        p.dac_step = dac_step

        v_min: float = DriverService.get_v_min()
        v_max: float = DriverService.get_v_max()

        voltage: float = NumericUtils.calculate_voltage_from_dac(
            p.dac_step,
            v_min,
            v_max
        )

        p.v_step = (-1 if dac_step < 0 else 1) * (v_min + abs(voltage))

    @staticmethod
    def set_v_ref_step_by_voltage(voltage: float) -> None:
        """
        Shift - wartość przesunięcia v_min, między v_max. Trzeba dodać tą wartość do podanego voltage.
        W przeciwnym wypadku wartość korku będzie przesunięta o v_min + v_max. Dla Gain x1 jest to ~0.039.
        :param voltage:
        :return:
        """
        v_min: float = DriverService.get_v_min()
        v_max: float = DriverService.get_v_max()

        if 0 == voltage:
            DriverService.set_v_ref_step(MIN_DAC)
            return

        DriverService.set_v_ref_step(
            (-1 if voltage < 0 else 1) * NumericUtils.calculate_dac(
                v_min + abs(voltage),
                v_min,
                v_max
            ),
        )

    @staticmethod
    def next_step() -> None:
        new_dac: int = DriverService.get_current_v_ref_as_dac() + DriverService.get_dac_step()

        if new_dac > MAX_DAC:
            new_dac = MAX_DAC

        elif new_dac < MIN_DAC:
            new_dac = MIN_DAC

        DriverService.set_v_ref_by_dac(new_dac)

    @staticmethod
    def change_step_direction() -> None:
        DriverService.set_v_ref_step(-DriverService.get_dac_step())

    @staticmethod
    def get_dac_step() -> int:
        dac_step: int = ParameterStateSingleton.get_instance().dac_step

        if dac_step is None:
            raise Exception('DAC_step has not been set.')

        return dac_step

    @staticmethod
    def get_v_step() -> float:
        v_step: float = ParameterStateSingleton.get_instance().v_step

        if v_step is None:
            raise Exception('V_step has not been set.')

        return v_step

    @staticmethod
    def get_voltage_and_current() -> dict[str, float]:
        raw_voltage_and_current: list[int] = DriverService.__send_command(CommandEnum.GET_VOLTAGE_AND_CURRENT)[3:7]

        raw_voltage: int = NumericUtils.merge_bytes_as_decimal(*raw_voltage_and_current[0:2])
        raw_current: int = NumericUtils.merge_bytes_as_decimal(*raw_voltage_and_current[2:4])

        voltage_adc: float = NumericUtils.calculate_adc_from_raw_value(raw_voltage, DriverService.get_v_pga())
        current_adc: float = NumericUtils.calculate_adc_from_raw_value(raw_current, DriverService.get_c_pga())

        return {
            'voltage': voltage_adc * DriverService.get_v_slope() + DriverService.get_v_inter(),
            'current': current_adc * DriverService.get_c_slope() + DriverService.get_c_inter(),
        }
