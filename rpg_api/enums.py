from enum import StrEnum


class UserStatus(StrEnum):
    """
    Status of the user.

    `active`: user is active
    `inactive`: user is inactive
    """

    active = "active"
    inactive = "inactive"


class Gender(StrEnum):
    """
    Gender Enum.

    `male`: gender is male
    `female`: gender is female
    `other`: gender is other
    """

    male = "male"
    female = "female"
    other = "other"
