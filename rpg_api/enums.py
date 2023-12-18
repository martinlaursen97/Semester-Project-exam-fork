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


class CharacterClass(StrEnum):
    """
    Character class Enum.

    `mage`: Character is a mage
    `warrior`: Character is a Warrior
    `shaman`: Character is a Shaman
    """

    mage = "mage"
    warrior = "warrior"
    shaman = "shaman"


class ItemType(StrEnum):
    """
    Item type Enum.

    `head`: Item that can be equipped to head
    `chest`: Item that can be equipped to neck
    `legs`: Item that can be equipped to legs
    `boots`: Item that can be equipped to boots
    `weapon`: Item that can be used as weapon
    """

    head = "head"
    chest = "chest"
    legs = "legs"
    boots = "boots"
    weapon = "weapon"


class MAttributeType(StrEnum):
    """
    Attribute Enum.

    `strength`: strength attribute
    `dexterity`: dexterity attribute
    `constitution`: constitution attribute
    `intelligence`: intelligence attribute
    `wisdom`: wisdom attribute
    `charisma`: charisma attribute
    """

    strength = "strength"
    dexterity = "dexterity"
    constitution = "constitution"
    intelligence = "intelligence"
    wisdom = "wisdom"
    charisma = "charisma"
