from enum import Enum


class GroupSettingResult(Enum):
    SUCCESS: int = 0
    NO_SCHEDULE: int = 1
    NO_GROUP: int = 2


class DistributionMode(Enum):
    SILENT: int = 0
    MORNING: int = 1
    EVENING: int = 2


class TrackerKeys(Enum):
    START: int = 0

    TODAY: int = 1
    TOMORROW: int = 2
    WEEKDAYS: int = 3

    OPTIONS: int = 4
    DISTRIBUTION: int = 5

    DONATIONS: int = 6
    HELP: int = 7
    WEBSITE: int = 8
    GROUP_INPUT = 9
    REPORT_INPUT = 10


class DialogResult(Enum):
    YES = 1,
    NO = 0,
    UNKNOWN = -1




