from enum import StrEnum, auto


class Roles(StrEnum):
    User = auto()
    Admin = auto()
    SuperAdmin = auto()
    Deactivated = auto()
    Unverified = auto()
