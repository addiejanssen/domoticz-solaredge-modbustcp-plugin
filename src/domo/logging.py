"""
Domoticz logging related helpers
"""

from enum import IntEnum, unique

import Domoticz


@unique
class LogLevels(IntEnum):
    """
    Log levels for controlling the verbosity of logging output.
    NORMAL: Standard logging level, shows essential information.
    INFO: Shows additional information for informational purposes.
    DEBUG: Extensive information for in-depth debugging purposes.
    """

    NORMAL = 0
    INFO = 1
    DEBUG = 2


CurrentLogLevel: LogLevels = LogLevels.NORMAL


def SetLogLevel(level: LogLevels) -> None:
    """Set the current logging level."""
    global CurrentLogLevel
    CurrentLogLevel = level


def DomoLog(level: LogLevels, message: str) -> None:
    """Log a message if the current logging level is greater than or equal to the specified level."""
    if CurrentLogLevel >= level:
        Domoticz.Log(message)
