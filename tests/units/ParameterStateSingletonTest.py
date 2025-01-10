import unittest
from unittest.mock import patch

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


if __name__ == '__main__':
    unittest.main(verbosity=2)
