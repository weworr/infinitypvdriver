import unittest
from unittest.mock import patch, mock_open

from ParameterStateSingleton import ParameterStateSingleton
from services.DriverService import DriverService


class DriverServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        patch('builtins.open', new_callable=mock_open).start()

        DriverService.init_driver()

    def tearDown(self) -> None:
        patch.stopall()

    def test_get_internal_idn(self) -> None:
        self.assertEqual(
            9369408,
            DriverService.get_internal_idn()
        )

    def test_active_channel_with_wrong_channel(self) -> None:
        for i in (-1, 10):
            with self.assertRaises(Exception):
                DriverService.active_unit(i)

    def test_active_channel(self) -> None:
        DriverService.active_unit(0)

        self.assertEqual(
            0,
            ParameterStateSingleton.get_active_channel()
        )

    def test_get_unit_idn(self) -> None:
        self.assertEqual(
            9369408,
            DriverService.get_unit_idn()
        )

    def test_get_q_limits(self) -> None:
        self.assertEqual(
            {
                'v_min': 28,
                'v_max': 28,
                'c_min': 30,
                'c_max': 25
            },
            DriverService.get_q_limits())

    def test_get_q_limits_when_one_value_is_none(self) -> None:
        p = ParameterStateSingleton.get_instance()
        p.q_limits_v_min = None

        self.assertEqual(
            {
                'v_min': 28,
                'v_max': 28,
                'c_min': 30,
                'c_max': 25
            },
            DriverService.get_q_limits()
        )

    def test_q_limits_v_max(self) -> None:
        self.assertEqual(
            28,
            DriverService.get_q_limits_v_max()
        )

    def test_q_limits_v_max_when_none(self) -> None:
        p = ParameterStateSingleton.get_instance()
        p.q_limits_v_max = None

        self.assertEqual(
            28,
            DriverService.get_q_limits_v_max()
        )

    def test_q_limits_c_min(self) -> None:
        self.assertEqual(
            30,
            DriverService.get_q_limits_c_min()
        )

    def test_get_q_limits_c_min_when_none(self) -> None:
        p = ParameterStateSingleton.get_instance()
        p.q_limits_c_min = None

        self.assertEqual(
            30,
            DriverService.get_q_limits_c_min()
        )

    def test_q_limits_c_max(self) -> None:
        self.assertEqual(
            25,
            DriverService.get_q_limits_c_max()
        )

    def test_q_limits_c_max_when_none(self) -> None:
        p = ParameterStateSingleton.get_instance()
        p.q_limits_c_max = None

        self.assertEqual(
            25,
            DriverService.get_q_limits_c_max()
        )

    # def test_set_v_ref_by_voltage(self) -> None:
    #     voltage: float = 1.0
    #     DriverService.set_v_ref_by_voltage(voltage)
    #
    #     self.assertEqual(
    #         NumericUtils.calculate_dac(voltage),
    #         ParameterStateSingleton.get_instance().v_ref
    #     )

    def test_set_v_ref_by_dac(self) -> None:
        dac: int = 1
        DriverService.set_v_ref_by_dac(dac)

        self.assertEqual(
            dac,
            ParameterStateSingleton.get_instance().v_ref
        )

    def test_get_mode(self) -> None:
        self.assertEqual(
            0,
            DriverService.get_mode()
        )

    def test_set_mode(self) -> None:
        DriverService.set_mode('VFIX')

        self.assertEqual(
            'VFIX',
            ParameterStateSingleton.get_instance().mode
        )

    def test_set_mode_with_wrong_mode(self) -> None:
        with self.assertRaises(Exception):
            DriverService.set_mode('WRONG')

    def test_set_c_pga(self) -> None:
        c_pga: int = 1
        DriverService.set_c_pga(c_pga)

        self.assertEqual(
            c_pga,
            ParameterStateSingleton.get_instance().c_pga
        )

    def test_set_c_pga_with_wrong_pga(self) -> None:
        with self.assertRaises(Exception):
            DriverService.set_c_pga(3)

    def test_set_v_pga(self) -> None:
        v_pga: int = 1
        DriverService.set_v_pga(v_pga)

        self.assertEqual(
            v_pga,
            ParameterStateSingleton.get_instance().v_pga
        )

    def test_set_v_pga_with_wrong_pga(self) -> None:
        with self.assertRaises(Exception):
            DriverService.set_v_pga(3)

    def test_get_v_pga(self) -> None:
        p = ParameterStateSingleton.get_instance()
        p.v_pga = None

        self.assertEqual(
            1,
            DriverService.get_v_pga()
        )

    def test_get_c_pga(self) -> None:
        p = ParameterStateSingleton.get_instance()
        p.c_pga = None

        self.assertEqual(
            1,
            DriverService.get_c_pga()
        )
