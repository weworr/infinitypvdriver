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
    GET_VMIN = 0x34
    GET_VMAX = 0x35

    GET_CMIN = 0x36
    GET_CMAX = 0x37

    GET_QLIMITS = 0x3E

    GET_VPGA = 0x3C
    GET_CPGA = 0x3D

    SET_VPGA = 0x43
    SET_CPGA = 0x45

    GET_VSLOPE = 0x38
    GET_VINTER = 0x39

    GET_CSLOPE = 0x3A
    GET_CINTER = 0x3B

    GET_QVSLOPE = 0x3F
    GET_QCSLOPE = 0x40

    GET_QVINTER = 0x41
    GET_QCINTER = 0x42

    # =====================
    # Working Commands
    # =====================
    SET_MODE = 0x2D
    GET_MODE = 0x2E

    SET_VREF = 0x2B
    GET_VOLTAGE_AND_CURRENT = 0x2C
