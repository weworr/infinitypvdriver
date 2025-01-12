import unittest
from unittest.mock import Mock, patch

from services.DriverService import DriverService
from utils.NumericUtils import NumericUtils
from tests.mocks.MockSerial import MockSerial

from SerialHandler import SerialHandler


class NumeralSystemUtilsTest(unittest.TestCase):
    __mock_serial: MockSerial = MockSerial()
    __mock_serial_handler: Mock = Mock(spec=SerialHandler)

    def setUp(self) -> None:
        patch('SerialHandler.SerialHandler.get_instance', return_value=self.__mock_serial).start()
        self.__mock_serial_handler.get_instance.return_value = NumeralSystemUtilsTest.__mock_serial
        DriverService.init_driver()

    def tearDown(self) -> None:
        patch.stopall()

    def test_merge_bytes_as_decimal_command_result_with_signed_true(self) -> None:
        self.assertEqual(
            -1075052830,
            NumericUtils.merge_bytes_as_decimal_command_result([102, 1, 2, 191, 235, 254, 226, 0, 52, 52])
        )

    def test_merge_bytes_as_decimal_with_signed_true(self) -> None:
        self.assertEqual(
            142,
            NumericUtils.merge_bytes_as_decimal(0, 142)
        )

        self.assertEqual(
            -2240,
            NumericUtils.merge_bytes_as_decimal(247, 64)
        )

    def test_calculate_adc_with_raw_value_less_or_equal_two_bytes_max_value(self) -> None:
        self.assertEqual(
            0.008875000000000001,
            NumericUtils.calculate_adc_from_raw_value(142, 1)
        )

    def test_calculate_adc_with_raw_value_greater_than_two_bytes_max_value(self) -> None:
        self.assertEqual(
            -1.423,
            NumericUtils.calculate_adc_from_raw_value(42768, 1)
        )

    def test_get_voltage_and_current(self):
        self.assertEqual(
            {'voltage': 0.014633910147473218, 'current': -2.7662073475122453},
            DriverService.get_voltage_and_current()
        )

    def test_calculate_value_from_q_format_when_value_q_greater_than_max_four_byte_value(self) -> None:
        self.assertEqual(
            -4.0007000006735325,
            NumericUtils.calculate_value_from_q_format(3221037567, 28)
        )

    def test_calculate_value_from_q_format_when_value_q_less_or_equal_max_four_byte_value(self) -> None:
        self.assertEqual(
            1.1999299973249435,
            NumericUtils.calculate_value_from_q_format(322103756, 28)
        )

    def test_calculate_dac_from_voltage(self) -> None:
        self.assertEqual(
            3089,
            NumericUtils.calculate_dac(
                2.01,
                DriverService.get_v_min(),
                DriverService.get_v_max()
            )
        )

    def test_calculate_voltage_from_dac(self) -> None:
        self.assertEqual(1, 1)  # TODO
