from SerialHandler import SerialHandler
from logger.LoggerDecorator import function_logger
from services.DriverService import DriverService


# TODO
#   - Logger
#   - vref na różne sposoby
#   - dekorator/lub po prostu coś innego handlera na close
#   - dokumentacja :(
#   - weryfikacja "TODO Do weryfikacji" 14.01
#   - README
#   - wywalić poza folder główny reszte klas
#   - i zrobić coś z reset.py

@function_logger
def init() -> None:
    """
    Funkcja sterownika.
    Inicjalizuje urządzenie i pamięć sterownika z domyślnymi danymi:
        - c_pga = 1
        - v_pga = 1
        - q_limits = {pobrane z urządzenia}
    """
    DriverService.init_driver()


@function_logger
def set_serial_port(port: str) -> None:
    """
    Funkcja sterownika.
    Ustawia port, z którym będzie komunikował się sterownik.

    W przypadku, gdy połączenie do dowolnego portu jest już nawiązane funkcja wyrzuci błąd.
    :param port: Port do którego podłączone jest urządzenie.
    """
    if SerialHandler.is_initialized():
        raise Exception('SerialHandler is already initialized.')

    SerialHandler.get_instance(port)


# ======================================================
#                   Funkcje urządzenia
# ======================================================

# ===========================
# region General Commands
# ===========================
@function_logger
def get_internal_idn() -> int:
    """
    :return: Numer identyfikacyjny urządzenia
    """
    return DriverService.get_internal_idn()


@function_logger
def active_unit(channel: int) -> None:
    """
    Ustawia komunikację z jedynm z ośmiu kanałów.
    :param channel: Kanał na którego przestawiamy komunikację. Należy podać liczbę całkowitą z przedziału od 0 do 7.
    """
    DriverService.active_unit(channel)


@function_logger
def get_unit_idn() -> int:
    """
    :return: Numer identyfikacyjny kanału.
    """
    return DriverService.get_unit_idn()

# endregion General Commands


# ===========================
# region Calibration Commands
# ===========================
@function_logger
def get_v_min() -> int:
    return DriverService.get_v_min()


@function_logger
def get_v_max() -> int:
    return DriverService.get_v_max()


@function_logger
def get_c_min() -> int:
    return DriverService.get_c_min()


@function_logger
def get_c_max() -> int:
    return DriverService.get_c_max()


@function_logger
def get_v_and_c_range() -> dict:
    return {
        'v_min': DriverService.get_v_min(),
        'v_max': DriverService.get_v_max(),
        'c_min': DriverService.get_c_min(),
        'c_max': DriverService.get_c_max()
    }


@function_logger
def get_q_limits() -> dict:
    return DriverService.get_q_limits()


@function_logger
def get_q_limit_v_min() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_q_limits_v_min()


@function_logger
def get_q_limit_v_max() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_q_limits_v_max()


@function_logger
def get_q_limit_c_min() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_q_limits_c_min()


@function_logger
def get_q_limit_c_max() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_q_limits_c_max()


@function_logger
def get_v_pga() -> int:
    return DriverService.get_v_pga()


@function_logger
def get_c_pga() -> int:
    return DriverService.get_c_pga()


@function_logger
def set_v_pga(pga: int) -> None:
    """
    :param pga: Programmable Gain Amplifier. Akceptowalna jest jedynie jedna z liczb: 1, 2, 4, 8.
    """
    DriverService.set_v_pga(pga)


@function_logger
def set_c_pga(pga: int) -> None:
    """
    :param pga: Programmable Gain Amplifier. Akceptowalna jest jedynie jedna z liczb: 1, 2, 4, 8.
    """
    DriverService.set_c_pga(pga)


@function_logger
def get_v_slope() -> float:
    return DriverService.get_v_slope()


@function_logger
def get_v_inter() -> float:
    return DriverService.get_v_inter()


@function_logger
def get_c_slope() -> float:
    return DriverService.get_c_slope()


@function_logger
def get_c_inter() -> float:
    return DriverService.get_c_inter()


@function_logger
def get_q_v_slope() -> dict:
    q_v_slope = DriverService.get_q_v_slope()

    return {
        'q_v_slope_x1': q_v_slope[0],
        'q_v_slope_x2': q_v_slope[1],
        'q_v_slope_x4': q_v_slope[2],
        'q_v_slope_x8': q_v_slope[3]
    }


@function_logger
def get_current_q_v_slope() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_current_q_v_slope()


@function_logger
def get_q_c_slope() -> dict:
    q_c_slope = DriverService.get_q_c_slope()

    return {
        'q_c_slope_x1': q_c_slope[0],
        'q_c_slope_x2': q_c_slope[1],
        'q_c_slope_x4': q_c_slope[2],
        'q_c_slope_x8': q_c_slope[3]
    }


@function_logger
def get_current_q_c_slope() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_current_q_c_slope()


@function_logger
def get_q_v_inter() -> dict:
    q_v_inter = DriverService.get_q_v_inter()

    return {
        'q_v_inter_x1': q_v_inter[0],
        'q_v_inter_x2': q_v_inter[1],
        'q_v_inter_x4': q_v_inter[2],
        'q_v_inter_x8': q_v_inter[3]
    }


@function_logger
def get_current_q_v_inter() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_current_q_v_inter()


@function_logger
def get_q_c_inter() -> dict:
    q_c_inter = DriverService.get_q_c_inter()

    return {
        'q_c_inter_x1': q_c_inter[0],
        'q_c_inter_x2': q_c_inter[1],
        'q_c_inter_x4': q_c_inter[2],
        'q_c_inter_x8': q_c_inter[3]
    }


@function_logger
def get_current_q_c_inter() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_current_q_c_inter()

# endregion Calibration Commands


# ===========================
# region Working Commands
# ===========================

@function_logger
def set_mode(mode: str) -> None:
    """
    Ustawia tryb działania urządzenia. Domyślnym trybem jest tryb "VFIX" - manualny.
    :param mode: Należy podać odpowiednią wartość. Dla manualnego ustawiania i wykonywania kroku "VFIX",
        dla automatycznego "MPPT".
    """
    return DriverService.set_mode(mode)


@function_logger
def get_mode() -> str:
    return DriverService.get_mode()


@function_logger
def set_v_ref_by_dac(dac: int) -> None:
    return DriverService.set_v_ref_by_dac(dac)


@function_logger
def set_v_ref_by_voltage(voltage: float) -> None:
    return DriverService.set_v_ref_by_voltage(voltage)


@function_logger
def get_voltage_and_current() -> dict:
    """
    :return: Słownik w postaci:
        {
            "voltage": <float>,
            "current": <float>
        }
    """
    return DriverService.get_voltage_and_current()

# endregion Working Commands


if __name__ == '__main__':
    init()
