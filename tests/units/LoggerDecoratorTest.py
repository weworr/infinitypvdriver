import unittest
from unittest.mock import patch, mock_open

from logger.LoggerDecorator import function_logger


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_open = mock_open()
        patch('builtins.open', self.mock_open).start()

    def tearDown(self) -> None:
        patch.stopall()

    def test_something(self) -> None:
        self.__sample_method()
        handler = self.mock_open()

        self.assertEqual(
            2,
            handler.write.call_count
        )

    @function_logger
    def __sample_method(self) -> int:
        return 1
