from io import TextIOWrapper
from math import log2

from CommandEnum import CommandEnum
from utils.HelperFunctions import Helper
from ParameterStateSingleton import ParameterStateSingleton
from SerialHandler import SerialHandler


def voltage_and_current(file: TextIOWrapper) -> dict:
    # --- voltage ---
    voltage_and_current = Helper.send_command(CommandEnum.GET_VOLTAGE_AND_CURRENT)
    voltage = Helper.merge_bytes_as_decimal(*voltage_and_current[3:5])

    # vpga = Helper.send_command(file, 0x3C)[4]
    p = ParameterStateSingleton().get_instance()
    vpga = p.v_pga
    voltage_fractional_bits_index = int(3 + log2(vpga))

    adc_volts = Helper.calculate_adc_from_raw_value(voltage, vpga)

    # v_slope = Helper.merge_with_fractional_bits(
    #     *Helper.send_command(file, 0x38)[3:7],
    #     fractional_bits=Helper.send_command(file, 0x3F)[voltage_fractional_bits_index],
    #     signed=True
    # )
    # v_inter = Helper.merge_with_fractional_bits(
    #     *Helper.send_command(file, 0x39)[3:7],
    #     fractional_bits=Helper.send_command(file, 0x41)[voltage_fractional_bits_index],
    #     signed=True
    # )

    current = Helper.merge_bytes_as_decimal(*voltage_and_current[5:7])

    # cpga = Helper.send_command(file, 0x3D)[4]
    cpga = p.c_pga
    current_fractional_bits_index = int(3 + log2(cpga))

    adc_current = Helper.calculate_adc_from_raw_value(current, cpga)

    # c_slope = Helper.merge_with_fractional_bits(
    #     *Helper.send_command(file, 0x3A)[3:7],
    #     fractional_bits=Helper.send_command(file, 0x40)[current_fractional_bits_index],
    #     signed=True
    # )
    # c_inter = Helper.merge_with_fractional_bits(
    #     *Helper.send_command(file, 0x3B)[3:7],
    #     fractional_bits=Helper.send_command(file, 0x42)[current_fractional_bits_index],
    #     signed=True
    # )

    return {
        'v': (adc_volts * p.v_slope) + p.v_inter,
        'c': (adc_current * p.c_slope) + p.c_inter,
    }


def set_serial_port(port: str) -> None:
    """
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
    return Helper.merge_bytes_as_decimal(
        *Helper.send_command(CommandEnum.GET_INTERNAL_IDN)[3:7],
        signed=False
    )


def active_unit(channel: int) -> None:
    """
    Ustawia komunikację z jedynm z ośmiu kanałów.
    :param channel: Kanał na którego przestawiamy komunikację. Należy podać liczbę całkowitą z przedziału od 0 do 7.
    """
    if 0 > channel or channel > 7:
        raise Exception("Channel must be between 0 and 7.")

    Helper.send_command(CommandEnum.ACTIVE_UNIT, data_lsb=channel)


def get_unit_idn() -> int:
    """
    :return: Numer identyfikacyjny kanału.
    """
    return Helper.merge_bytes_as_decimal(*Helper.send_command(CommandEnum.GET_UNIT_IDN)[3:7])

# endregion General Commands


# ===========================
# region Calibration Commands
# ===========================
def get_vmin() -> int:
    return Helper.get_vmin()


def get_vmax() -> int:
    return Helper.get_vmax()


def get_cmin() -> int:
    return Helper.get_vmax()


def get_cmax() -> int:
    return Helper.get_cmax()

# endregion Calibration Commands


# ===========================
# region Working Commands
# ===========================

def set_mode():
    return None

# endregion Working Commands


def init() -> None:
    state = ParameterStateSingleton.get_instance()

    state.c_pga = 1
    state.v_pga = 1
    state.q_limits = Helper.send_command(CommandEnum.GET_QLIMITS)


def main():
    init()
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
                response = Helper.send_command(command, data_msb, data_lsb)
                continue

            match keyboard_input:
                case 'vc':
                    response = voltage_and_current(file)
                case 'v_ranges':
                    response = Helper.get_ranges(file)
                case 'c_ranges':
                    response = Helper.get_ranges(file, False)
                case 'v_min':
                    response = Helper.merge_bytes_as_decimal_command_result(Helper.send_command(file, 0x34))
                    # response = Helper.merge_command_result(ParameterStateSingleton.get_instance().v_min, signed=True)
                case 'v_max':
                    response = Helper.merge_bytes_as_decimal_command_result(ParameterStateSingleton.get_instance().v_max)
                    # response = Helper.merge_command_result(Helper.send_command(file, 0x35), signed=True)
                case 'q':
                    return
                case _:
                    continue

            print(response)
            file.write(f"function: {keyboard_input}, response {response}\n")


if __name__ == '__main__':
    main()
