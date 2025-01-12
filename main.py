from SerialHandler import SerialHandler
from services.DriverService import DriverService
from utils.NumericUtils import NumericUtils


# TODO
#   - Logger
#   - vref na różne sposoby
#   - dekorator/lub po prostu coś innego handlera na close
#   - dokumentacja :(
#   - weryfikacja "TODO Do weryfikacji" 14.01
#   - README
#   - wywalić poza folder główny reszte klas
#   - i zrobić coś z reset.py


def init() -> None:
    """
    Funkcja sterownika.
    Inicjalizuje urządzenie i pamięć sterownika z domyślnymi danymi:
        - c_pga = 1
        - v_pga = 1
        - q_limits = {pobrane z urządzenia}
    """
    DriverService.init_driver()


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
def get_internal_idn() -> int:
    """
    :return: Numer identyfikacyjny urządzenia
    """
    return DriverService.get_internal_idn()


def active_unit(channel: int) -> None:
    """
    Ustawia komunikację z jedynm z ośmiu kanałów.
    :param channel: Kanał na którego przestawiamy komunikację. Należy podać liczbę całkowitą z przedziału od 0 do 7.
    """
    DriverService.active_unit(channel)


def get_unit_idn() -> int:
    """
    :return: Numer identyfikacyjny kanału.
    """
    return DriverService.get_unit_idn()

# endregion General Commands


# ===========================
# region Calibration Commands
# ===========================
def get_v_min() -> int:
    return DriverService.get_v_min()


def get_v_max() -> int:
    return DriverService.get_v_max()


def get_c_min() -> int:
    return DriverService.get_c_min()


def get_c_max() -> int:
    return DriverService.get_c_max()


def get_v_and_c_range() -> dict[str, float]:
    return {
        'v_min': DriverService.get_v_min(),
        'v_max': DriverService.get_v_max(),
        'c_min': DriverService.get_c_min(),
        'c_max': DriverService.get_c_max()
    }


def get_q_limits() -> dict[str, int]:
    return DriverService.get_q_limits()


def get_q_limit_v_min() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_q_limits_v_min()


def get_q_limit_v_max() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_q_limits_v_max()


def get_q_limit_c_min() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_q_limits_c_min()


def get_q_limit_c_max() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_q_limits_c_max()


def get_v_pga() -> int:
    return DriverService.get_v_pga()


def get_c_pga() -> int:
    return DriverService.get_c_pga()


def set_v_pga(pga: int) -> None:
    """
    :param pga: Programmable Gain Amplifier. Akceptowalna jest jedynie jedna z liczb: 1, 2, 4, 8.
    """
    DriverService.set_v_pga(pga)


def set_c_pga(pga: int) -> None:
    """
    :param pga: Programmable Gain Amplifier. Akceptowalna jest jedynie jedna z liczb: 1, 2, 4, 8.
    """
    DriverService.set_c_pga(pga)


def get_v_slope() -> float:
    return DriverService.get_v_slope()


def get_v_inter() -> float:
    return DriverService.get_v_inter()


def get_c_slope() -> float:
    return DriverService.get_c_slope()


def get_c_inter() -> float:
    return DriverService.get_c_inter()


def get_q_v_slope() -> dict[str, int]:
    q_v_slope = DriverService.get_q_v_slope()

    return {
        'q_v_slope_x1': q_v_slope[0],
        'q_v_slope_x2': q_v_slope[1],
        'q_v_slope_x4': q_v_slope[2],
        'q_v_slope_x8': q_v_slope[3]
    }


def get_current_q_v_slope() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_current_q_v_slope()


def get_q_c_slope() -> dict[str, int]:
    q_c_slope = DriverService.get_q_c_slope()

    return {
        'q_c_slope_x1': q_c_slope[0],
        'q_c_slope_x2': q_c_slope[1],
        'q_c_slope_x4': q_c_slope[2],
        'q_c_slope_x8': q_c_slope[3]
    }


def get_current_q_c_slope() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_current_q_c_slope()


def get_q_v_inter() -> dict[str, int]:
    q_v_inter = DriverService.get_q_v_inter()

    return {
        'q_v_inter_x1': q_v_inter[0],
        'q_v_inter_x2': q_v_inter[1],
        'q_v_inter_x4': q_v_inter[2],
        'q_v_inter_x8': q_v_inter[3]
    }


def get_current_q_v_inter() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_current_q_v_inter()


def get_q_c_inter() -> dict[str, int]:
    q_c_inter = DriverService.get_q_c_inter()

    return {
        'q_c_inter_x1': q_c_inter[0],
        'q_c_inter_x2': q_c_inter[1],
        'q_c_inter_x4': q_c_inter[2],
        'q_c_inter_x8': q_c_inter[3]
    }


def get_current_q_c_inter() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_current_q_c_inter()

# endregion Calibration Commands


# ===========================
# region Working Commands
# ===========================

def set_mode(mode: str) -> None:
    """
    Ustawia tryb działania urządzenia. Domyślnym trybem jest tryb "VFIX" - manualny.
    :param mode: Należy podać odpowiednią wartość. Dla manualnego ustawiania i wykonywania kroku "VFIX",
        dla automatycznego "MPPT".
    """
    return DriverService.set_mode(mode)


def get_mode() -> str:
    return DriverService.get_mode()


def set_v_ref(dac: int) -> None:
    return DriverService.set_v_ref_by_dac(dac)


def set_v_ref_by_voltage(voltage: float) -> None:
    """
    Funkcja sterownika.
    """
    return DriverService.set_v_ref_by_voltage(voltage)


def get_current_v_ref() -> int:
    """
    Funkcja sterownika
    """
    return DriverService.get_current_v_ref_as_dac()


def get_current_v_ref_as_voltage() -> float:
    """
    Funkcja sterownika
    """
    return DriverService.get_current_v_ref_as_v()


def set_v_ref_step(dac: int) -> None:
    """
    Funkcja sterownika
    """
    DriverService.set_v_ref_step(dac)


def set_v_ref_step_by_voltage(voltage: float) -> None:
    """
    Funkcja sterownika
    """
    DriverService.set_v_ref_step_by_voltage(voltage)


def next_step() -> None:
    """
    Funkcja sterownika
    """
    DriverService.next_step()


def change_step_direction() -> None:
    DriverService.change_step_direction()


def get_voltage_and_current() -> dict[str, float]:
    return DriverService.get_voltage_and_current()

# endregion Working Commands


if __name__ == '__main__':
    init()

    # TODO Kuba - przetestować do końca ustawianie tych v_ref i stepów.
    exit()
    voltage = 0.1
    # step = 0.05 + 0.04
    step = -0.05
    # 0.05 -> 0.01
    # 0.1 -> 0.06
    v_min = DriverService.get_v_min()
    v_max = DriverService.get_v_max()

    print('v_min + step', v_min + step)

    print(v_min + v_max)  # 0.038

    print('v_min:\t', v_min)
    print('v_max:\t', v_max)

    dac = NumericUtils.calculate_dac(voltage, v_min, v_max)
    print(f'calculate_dac {voltage}:\t', dac)

    print('calculate_voltage_from_dac:\t', NumericUtils.calculate_voltage_from_dac(dac, v_min, v_max))

    DriverService.set_v_ref_step_by_voltage(step)
    print('get_dac_step:\t', DriverService.get_dac_step())
    print('get_v_step:\t', DriverService.get_v_step())
