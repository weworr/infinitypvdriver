class ParametersState:
    def __init__(self, channel: int):
        self.__channel: int = channel

        self.__v_pga: int = 1
        self.__v_min: int | None = None
        self.__v_max: int | None = None
        self.__v_slope: int | None = None
        self.__v_inter: int | None = None

        self.__c_pga: int = 1
        self.__c_min: int | None = None
        self.__c_max: int | None = None
        self.__c_slope: int | None = None
        self.__c_inter: int | None = None

        self.__q_limits: list[int] = []
        self.__q_c_slope: list[int] = []
        self.__q_c_inter: list[int] = []
        self.__q_v_slope: list[int] = []
        self.__q_v_inter: list[int] = []

        self.__mode: str | None = None
        self.__v_ref: int | None = None
        self.__v_step: int | None = None
        self.__c_step: int | None = None

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
    def v_min(self) -> int | None:
        return self.__v_min

    @v_min.setter
    def v_min(self, value: int) -> None:
        self.__v_min = value

    @property
    def v_max(self) -> int | None:
        return self.__v_max

    @v_max.setter
    def v_max(self, value: int) -> None:
        self.__v_max = value

    @property
    def v_slope(self) -> int | None:
        return self.__v_slope

    @v_slope.setter
    def v_slope(self, value: int) -> None:
        self.__v_slope = value

    @property
    def v_inter(self) -> int | None:
        return self.__v_inter

    @v_inter.setter
    def v_inter(self, value: int) -> None:
        self.__v_inter = value

    @property
    def c_pga(self) -> int:
        return self.__c_pga

    @c_pga.setter
    def c_pga(self, value: int) -> None:
        self.__c_pga = value

        self.regenerate_soft_values()

    @property
    def c_min(self) -> int | None:
        return self.__c_min

    @c_min.setter
    def c_min(self, value: int):
        self.__c_min = value

    @property
    def c_max(self) -> int | None:
        return self.__c_max

    @c_max.setter
    def c_max(self, value: int) -> None:
        self.__c_max = value

    @property
    def c_slope(self) -> int | None:
        return self.__c_slope

    @c_slope.setter
    def c_slope(self, value: int) -> None:
        self.__c_slope = value

    @property
    def c_inter(self) -> int | None:
        return self.__c_inter

    @c_inter.setter
    def c_inter(self, value: int) -> None:
        self.__c_inter = value

    @property
    def q_limits(self) -> list:
        return self.__q_limits

    @q_limits.setter
    def q_limits(self, value: list) -> None:
        self.__q_limits = value

    @property
    def q_c_slope(self) -> list:
        return self.__q_c_slope

    @q_c_slope.setter
    def q_c_slope(self, value) -> None:
        self.__q_c_slope = value

    @property
    def q_c_inter(self) -> list:
        return self.__q_c_inter

    @q_c_inter.setter
    def q_c_inter(self, value) -> None:
        self.__q_c_inter = value

    @property
    def q_v_inter(self) -> list:
        return self.__q_v_inter

    @q_v_inter.setter
    def q_v_inter(self, value: list) -> None:
        self.__q_v_inter = value

    @property
    def mode(self) -> str | None:
        return self.__mode

    @mode.setter
    def mode(self, value: str) -> None:
        self.__mode = value

    @property
    def v_ref(self) -> int | None:
        return self.__v_ref

    @v_ref.setter
    def v_ref(self, value: int) -> None:
        self.__v_ref = value

    @property
    def v_step(self) -> int | None:
        return self.__v_step

    @v_step.setter
    def v_step(self, value: int) -> None:
        self.__v_step = value

    @property
    def c_step(self) -> int | None:
        return self.__c_step

    @c_step.setter
    def c_step(self, value: int) -> None:
        self.__c_step = value

    def regenerate_soft_values(self) -> None:
        from utils.HelperFunctions import Helper

        self.v_min = Helper.get_v_min()
        self.v_max = Helper.get_v_max()
        self.v_slope = Helper.get_v_slope()
        self.v_inter = Helper.get_v_inter()

        self.c_min = Helper.get_c_min()
        self.c_max = Helper.get_c_max()
        self.c_slope = Helper.get_c_slope()
        self.c_inter = Helper.get_c_inter()
