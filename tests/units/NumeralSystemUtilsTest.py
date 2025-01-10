import unittest
from unittest.mock import Mock, patch

from services.DriverService import DriverService
from utils.NumericUtils import NumericUtils
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
            NumericUtils.merge_bytes_as_decimal_command_result([102, 1, 2, 191, 235, 254, 226, 0, 52, 52]),
            -1075052830
        )

    def test_merge_bytes_as_decimal_with_signed_true(self) -> None:
        self.assertEqual(
            NumericUtils.merge_bytes_as_decimal(0, 142),
            142
        )

        self.assertEqual(
            NumericUtils.merge_bytes_as_decimal(247, 64),
            -2240
        )

    def test_calculate_adc_from_raw_value(self) -> None:
        self.assertEqual(
            NumericUtils.calculate_adc_from_raw_value(142, 1),
            0.008875000000000001
        )

        self.assertEqual(
            NumericUtils.calculate_adc_from_raw_value(-2240, 1),
            -0.14
        )

    def test_get_voltage_and_current(self):
        self.assertEqual(
            DriverService.get_voltage_and_current(),
            {'voltage': 0.014633910147473218, 'current': -2.7662073475122453}
        )

    def test_calculate_value_from_q_format(self) -> None:
        self.assertEqual(
            NumericUtils.calculate_value_from_q_format(-1073741824, 30),
            -1.0
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
