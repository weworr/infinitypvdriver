import unittest
from unittest.mock import patch, mock_open, MagicMock

from loggers.LoggerDecorator import function_logger


class LoggerDecoratorTest(unittest.TestCase):
    mock_open: MagicMock = None

    def setUp(self) -> None:
        self.mock_open = mock_open()
        patch('builtins.open', self.mock_open).start()

    def tearDown(self) -> None:
        patch.stopall()

    def test_logger(self) -> None:
        handler = self.mock_open()
        self.__sample_method()

        self.assertEqual(
            2,
            handler.write.call_count
        )

    @function_logger
    def __sample_method(self) -> int:
        return 1
