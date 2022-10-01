import Domoticz

class Delta:

    def __init__(self):
        self.prev_value
        self.delta

    def update(self, new_value, scale = 0):
        value = new_value * (10 ** scale)
        self.delta = value - self.prev_value
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

        Domoticz.Debug("Average: {} - {} values".format(self.get(), len(self.samples)))

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

        Domoticz.Debug("Maximum: {} - {} values".format(self.get(), len(self.samples)))

    def get(self):
        return max(self.samples)
