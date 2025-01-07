from ParametersState import ParametersState


class ParameterStateSingleton:
    __MAX_CHANNEL: int = 8
    __instances: list[ParametersState] = [ParametersState(i) for i in range(__MAX_CHANNEL)]
    __active_channel: int | None = None

    def __init__(self):
        pass

    @staticmethod
    def set_active_channel(channel: int) -> None:
        ParameterStateSingleton.__active_channel = channel

    @staticmethod
    def get_max_channel() -> int:
        return ParameterStateSingleton.__MAX_CHANNEL

    @staticmethod
    def get_instance() -> ParametersState:
        return ParameterStateSingleton.__instances[ParameterStateSingleton.__active_channel]

    @staticmethod
    def get_all_instances() -> list[ParametersState]:
        return ParameterStateSingleton.__instances
