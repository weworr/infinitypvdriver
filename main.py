from serialHandlers.SerialHandler import SerialHandler
from loggers.LoggerDecorator import function_logger
from services.DriverService import DriverService
from utils.NumericUtils import NumericUtils


# TODO
#   - dekorator/lub po prostu coś innego handlera na close
#   - dokumentacja :(
#   - weryfikacja "TODO Do weryfikacji" 14.01
#   - README
#   - funkcje zwracające dicta, powinny zwracać listę

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
def get_v_and_c_range_as_dict() -> dict[str, float]:
    return {
        'v_min': DriverService.get_v_min(),
        'v_max': DriverService.get_v_max(),
        'c_min': DriverService.get_c_min(),
        'c_max': DriverService.get_c_max()
    }


@function_logger
def get_v_and_c_range() -> list[float]:
    return list(get_v_and_c_range_as_dict().values())


@function_logger
def get_q_limits_as_dict() -> dict[str, int]:
    return DriverService.get_q_limits()


@function_logger
def get_q_limits() -> list[int]:
    return list(get_q_limits_as_dict().values())


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
def get_q_v_slope_as_dict() -> dict[str, int]:
    q_v_slope = DriverService.get_q_v_slope()

    return {
        'q_v_slope_x1': q_v_slope[0],
        'q_v_slope_x2': q_v_slope[1],
        'q_v_slope_x4': q_v_slope[2],
        'q_v_slope_x8': q_v_slope[3]
    }


@function_logger
def get_q_v_slope() -> list[int]:
    return list(get_q_v_slope_as_dict().values())


@function_logger
def get_current_q_v_slope() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_current_q_v_slope()


@function_logger
def get_q_c_slope_as_dict() -> dict[str, int]:
    q_c_slope = DriverService.get_q_c_slope()

    return {
        'q_c_slope_x1': q_c_slope[0],
        'q_c_slope_x2': q_c_slope[1],
        'q_c_slope_x4': q_c_slope[2],
        'q_c_slope_x8': q_c_slope[3]
    }


@function_logger
def get_q_c_slope() -> list[int]:
    return list(get_q_c_slope_as_dict().values())


@function_logger
def get_current_q_c_slope() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_current_q_c_slope()


@function_logger
def get_q_v_inter_as_dict() -> dict[str, int]:
    q_v_inter = DriverService.get_q_v_inter()

    return {
        'q_v_inter_x1': q_v_inter[0],
        'q_v_inter_x2': q_v_inter[1],
        'q_v_inter_x4': q_v_inter[2],
        'q_v_inter_x8': q_v_inter[3]
    }


@function_logger
def get_q_v_inter() -> list[int]:
    return list(get_q_v_inter_as_dict().values())


@function_logger
def get_current_q_v_inter() -> int:
    """
    Funkcja sterownika.
    """
    return DriverService.get_current_q_v_inter()


@function_logger
def get_q_c_inter_as_dict() -> dict[str, int]:
    q_c_inter = DriverService.get_q_c_inter()

    return {
        'q_c_inter_x1': q_c_inter[0],
        'q_c_inter_x2': q_c_inter[1],
        'q_c_inter_x4': q_c_inter[2],
        'q_c_inter_x8': q_c_inter[3]
    }


@function_logger
def get_q_c_inter() -> list[int]:
    return list(get_q_c_inter_as_dict().values())


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
def set_v_ref(dac: int) -> None:
    return DriverService.set_v_ref_by_dac(dac)


@function_logger
def set_v_ref_by_voltage(voltage: float) -> None:
    """
    Funkcja sterownika.
    """
    return DriverService.set_v_ref_by_voltage(voltage)


@function_logger
def get_current_v_ref() -> int:
    """
    Funkcja sterownika
    """
    return DriverService.get_current_v_ref_as_dac()


@function_logger
def get_current_v_ref_as_voltage() -> float:
    """
    Funkcja sterownika
    """
    return DriverService.get_current_v_ref_as_v()


@function_logger
def set_v_ref_step(dac: int) -> None:
    """
    Funkcja sterownika
    """
    DriverService.set_v_ref_step(dac)


@function_logger
def set_v_ref_step_by_voltage(voltage: float) -> None:
    """
    Funkcja sterownika
    """
    DriverService.set_v_ref_step_by_voltage(voltage)


@function_logger
def next_step() -> None:
    """
    Funkcja sterownika
    """
    DriverService.next_step()


@function_logger
def change_step_direction() -> None:
    DriverService.change_step_direction()


@function_logger
def get_voltage_and_current_as_dict() -> dict[str, float]:
    return DriverService.get_voltage_and_current()


def get_voltage_and_current() -> list[float]:
    return list(get_voltage_and_current_as_dict().values())

# endregion Working Commands


if __name__ == '__main__':
    init()

    # TODO Kuba - przetestować do końca ustawianie tych v_ref i stepów.
    # exit()
    voltage = 0.1
    step = -0.05

    v_min = DriverService.get_v_min()
    v_max = DriverService.get_v_max()

    print('v_min:\t', v_min)
    print('v_max:\t', v_max)

    if step < 0:
        DriverService.set_v_ref_by_dac(4095)

    dac = NumericUtils.calculate_dac(voltage, v_min, v_max)
    # print(dac, NumericUtils.calculate_voltage_from_dac(dac, v_min, v_max))
    # print(f'calculate_dac {voltage}:\t', dac)

    # print('calculate_voltage_from_dac:\t', NumericUtils.calculate_voltage_from_dac(dac, v_min, v_max))
    DriverService.set_v_ref_step_by_voltage(step)
    print('------- MAIN DriverService.set_v_ref_step_by_voltage(step) ------')
    print('get_dac_step:\t', DriverService.get_dac_step())
    print('get_v_step:\t', DriverService.get_v_step())
    print('------- ------- ------- ------- ------- ------')
    exit()
    # print('get_current_v_ref_as_dac:\t', DriverService.get_current_v_ref_as_dac())
    # print('get_current_v_ref_as_v:\t', DriverService.get_current_v_ref_as_v())

    for i in range(5):
        DriverService.next_step()
        print(f'AFTER {i+1} STEP')
        print('get_current_v_ref_as_dac:\t', DriverService.get_current_v_ref_as_dac())
        print('get_current_v_ref_as_v:\t', DriverService.get_current_v_ref_as_v())

    print('---------------------------------------------')
    DriverService.change_step_direction()

    for i in range(5):
        DriverService.next_step()
        print(f'AFTER {i+1} STEP')
        print('get_current_v_ref_as_dac:\t', DriverService.get_current_v_ref_as_dac())
        print('get_current_v_ref_as_v:\t', DriverService.get_current_v_ref_as_v())
