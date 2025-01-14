import unittest
from unittest.mock import patch, mock_open, Mock

from parameters.ParameterStateSingleton import ParameterStateSingleton
from parameters.ParameterState import ParameterState
from enums.CommandEnum import CommandEnum
from enums.ModeEnum import ModeEnum
from serialHandlers.SerialHandler import SerialHandler
from services.DriverService import DriverService
from tests.mocks.MockSerial import MockSerial
from utils.NumericUtils import NumericUtils


class DriverServiceTest(unittest.TestCase):
    __V_MIN_GAIN_1: float = -4.004883877933025
    __V_MAX_GAIN_1: float = 3.9668768607079983

    __C_MIN_GAIN_1: float = -1.0
    __C_MAX_GAIN_1: float = 40.38594967126846

    __Q_LIMITS_GAIN_1: dict[str, int] = {
        'v_min': 28,
        'v_max': 28,
        'c_min': 30,
        'c_max': 25
    }

    __V_SLOPE_GAIN_1: float = 1.9678197354078293
    __V_INTER_GAIN_1: float = -0.002830490004271269
    __C_SLOPE_GAIN_1: float = 19.722755804657936
    __C_INTER_GAIN_1: float = -0.005021534860134125

    __Q_V_SLOPE: list[int] = [30, 30, 30, 29]
    __Q_C_SLOPE: list[int] = [26, 26, 26, 26]
    __Q_V_INTER: list[int] = [31, 31, 31, 31]
    __Q_C_INTER: list[int] = [31, 31, 31, 31]

    __mock_serial: MockSerial = MockSerial()
    __mock_serial_handler: Mock = Mock(spec=SerialHandler)

    def setUp(self) -> None:
        patch('serialHandlers.SerialHandler.SerialHandler.get_instance', return_value=self.__mock_serial).start()
        patch('builtins.open', new_callable=mock_open).start()

        self.__mock_serial_handler.get_instance.return_value = DriverServiceTest.__mock_serial

        DriverService.init_driver()

    def tearDown(self) -> None:
        patch.stopall()

    def test_send_command(self) -> None:
        self.assertEqual(
            [102, 1, 2, 0, 142, 247, 64, 0, 44, 52],
            DriverService._DriverService__send_command(CommandEnum.GET_INTERNAL_IDN)
        )

    def test_calculate_value_from_q_format(self) -> None:
        self.assertEqual(
            self.__V_MIN_GAIN_1,
            DriverService._DriverService__calculate_value_from_q_format(
                CommandEnum.GET_V_MIN,
                self.__Q_LIMITS_GAIN_1['v_min']
            )
        )

    def test_set_q_limits(self) -> None:
        DriverService._DriverService__set_q_limits()

        self.assertEqual(
            self.__Q_LIMITS_GAIN_1,
            DriverService.get_q_limits()
        )

    def test_validate_dac(self) -> None:
        for i in (-1, 4096):
            with self.assertRaises(Exception):
                DriverService._DriverService__validate_dac(i)

    def test_init_driver(self) -> None:
        DriverService.init_driver()

        for instance in ParameterStateSingleton.get_all_instances():
            self.assertIsInstance(instance, ParameterState)
            self.assertEqual(self.__V_MIN_GAIN_1, instance.v_min)
            self.assertEqual(self.__V_MAX_GAIN_1, instance.v_max)

            self.assertEqual(self.__V_SLOPE_GAIN_1, instance.v_slope)
            self.assertEqual(self.__V_INTER_GAIN_1, instance.v_inter)
            self.assertEqual(self.__C_SLOPE_GAIN_1, instance.c_slope)
            self.assertEqual(self.__C_INTER_GAIN_1, instance.c_inter)

            self.assertEqual(self.__Q_LIMITS_GAIN_1['v_min'], instance.q_limits_v_min)
            self.assertEqual(self.__Q_LIMITS_GAIN_1['v_max'], instance.q_limits_v_max)
            self.assertEqual(self.__Q_LIMITS_GAIN_1['c_min'], instance.q_limits_c_min)
            self.assertEqual(self.__Q_LIMITS_GAIN_1['c_max'], instance.q_limits_c_max)

    def test_get_internal_idn(self) -> None:
        self.assertEqual(
            9369408,
            DriverService.get_internal_idn()
        )

    def test_active_channel_default_value(self) -> None:
        self.assertEqual(
            0,
            ParameterStateSingleton.get_active_channel()
        )

    def test_active_channel(self) -> None:
        DriverService.active_unit(7)

        self.assertEqual(
            7,
            ParameterStateSingleton.get_active_channel()
        )

        # Cleanup
        DriverService.active_unit(0)

    def test_active_channel_with_wrong_channel(self) -> None:
        for i in (-1, 8):
            with self.assertRaises(Exception):
                DriverService.active_unit(i)

    def test_get_unit_idn(self) -> None:
        self.assertEqual(
            9369408,
            DriverService.get_unit_idn()
        )

    def test_get_v_min(self) -> None:
        self.assertEqual(
            self.__V_MIN_GAIN_1,
            DriverService.get_v_min()
        )

    def test_get_v_min_when_none(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.v_min = None

        DriverService.get_v_min()

        self.assertEqual(
            self.__V_MIN_GAIN_1,
            p.v_min
        )

    def test_get_v_max(self) -> None:
        self.assertEqual(
            self.__V_MAX_GAIN_1,
            DriverService.get_v_max()
        )

    def test_get_v_max_when_none(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.v_max = None

        DriverService.get_v_max()

        self.assertEqual(
            self.__V_MAX_GAIN_1,
            p.v_max
        )

    def test_get_c_min(self) -> None:
        self.assertEqual(
            self.__C_MIN_GAIN_1,
            DriverService.get_c_min()
        )

    def test_get_c_min_when_none(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.c_min = None

        DriverService.get_c_min()

        self.assertEqual(
            self.__C_MIN_GAIN_1,
            p.c_min
        )

    def test_get_c_max(self) -> None:
        self.assertEqual(
            self.__C_MAX_GAIN_1,
            DriverService.get_c_max()
        )

    def test_get_c_max_when_none(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.c_max = None

        DriverService.get_c_max()

        self.assertEqual(
            self.__C_MAX_GAIN_1,
            p.c_max
        )

    def test_get_q_limits(self) -> None:
        self.assertEqual(
            self.__Q_LIMITS_GAIN_1,
            DriverService.get_q_limits()
        )

    def test_get_q_limits_when_one_value_is_none(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.q_limits_v_min = None

        DriverService.get_q_limits()

        self.assertEqual(
            self.__Q_LIMITS_GAIN_1,
            {
                'v_min': p.q_limits_v_min,
                'v_max': p.q_limits_v_max,
                'c_min': p.q_limits_c_min,
                'c_max': p.q_limits_c_max,
            }
        )

    def test_q_limits_v_min(self) -> None:
        self.assertEqual(
            self.__Q_LIMITS_GAIN_1['v_min'],
            DriverService.get_q_limits_v_min()
        )

    def test_q_limits_v_min_when_none(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.q_limits_v_min = None

        DriverService.get_q_limits()

        self.assertEqual(
            self.__Q_LIMITS_GAIN_1['v_min'],
            p.q_limits_v_min
        )

    def test_q_limits_v_max(self) -> None:
        self.assertEqual(
            self.__Q_LIMITS_GAIN_1['v_max'],
            DriverService.get_q_limits_v_max()
        )

    def test_q_limits_v_max_when_none(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.q_limits_v_max = None

        DriverService.get_q_limits_v_max()

        self.assertEqual(
            self.__Q_LIMITS_GAIN_1['v_max'],
            p.q_limits_v_max
        )

    def test_q_limits_c_min(self) -> None:
        self.assertEqual(
            self.__Q_LIMITS_GAIN_1['c_min'],
            DriverService.get_q_limits_c_min()
        )

    def test_get_q_limits_c_min_when_none(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.q_limits_c_min = None

        DriverService.get_q_limits_c_min()

        self.assertEqual(
            self.__Q_LIMITS_GAIN_1['c_min'],
            p.q_limits_c_min
        )

    def test_q_limits_c_max(self) -> None:
        self.assertEqual(
            self.__Q_LIMITS_GAIN_1['c_max'],
            DriverService.get_q_limits_c_max()
        )

    def test_q_limits_c_max_when_none(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.q_limits_c_max = None

        DriverService.get_q_limits_c_max()

        self.assertEqual(
            self.__Q_LIMITS_GAIN_1['c_max'],
            p.q_limits_c_max
        )

    def test_get_v_pga(self) -> None:
        self.assertEqual(
            1,
            DriverService.get_v_pga()
        )

    def test_get_v_pga_when_none(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.v_pga = None

        DriverService.get_v_pga()

        self.assertEqual(
            1,
            p.v_pga
        )

    def test_get_c_pga(self) -> None:
        self.assertEqual(
            1,
            DriverService.get_c_pga()
        )

    def test_get_c_pga_when_none(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.c_pga = None

        DriverService.get_c_pga()

        self.assertEqual(
            1,
            p.c_pga
        )

    def test_set_v_pga(self) -> None:
        for v_pga in [8, 4, 2, 1]:
            DriverService.set_v_pga(v_pga)

            self.assertEqual(
                v_pga,
                ParameterStateSingleton.get_instance().v_pga
            )

    def test_set_v_pga_with_wrong_pga(self) -> None:
        with self.assertRaises(Exception):
            DriverService.set_v_pga(3)

    def test_set_c_pga(self) -> None:
        for c_pga in [8, 4, 2, 1]:
            DriverService.set_c_pga(c_pga)

            self.assertEqual(
                c_pga,
                ParameterStateSingleton.get_instance().c_pga
            )

    def test_set_c_pga_with_wrong_pga(self) -> None:
        with self.assertRaises(Exception):
            DriverService.set_c_pga(3)

    def test_get_v_slope(self) -> None:
        self.assertEqual(
            self.__V_SLOPE_GAIN_1,
            DriverService.get_v_slope()
        )

    def test_get_v_slope_when_none(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.v_slope = None

        DriverService.get_v_slope()

        self.assertEqual(
            self.__V_SLOPE_GAIN_1,
            p.v_slope
        )

    def test_get_v_inter(self) -> None:
        self.assertEqual(
            self.__V_INTER_GAIN_1,
            DriverService.get_v_inter()
        )

    def test_get_v_inter_when_none(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.v_inter = None

        DriverService.get_v_inter()

        self.assertEqual(
            self.__V_INTER_GAIN_1,
            p.v_inter
        )

    def test_get_c_slope(self) -> None:
        self.assertEqual(
            self.__C_SLOPE_GAIN_1,
            DriverService.get_c_slope()
        )

    def test_get_c_slope_when_none(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.c_slope = None

        DriverService.get_c_slope()

        self.assertEqual(
            self.__C_SLOPE_GAIN_1,
            p.c_slope
        )

    def test_get_c_inter(self) -> None:
        self.assertEqual(
            self.__C_INTER_GAIN_1,
            DriverService.get_c_inter()
        )

    def test_get_c_inter_when_none(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.c_inter = None

        DriverService.get_c_inter()

        self.assertEqual(
            self.__C_INTER_GAIN_1,
            p.c_inter
        )

    def test_get_q_v_slope(self) -> None:
        self.assertEqual(
            self.__Q_V_SLOPE,
            DriverService.get_q_v_slope()
        )

    def test_get_q_v_slope_when_empty(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.q_v_slope = []

        DriverService.get_q_v_slope()

        self.assertEqual(
            self.__Q_V_SLOPE,
            p.q_v_slope
        )

    def test_current_q_v_slope(self) -> None:
        self.assertEqual(
            self.__Q_V_SLOPE[0],
            DriverService.get_current_q_v_slope()
        )

    def test_current_q_v_slope_when_empty(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.q_v_slope = []

        self.assertEqual(
            self.__Q_V_SLOPE[0],
            DriverService.get_current_q_v_slope()
        )

        self.assertEqual(
            self.__Q_V_SLOPE[0],
            p.q_v_slope[0]
        )

    def test_get_q_c_slope(self) -> None:
        self.assertEqual(
            self.__Q_C_SLOPE,
            DriverService.get_q_c_slope()
        )

    def test_get_q_c_slope_when_empty(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.q_c_slope = []

        DriverService.get_q_c_slope()

        self.assertEqual(
            self.__Q_C_SLOPE,
            p.q_c_slope
        )

    def test_get_current_q_c_slope(self) -> None:
        self.assertEqual(
            self.__Q_C_SLOPE[0],
            DriverService.get_current_q_c_slope()
        )

    def test_get_current_q_c_slope_when_empty(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.q_c_slope = []

        self.assertEqual(
            self.__Q_C_SLOPE[0],
            DriverService.get_current_q_c_slope()
        )

        self.assertEqual(
            self.__Q_C_SLOPE[0],
            p.q_c_slope[0]
        )

    def test_get_q_v_inter(self) -> None:
        self.assertEqual(
            self.__Q_V_INTER,
            DriverService.get_q_v_inter()
        )

    def test_get_q_v_inter_when_empty(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.q_v_inter = []

        DriverService.get_q_v_inter()

        self.assertEqual(
            self.__Q_V_INTER,
            p.q_v_inter
        )

    def test_get_current_q_v_inter(self) -> None:
        self.assertEqual(
            self.__Q_V_INTER[0],
            DriverService.get_current_q_v_inter()
        )

    def test_get_current_q_v_inter_when_empty(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.q_v_inter = []

        self.assertEqual(
            self.__Q_V_INTER[0],
            DriverService.get_current_q_v_inter()
        )

        self.assertEqual(
            self.__Q_V_INTER[0],
            p.q_v_inter[0]
        )

    def test_get_q_c_inter(self) -> None:
        self.assertEqual(
            self.__Q_C_INTER,
            DriverService.get_q_c_inter()
        )

    def test_get_q_c_inter_when_empty(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.q_c_inter = []

        DriverService.get_q_c_inter()

        self.assertEqual(
            self.__Q_C_INTER,
            p.q_c_inter
        )

    def test_get_current_q_c_inter(self) -> None:
        self.assertEqual(
            self.__Q_C_INTER[0],
            DriverService.get_current_q_c_inter()
        )

    def test_get_current_q_c_inter_when_empty(self) -> None:
        p: ParameterState = ParameterStateSingleton.get_instance()
        p.q_c_inter = []

        self.assertEqual(
            self.__Q_C_INTER[0],
            DriverService.get_current_q_c_inter()
        )

        self.assertEqual(
            self.__Q_C_INTER[0],
            p.q_c_inter[0]
        )

    def test_set_mode(self) -> None:
        DriverService.set_mode(ModeEnum.VFIX.name)

        self.assertEqual(
            ModeEnum.VFIX.name,
            ParameterStateSingleton.get_instance().mode
        )

    def test_set_mode_with_wrong_mode(self) -> None:
        with self.assertRaises(Exception):
            DriverService.set_mode('WRONG')

    def test_get_mode(self) -> None:
        self.assertEqual(
            ModeEnum.VFIX.name,
            DriverService.get_mode()
        )

    def test_set_v_ref_by_dac(self) -> None:
        dac: int = 1
        DriverService.set_v_ref_by_dac(dac)

        self.assertEqual(
            dac,
            ParameterStateSingleton.get_instance().v_ref
        )

    def test_set_v_ref_by_dac_with_wrong_dac(self) -> None:
        for i in (-1, 4096):
            with self.assertRaises(Exception):
                DriverService.set_v_ref_by_dac(i)

    def test_set_v_ref_by_voltage(self) -> None:
        voltage: float = 1.0
        DriverService.set_v_ref_by_voltage(voltage)

        self.assertEqual(
            NumericUtils.calculate_dac(voltage, self.__V_MIN_GAIN_1, self.__V_MAX_GAIN_1),
            ParameterStateSingleton.get_instance().v_ref
        )

    def test_set_v_ref_by_voltage_with_wrong_voltage(self) -> None:
        for i in (self.__V_MIN_GAIN_1 - 1, self.__V_MAX_GAIN_1 + 1):
            with self.assertRaises(Exception):
                DriverService.set_v_ref_by_voltage(i)

    def test_get_current_v_ref_as_dac(self) -> None:
        self.assertEqual(1, 1)  # TODO

    def test_get_current_v_ref_as_v(self) -> None:
        self.assertEqual(1, 1)  # TODO

    def test_set_v_ref_step(self) -> None:
        dac: int = 100
        DriverService.set_v_ref_step(dac)

        self.assertEqual(
            dac,
            ParameterStateSingleton.get_instance().dac_step
        )

    def test_set_v_ref_step_with_invalid_dac_step(self) -> None:
        self.assertEqual(1, 1)  # TODO

    def test_set_v_ref_step_by_voltage(self) -> None:
        self.assertEqual(1, 1)  # TODO

    def test_set_v_ref_step_by_voltage_with_invalid_voltage(self) -> None:
        self.assertEqual(1, 1)  # TODO

    def test_next_step(self) -> None:
        self.assertEqual(1, 1)  # TODO

    def test_next_step_when_dac_step_is_none(self) -> None:
        self.assertEqual(1, 1)  # TODO

    def test_change_step_direction(self) -> None:
        self.assertEqual(1, 1)  # TODO

    def test_change_step_direction_when_dac_step_is_none(self) -> None:
        self.assertEqual(1, 1)  # TODO

    def test_get_dac_step(self) -> None:
        self.assertEqual(1, 1)  # TODO

    def test_get_dac_step_when_none(self) -> None:
        self.assertEqual(1, 1)  # TODO

    def test_get_v_step(self) -> None:
        self.assertEqual(1, 1)  # TODO

    def test_get_v_step_when_none(self) -> None:
        with self.assertRaises(Exception):
            DriverService.get_v_step()

    def test_get_voltage_and_current(self) -> None:
        self.assertEqual(1, 1)  # TODO
