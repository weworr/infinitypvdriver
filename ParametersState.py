class ParametersState:
    # active_channel: int = None
    #
    # v_pga: int = None
    # v_min: int = None
    # v_max: int = None
    # v_slope: int = None
    # v_inter: int = None
    #
    # c_pga: int = None
    # c_min: int = None
    # c_max: int = None
    # c_slope: int = None
    # c_inter: int = None
    #
    # q_limits: list = []
    # q_c_slope: list = []
    # q_c_inter: list = []
    # q_v_slope: list = []
    # q_v_inter: list = []
    #
    # mode: str = None
    # v_ref: int = None
    # v_step: int = None
    # c_step: int = None

    def __init__(self):
        self.__active_channel: int|None = None

        self.__v_pga: int|None = None
        self.__v_min: int|None = None
        self.__v_max: int|None = 10
        self.__v_slope: int|None = None
        self.__v_inter: int|None = None

        self.__c_pga: int|None = None
        self.__c_min: int|None = None
        self.__c_max: int|None = None
        self.__c_slope: int|None = None
        self.__c_inter: int|None = None

        self.__q_limits: list = []
        self.__q_c_slope: list = []
        self.__q_c_inter: list = []
        self.__q_v_slope: list = []
        self.__q_v_inter: list = []

        self.__mode: str|None = None
        self.__v_ref: int|None = None
        self.__v_step: int|None = None
        self.__c_step: int|None = None

    @property
    def active_channel(self):
        return self.__active_channel

    @active_channel.setter
    def active_channel(self, value):
        self.__active_channel = value

    @property
    def v_pga(self) -> int:
        return self.__v_pga

    @v_pga.setter
    def v_pga(self, value: int):
        self.__v_pga = value

    @property
    def v_min(self):
        return self.__v_min

    @v_min.setter
    def v_min(self, value):
        self.__v_min = value

    @property
    def v_max(self):
        return self.__v_max

    @v_max.setter
    def v_max(self, value):
        self.__v_max = value

    @property
    def v_slope(self):
        return self.__v_slope

    @v_slope.setter
    def v_slope(self, value):
        self.__v_slope = value

    @property
    def v_inter(self):
        return self.__v_inter

    @v_inter.setter
    def v_inter(self, value):
        self.__v_inter = value

    @property
    def c_pga(self):
        return self.__c_pga

    @c_pga.setter
    def c_pga(self, value):
        self.__c_pga = value

    @property
    def c_min(self):
        return self.__c_min

    @c_min.setter
    def c_min(self, value):
        self.__c_min = value

    @property
    def c_max(self):
        return self.__c_max

    @c_max.setter
    def c_max(self, value):
        self.__c_max = value

    @property
    def c_slope(self):
        return self.__c_slope

    @c_slope.setter
    def c_slope(self, value):
        self.__c_slope = value

    @property
    def q_limits(self):
        return self.__q_limits

    @q_limits.setter
    def q_limits(self, value):
        self.__q_limits = value

    @property
    def q_c_slope(self):
        return self.__q_c_slope

    @q_c_slope.setter
    def q_c_slope(self, value):
        self.__q_c_slope = value

    @property
    def q_c_inter(self):
        return self.__q_c_inter

    @q_c_inter.setter
    def q_c_inter(self, value):
        self.__q_c_inter = value

    @property
    def q_v_inter(self):
        return self.__q_v_inter

    @q_v_inter.setter
    def q_v_inter(self, value):
        self.__q_v_inter = value

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = value

    @property
    def v_ref(self):
        return self.__v_ref

    @v_ref.setter
    def v_ref(self, value):
        self.__v_ref = value

    @property
    def v_step(self):
        return self.__v_step

    @v_step.setter
    def v_step(self, value):
        self.__v_step = value

    @property
    def c_step(self):
        return self.__c_step

    @c_step.setter
    def c_step(self, value):
        self.__c_step = value