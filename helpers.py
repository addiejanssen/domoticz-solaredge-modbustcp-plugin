from concurrent.futures.process import EXTRA_QUEUED_CALLS
from re import VERBOSE
from tkinter import ALL
from tkinter.font import NORMAL
import Domoticz

from enum import IntEnum, unique


#
# Logging
#

@unique
class LogLevels(IntEnum):

    NORMAL      = 0
    VERBOSE     = 1
    EXTRA       = 2
    ALL         = 3

CurrentLogLevel = LogLevels.NORMAL

def SetLogLevel(level):
    global CurrentLogLevel
    CurrentLogLevel = level

def DomoLog(level, message):
    if (CurrentLogLevel >= level):
        Domoticz.Log(message)

#
# The kWh device expects 2 values, but we don't always have them.
# The Delta class calculates a delta between 2 values and
# that is used to satisfy the kWh device.
#

class Delta:

    def __init__(self):
        self.prev_value = 0
        self.delta = 0

    def update(self, new_value, scale = 0):
        value = new_value * (10 ** scale)
        self.delta = value - self.prev_value
        DomoLog(LogLevels.ALL, "Delta: {} - {} = {}".format(value, self.prev_value, self.delta))
        self.prev_value = value

    def get(self):
        return self.delta


#
# Domoticz shows graphs with intervals of 5 minutes.
# When collecting information from the inverter more frequently than that, then it makes no sense to only show the last value.
#
# The Average class can be used to calculate the average value based on a sliding window of samples.
# The number of samples stored depends on the interval used to collect the value from the inverter itself.
#

class Average:

    def __init__(self):
        self.samples = []
        self.max_samples = 30

    def set_max_samples(self, max):
        self.max_samples = max
        if self.max_samples < 1:
            self.max_samples = 1

    def update(self, new_value, scale = 0):
        self.samples.append(new_value * (10 ** scale))
        while (len(self.samples) > self.max_samples):
            del self.samples[0]

        DomoLog(LogLevels.ALL, "Average: {} - {} values".format(self.get(), len(self.samples)))

    def get(self):
        return sum(self.samples) / len(self.samples)

#
# Domoticz shows graphs with intervals of 5 minutes.
# When collecting information from the inverter more frequently than that, then it makes no sense to only show the last value.
#
# The Maximum class can be used to calculate the highest value based on a sliding window of samples.
# The number of samples stored depends on the interval used to collect the value from the inverter itself.
#

class Maximum:

    def __init__(self):
        self.samples = []
        self.max_samples = 30

    def set_max_samples(self, max):
        self.max_samples = max
        if self.max_samples < 1:
            self.max_samples = 1

    def update(self, new_value, scale = 0):
        self.samples.append(new_value * (10 ** scale))
        while (len(self.samples) > self.max_samples):
            del self.samples[0]

        DomoLog(LogLevels.ALL, "Maximum: {} - {} values".format(self.get(), len(self.samples)))

    def get(self):
        return max(self.samples)
