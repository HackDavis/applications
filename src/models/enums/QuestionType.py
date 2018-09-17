from enum import auto, Enum


class QuestionType(Enum):
    communicationsOptIn = auto()
    demographic = auto()
    dietaryRestriction = auto()
    email = auto()
    essay = auto()
    ignore = auto()
    link = auto()
    resumeLink = auto()
    resumeSharingOptIn = auto()
    shirtSize = auto()
    interest = auto()
    interestYesNo = auto()
    age = auto()
    university = auto()
