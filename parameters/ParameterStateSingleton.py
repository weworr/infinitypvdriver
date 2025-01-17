from parameters.ParameterState import ParameterState


class ParameterStateSingleton:
    __MAX_CHANNEL: int = 8
    __instances: list[ParameterState] = [ParameterState(i) for i in range(__MAX_CHANNEL)]
    __active_channel: int = 0

    def __init__(self):
        pass

    @staticmethod
    def set_active_channel(channel: int) -> None:
        ParameterStateSingleton.__active_channel = channel

    @staticmethod
    def get_active_channel() -> int:
        return ParameterStateSingleton.__active_channel

    @staticmethod
    def get_max_channel() -> int:
        return ParameterStateSingleton.__MAX_CHANNEL

    @staticmethod
    def get_instance() -> ParameterState:
        if ParameterStateSingleton.__active_channel is None:
            raise RuntimeError('Active channel is not set.')

        return ParameterStateSingleton.__instances[ParameterStateSingleton.__active_channel]

    @staticmethod
    def get_all_instances() -> list[ParameterState]:
        return ParameterStateSingleton.__instances
