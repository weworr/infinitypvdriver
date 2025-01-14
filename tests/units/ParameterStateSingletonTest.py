import unittest
from unittest.mock import patch, PropertyMock, mock_open, Mock

from parameters.ParameterStateSingleton import ParameterStateSingleton
from serialHandlers.SerialHandler import SerialHandler
from services.DriverService import DriverService
from tests.mocks.MockSerial import MockSerial


class ParameterStateSingletonTest(unittest.TestCase):
    __mock_serial: MockSerial = MockSerial()
    __mock_serial_handler: Mock = Mock(spec=SerialHandler)

    def setUp(self) -> None:
        patch('serialHandlers.SerialHandler.SerialHandler.get_instance', return_value=self.__mock_serial).start()
        patch('builtins.open', new_callable=mock_open).start()

        self.__mock_serial_handler.get_instance.return_value = ParameterStateSingletonTest.__mock_serial

        DriverService.init_driver()

    def tearDown(self) -> None:
        patch.stopall()

    def test_get_parameter_state(self) -> None:
        ParameterStateSingleton.get_max_channel()

        for i in range(ParameterStateSingleton.get_max_channel()):
            ParameterStateSingleton.set_active_channel(i)

            self.assertEqual(ParameterStateSingleton.get_instance().channel, i)

    def test_get_instance_without_active_channel(self):
        with patch.object(
                ParameterStateSingleton,
                '_ParameterStateSingleton__active_channel',
                new_callable=PropertyMock
        ) as mock:
            mock.return_value = None

            with self.assertRaises(RuntimeError):
                ParameterStateSingleton.get_instance()
