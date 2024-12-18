from ParametersState import ParametersState

class ParameterStateSingleton:
    __instance: ParametersState|None = None

    def __init__(self):
        pass

    @staticmethod
    def get_instance() -> ParametersState:
        if ParameterStateSingleton.__instance is None:
            ParameterStateSingleton.__instance = ParametersState()

        return ParameterStateSingleton.__instance
