from enum import auto, Enum


class QuestionType(Enum):
    ignore = auto()
    essay = auto()
    multiple_choice = auto()
