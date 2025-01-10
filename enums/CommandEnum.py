from enum import Enum


class CommandEnum(Enum):
    # =====================
    # General Commands
    # =====================
    GET_INTERNAL_IDN = 0x10
    ACTIVE_UNIT = 0x29
    GET_UNIT_IDN = 0x2F

    # =====================
    # Calibration Commands
    # =====================
    GET_V_MIN = 0x34
    GET_V_MAX = 0x35

    GET_C_MIN = 0x36
    GET_C_MAX = 0x37

    GET_Q_LIMITS = 0x3E

    GET_V_PGA = 0x3C
    GET_C_PGA = 0x3D

    SET_V_PGA = 0x43
    SET_C_PGA = 0x45

    GET_V_SLOPE = 0x38
    GET_V_INTER = 0x39

    GET_C_SLOPE = 0x3A
    GET_C_INTER = 0x3B

    GET_Q_V_SLOPE = 0x3F
    GET_Q_C_SLOPE = 0x40

    GET_Q_V_INTER = 0x41
    GET_Q_C_INTER = 0x42

    # =====================
    # Working Commands
    # =====================
    SET_MODE = 0x2D
    GET_MODE = 0x2E

    SET_VREF = 0x2B
    GET_VOLTAGE_AND_CURRENT = 0x2C
