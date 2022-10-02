import Domoticz

from enum import IntEnum, unique

#
# A nice way to only show what we want to show.
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
# Meters can measure power, which can show a positive or negative
# value depending on the direction of the power.
# In certain scenario's we want to split it up and "swap" the graph.
# Showing positive values for both flows of power and only
# have the part where the value is more than 0.
# That's where this class comes into play.
#

class Above:
    def __init__(self, base, multiplier):
        self.base = base
        self.multiplier = multiplier

    def get(self, value):
        if (value * self.multiplier) >= self.base:
            return value * self.multiplier
        else:
            return 0

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
