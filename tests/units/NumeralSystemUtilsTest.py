import unittest
from unittest.mock import Mock, patch

from service.DriverService import DriverService
from utils.NumeralSystemUtils import NumeralSystemUtils
from mocks.MockSerial import MockSerial

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
            NumeralSystemUtils.merge_bytes_as_decimal_command_result([102, 1, 2, 191, 235, 254, 226, 0, 52, 52]),
            -1075052830
        )

    def test_merge_bytes_as_decimal_with_fractional_bits_with_signed_true_self(self) -> None:
        self.assertEqual(
            NumeralSystemUtils.merge_bytes_as_decimal_with_fractional_bits(125, 240, 194, 48, fractional_bits=30),
            1.9678197354078293
        )

    def test_merge_bytes_as_decimal_with_signed_true(self) -> None:
        self.assertEqual(
            NumeralSystemUtils.merge_bytes_as_decimal(0, 142),
            142
        )

        self.assertEqual(
            NumeralSystemUtils.merge_bytes_as_decimal(247, 64),
            -2240
        )

    def test_calculate_adc_from_raw_value(self) -> None:
        self.assertEqual(
            DriverService.calculate_adc_from_raw_value(142, 1),
            0.008875000000000001
        )

        self.assertEqual(
            DriverService.calculate_adc_from_raw_value(-2240, 1),
            -0.14
        )

    def test_get_voltage_and_current(self):
        self.assertEqual(
            DriverService.get_voltage_and_current(),
            {'voltage': 0.014633910147473218, 'current': -2.7662073475122453}
        )

    def test_get_ranges_for_voltage(self) -> None:
        self.assertEqual(
            DriverService.get_ranges(True),
            {'v_min': -4.004883877933025, 'v_max': 3.9668768607079983}
        )

    def test_get_ranges_for_current(self) -> None:
        self.assertEqual(
            DriverService.get_ranges(False),
            {'c_min': -1.0, 'c_max': 40.38594967126846}
        )

    def test_calculate_ranges(self) -> None:
        self.assertEqual(
            DriverService.calculate_range(-1073741824, 30),
            -1.0
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
