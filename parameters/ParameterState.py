from enums.ModeEnum import ModeEnum


class ParameterState:
    def __init__(self, channel: int):
        self.__channel: int = channel

        self.__v_pga: int = 1
        self.__v_min: float = None
        self.__v_max: float = None
        self.__v_slope: float = None
        self.__v_inter: float = None

        self.__c_pga: int = 1
        self.__c_min: float = None
        self.__c_max: float = None
        self.__c_slope: float = None
        self.__c_inter: float = None

        self.__q_limits_v_min: int = 28
        self.__q_limits_v_max: int = 28
        self.__q_limits_c_min: int = 30
        self.__q_limits_c_max: int = 25

        self.__q_c_slope: list[int] = []  # TODO Do weryfikacji, czy wartość jest stała niezależnie od vref i gain
        self.__q_c_inter: list[int] = []  # TODO Do weryfikacji, czy wartość jest stała niezależnie od vref i gain
        self.__q_v_slope: list[int] = []  # TODO Do weryfikacji, czy wartość jest stała niezależnie od vref i gain
        self.__q_v_inter: list[int] = []  # TODO Do weryfikacji, czy wartość jest stała niezależnie od vref i gain

        self.__mode: str = ModeEnum.VFIX.name
        self.__v_ref: int = 0  # TODO Do weryfikacji, czy wartość jest 0 na start.
        self.__dac_step: int = None
        self.__v_step: int = None

    @property
    def channel(self) -> int:
        return self.__channel

    @channel.setter
    def channel(self, value: int) -> None:
        self.__channel = value

    @property
    def v_pga(self) -> int:
        return self.__v_pga

    @v_pga.setter
    def v_pga(self, value: int) -> None:
        self.__v_pga = value

        self.regenerate_soft_values()

    @property
    def v_min(self) -> float:
        return self.__v_min

    @v_min.setter
    def v_min(self, value: float) -> None:
        self.__v_min = value

    @property
    def v_max(self) -> float:
        return self.__v_max

    @v_max.setter
    def v_max(self, value: float) -> None:
        self.__v_max = value

    @property
    def v_slope(self) -> float:
        return self.__v_slope

    @v_slope.setter
    def v_slope(self, value: float) -> None:
        self.__v_slope = value

    @property
    def v_inter(self) -> float:
        return self.__v_inter

    @v_inter.setter
    def v_inter(self, value: float) -> None:
        self.__v_inter = value

    @property
    def c_pga(self) -> int:
        return self.__c_pga

    @c_pga.setter
    def c_pga(self, value: int) -> None:
        self.__c_pga = value

        self.regenerate_soft_values()

    @property
    def c_min(self) -> float:
        return self.__c_min

    @c_min.setter
    def c_min(self, value: float):
        self.__c_min = value

    @property
    def c_max(self) -> float:
        return self.__c_max

    @c_max.setter
    def c_max(self, value: float) -> None:
        self.__c_max = value

    @property
    def c_slope(self) -> float:
        return self.__c_slope

    @c_slope.setter
    def c_slope(self, value: float) -> None:
        self.__c_slope = value

    @property
    def c_inter(self) -> float:
        return self.__c_inter

    @c_inter.setter
    def c_inter(self, value: float) -> None:
        self.__c_inter = value

    @property
    def q_limits_v_min(self) -> int:
        return self.__q_limits_v_min

    @q_limits_v_min.setter
    def q_limits_v_min(self, value: int) -> None:
        self.__q_limits_v_min = value

    @property
    def q_limits_v_max(self) -> int:
        return self.__q_limits_v_max

    @q_limits_v_max.setter
    def q_limits_v_max(self, value: int) -> None:
        self.__q_limits_v_max = value

    @property
    def q_limits_c_min(self) -> int:
        return self.__q_limits_c_min

    @q_limits_c_min.setter
    def q_limits_c_min(self, value: int) -> None:
        self.__q_limits_c_min = value

    @property
    def q_limits_c_max(self) -> int:
        return self.__q_limits_c_max

    @q_limits_c_max.setter
    def q_limits_c_max(self, value: int) -> None:
        self.__q_limits_c_max = value

    @property
    def q_c_slope(self) -> list[int]:
        return self.__q_c_slope

    @q_c_slope.setter
    def q_c_slope(self, value: list[int]) -> None:
        self.__q_c_slope = value

    @property
    def q_c_inter(self) -> list[int]:
        return self.__q_c_inter

    @q_c_inter.setter
    def q_c_inter(self, value: list[int]) -> None:
        self.__q_c_inter = value

    @property
    def q_v_slope(self) -> list[int]:
        return self.__q_v_slope

    @q_v_slope.setter
    def q_v_slope(self, value: list[int]) -> None:
        self.__q_v_slope = value

    @property
    def q_v_inter(self) -> list[int]:
        return self.__q_v_inter

    @q_v_inter.setter
    def q_v_inter(self, value: list[int]) -> None:
        self.__q_v_inter = value

    @property
    def mode(self) -> str:
        return self.__mode

    @mode.setter
    def mode(self, value: str) -> None:
        self.__mode = value

    @property
    def v_ref(self) -> int:
        return self.__v_ref

    @v_ref.setter
    def v_ref(self, value: int) -> None:
        self.__v_ref = value

    @property
    def dac_step(self) -> int:
        return self.__dac_step

    @dac_step.setter
    def dac_step(self, value: int) -> None:
        self.__dac_step = value

    @property
    def v_step(self) -> float:
        return self.__v_step

    @v_step.setter
    def v_step(self, value: float) -> None:
        self.__v_step = value

    def regenerate_soft_values(self, regenerate_q_limits: bool = True) -> None:
        from services.DriverService import DriverService

        if regenerate_q_limits:
            DriverService.get_q_limits(True)

        DriverService.get_v_min(True)
        DriverService.get_v_max(True)
        DriverService.get_v_slope(True)
        DriverService.get_v_inter(True)

        DriverService.get_c_min(True)
        DriverService.get_c_max(True)
        DriverService.get_c_slope(True)
        DriverService.get_c_inter(True)
