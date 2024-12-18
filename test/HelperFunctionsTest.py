import unittest
from io import TextIOWrapper
from unittest.mock import Mock, patch

from HelperFunctions import Helper
from MockSerial import MockSerial

from SerialHandler import SerialHandler
from test import voltage_and_current


class TestHelperFunctions(unittest.TestCase):
    __mock_serial: MockSerial = MockSerial()
    __mock_serial_handler: Mock = Mock(spec=SerialHandler)
    __mock_file: Mock = Mock(spec=TextIOWrapper)

    def setUp(self) -> None:
        patch('SerialHandler.SerialHandler.get_instance', return_value=self.__mock_serial).start()
        self.__mock_serial_handler.get_instance.return_value = TestHelperFunctions.__mock_serial

    def test_merge_command_result_with_signed_true(self) -> None:
        self.assertEqual(
            Helper.merge_command_result([102, 1, 2, 191, 235, 254, 226, 0, 52, 52], True),
            -1075052830
        )

    def test_merge_merge_with_fractional_bits_with_signed_true_self(self) -> None:
        self.assertEqual(
            Helper.merge_with_fractional_bits(125, 240, 194, 48, fractional_bits=30, signed=True),
            1.9678197354078293
        )

    def test_merge_with_signed_true(self) -> None:
        self.assertEqual(
            Helper.merge(0, 142, signed=True),
            142
        )

        self.assertEqual(
            Helper.merge(247, 64, signed=True),
            -2240
        )

    def test_calculate_adc_from_raw_value(self) -> None:
        self.assertEqual(
            Helper.calculate_adc_from_raw_value(142, 1),
            0.008875000000000001
        )

        self.assertEqual(
            Helper.calculate_adc_from_raw_value(-2240, 1),
            -0.14
        )

    def test_voltage_and_current(self):
        self.assertEqual(
            voltage_and_current(self.__mock_file),
            {'v': 0.014633910147473218, 'c': -2.7662073475122453}
        )

    def test_get_ranges_for_voltage(self) -> None:
        self.assertEqual(
            Helper.get_ranges(self.__mock_file, True),
            {'v_min': -4.004883877933025, 'v_max': 3.9668768607079983}
        )

    def test_get_ranges_for_current(self) -> None:
        self.assertEqual(
            Helper.get_ranges(self.__mock_file, False),
            {'c_min': -1.0, 'c_max': 40.38594967126846}
        )

    def test_calculate_ranges(self) -> None:
        self.assertEqual(
            Helper.calculate_range(-1073741824, 30),
            -1.0
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)
