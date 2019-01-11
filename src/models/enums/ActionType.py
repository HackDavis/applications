from enum import auto, Enum


class ActionType(Enum):
    configure_settings = auto()
    configure_weights = auto()
    export = auto()
    load = auto()
    reload = auto()
    score = auto()
    skip = auto()
