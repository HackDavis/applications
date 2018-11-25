from enum import auto, Enum


class QuestionType(Enum):
    communicationsOptIn = auto()
    demographic = auto()
    dietaryRestriction = auto()
    email = auto()
    essay = auto()
    firstName = auto()
    ignore = auto()
    lastName = auto()
    link = auto()
    resumeLink = auto()
    resumeSharingOptIn = auto()
    shirtSize = auto()
    checkbox = auto()
