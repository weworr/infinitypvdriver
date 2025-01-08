from CommandEnum import CommandEnum
from service.DriverService import DriverService
from utils.NumeralSystemUtils import NumeralSystemUtils
from ParameterStateSingleton import ParameterStateSingleton
from SerialHandler import SerialHandler


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
    :param port: Port do którego podłączone jest urządzenie
    """
    if SerialHandler.is_initialized():
        raise Exception("SerialHandler is already initialized.")

    SerialHandler.get_instance(port)


# ===========================
# region General Commands
# ===========================
def get_internal_idn() -> int:
    """
    :return: Numer identyfikacyjny urządzenia
    """
    return NumeralSystemUtils.merge_bytes_as_decimal(
        *DriverService.send_command(CommandEnum.GET_INTERNAL_IDN)[3:7],
        signed=False
    )


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
    return NumeralSystemUtils.merge_bytes_as_decimal(*DriverService.send_command(CommandEnum.GET_UNIT_IDN)[3:7])

# endregion General Commands


# ===========================
# region Calibration Commands
# ===========================
def get_v_min() -> int:
    return DriverService.get_v_min()


def get_v_max() -> int:
    return DriverService.get_v_max()


def get_c_min() -> int:
    return DriverService.get_v_max()


def get_c_max() -> int:
    return DriverService.get_c_max()


def get_q_limits() -> dict:
    return {}  # TODO


def get_v_pga() -> int:
    return 0  # TODO


def get_c_pga() -> int:
    return 0  # TODO


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


def get_q_v_slope() -> list:
    return []  # TODO


def get_current_q_v_slope() -> int:
    """
    Funkcja sterownika.
    """
    return 0  # TODO


def get_q_c_slope() -> list:
    return []  # TODO


def get_current_q_c_slope() -> int:
    """
    Funkcja sterownika.
    """
    # TODO W tych miejscach gdzie możemy wyciągać cache'owane rzeczy trzeba ifowac, czy są setnięte
    # Jak nie to trzeba pobrać je z maszyny. Lub na inicie pobrać wszystko na start i mieć to pompie.
    # * można sprawdzić na PG jakie są domyślne wartości i je przypisać na stałe w kodzie i wtedy
    # init będzie tylko po to, żeby zresetować wartości w sterowniku np.
    # Trzeba to przemyśleć jeszcze i guess.
    p = ParameterStateSingleton.get_instance()
    return p.q_c_slope[NumeralSystemUtils.calculate_byte_to_read_index(p.c_pga)]


def get_q_v_inter() -> list:
    return []  # TODO


def get_current_q_v_inter() -> int:
    return 0  # TODO


def get_q_c_inter() -> list:
    return []  # TODO


def get_current_q_c_inter() -> int:
    return 0  # TODO

# endregion Calibration Commands


# ===========================
# region Working Commands
# ===========================

def set_mode() -> None:
    return None


def get_mode() -> str:
    return ''


def set_vref() -> None:
    return None


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


def main():
    init()
    print('===============================')
    get_v_max()
    get_v_max()
    exit()

    SerialHandler.get_instance('/dev/pts/2')
    with open('logs.txt', 'a') as file:
        file.write('------------------------------------------------------\n')

        while True:
            skip = False

            data_msb = 0x00
            data_lsb = 0x00

            keyboard_input = input("Command: ")
            match keyboard_input:
                case '10':
                    command = 0x10
                case '29':  # Set active Channel
                    command = 0x29
                    data_lsb = 0x00
                case '2F':
                    command = 0x2F
                case '34':
                    command = 0x34  # Get Vmin
                case '35':
                    command = 0x35  # Get Vmax
                case '36':
                    command = 0x36  # Get Cmin
                case '37':
                    command = 0x37  # Get Cmax
                case '3E':
                    command = 0x3E
                case '3C':
                    command = 0x3C  # Get VPGA
                case '3D':
                    command = 0x3D  # Get CPGA

                # When chaning PGA (CPGA/VPGA) again read and set qvslope etc values
                case '43-1':  # Set VPGA x1
                    command = 0x43
                    data_lsb = 0x01
                case '43-2':  # Set VPGA x2
                    command = 0x43
                    data_lsb = 0x02
                case '43-4':  # Set VPGA x4
                    command = 0x43
                    data_lsb = 0x04
                case '43-8':  # Set VPGA x8
                    command = 0x43
                    data_lsb = 0x08

                case '44-1':  # Set CPGA x1
                    command = 0x44
                    data_lsb = 0x01
                case '44-2':  # Set CPGA x2
                    command = 0x44
                    data_lsb = 0x02
                case '44-4':  # Set CPGA x4
                    command = 0x44
                    data_lsb = 0x04
                case '44-8':  # Set CPGA x8
                    command = 0x44
                    data_lsb = 0x08
                case '38':  # Set VSLOPE ??
                    command = 0x38

                case '39':
                    command = 0x39
                case '3A':
                    command = 0x3A
                case '3B':
                    command = 0x3B
                case '3F':
                    command = 0x3F
                case '40':
                    command = 0x40  # Get Qcslope
                case '41':
                    command = 0x41  # Get Qvinter
                case '42':
                    command = 0x42  # Get Qcinter
                case '2D-VFIX':  # Set Mode
                    command = 0x2D
                    data_lsb = 0x10
                case '2D-MPPT':
                    command = 0x2D
                    data_lsb = 0x1F
                case '2E':
                    command = 0x2E  # Get Mode
                case '2B':  # Set vref
                    command = 0x2B
                    keyboard_input_msb = input("MSB: ")
                    keyboard_input_lsb = input("LSB: ")
                    data_msb = int(keyboard_input_msb, 16)
                    data_lsb = int(keyboard_input_lsb, 16)
                case '2C':
                    command = 0x2C  # Get voltage and current
                case _:
                    skip = True

            if not skip:
                response = NumeralSystemUtils.send_command(command, data_msb, data_lsb)
                continue

            match keyboard_input:
                case 'vc':
                    response = voltage_and_current(file)
                case 'v_ranges':
                    response = NumeralSystemUtils.get_ranges()
                case 'c_ranges':
                    response = NumeralSystemUtils.get_ranges(False)
                case 'v_min':
                    response = NumeralSystemUtils.merge_bytes_as_decimal_command_result(NumeralSystemUtils.send_command(file, 0x34))
                    # response = Helper.merge_command_result(ParameterStateSingleton.get_instance().v_min, signed=True)
                case 'v_max':
                    response = NumeralSystemUtils.merge_bytes_as_decimal_command_result(
                        ParameterStateSingleton.get_instance().v_max
                    )
                    # response = Helper.merge_command_result(Helper.send_command(file, 0x35), signed=True)
                case 'q':
                    return
                case _:
                    continue

            print(response)
            file.write(f"function: {keyboard_input}, response {response}\n")


if __name__ == '__main__':
    main()
