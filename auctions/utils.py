from enum import Enum


class BaseEnumChoice(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
