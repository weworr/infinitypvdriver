import unittest
from unittest.mock import patch, PropertyMock

from ParameterStateSingleton import ParameterStateSingleton
from services.DriverService import DriverService


class ParameterStateSingletonTest(unittest.TestCase):
    def setUp(self) -> None:
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
