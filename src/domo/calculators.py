from datetime import datetime, timedelta

class Calculator:
    """Base class for all calculator classes"""

    def update(self, new_value: float) -> float:
        """
        Update the calculation and return the updated value.
        """
        return self.get()

    def get(self) -> float:
        """
        Abstract method to retrieve a value based on the stored samples.
        This method should be implemented by subclasses to provide specific calculations (e.g., average, maximum)
        """
        raise NotImplementedError("Subclasses must implement the get method.")


class TimedSampleList(Calculator):
    """
    A class to store samples with timestamps and provide methods to update and retrieve values based on a sliding window of time.
    The samples are stored as a list of tuples, where each tuple contains a timestamp and a corresponding value.
    On update, the class appends a new sample and removes any samples that are older than 5 minutes.
    """

    def __init__(self) -> None:
        self.samples: list[tuple[datetime, float]] = []
        self.max_time: timedelta = timedelta(minutes=5)

    def update(self, new_value: float) -> float:
        """
        Update the sample list with a new value and remove any samples that are older than the maximum time window.
        """
        now: datetime = datetime.now()
        self.samples.append((now, new_value))

        self.prune()

        return self.get()

    def prune(self) -> None:
        """
        Prune the sample list by removing any samples that are older than the maximum time window.
        """
        if self.samples:
            now: datetime = datetime.now()
            self.samples = [(timestamp, value) for timestamp,
                            value in self.samples if now - timestamp <= self.max_time]

class Average(TimedSampleList):
    """
    A class to calculate the average value based on a sliding window of samples.
    Inherits from TimedSampleList and implements the get method to return the average of the stored samples.
    """

    def __init__(self) -> None:
        super().__init__()

    def get(self) -> float:
        """
        Calculate the average of the stored samples.

        Returns
        -------
            float: The average value of the samples, or 0 if there are no samples.
        """
        self.prune()  # Ensure samples are pruned before calculating the average

        if self.samples:
            sum_value: float = sum(value for _, value in self.samples)
            return sum_value / len(self.samples)
        else:
            return 0


class Maximum(TimedSampleList):
    """
    A class to calculate the maximum value based on a sliding window of samples.
    Inherits from TimedSampleList and implements the get method to return the maximum of the stored samples.
    """

    def __init__(self) -> None:
        super().__init__()

    def get(self) -> float:
        """
        Calculate the maximum of the stored samples.

        Returns
        -------
            float: The maximum value of the samples, or 0 if there are no samples.
        """
        self.prune()  # Ensure samples are pruned before calculating the maximum

        if self.samples:
            return max(value for _, value in self.samples)
        else:
            return 0


class AboveZero(Calculator):
    """
    Meters can measure power, which can show a positive or negative value depending on the direction of the power.
    In certain scenarios, we want to show a graph for one direction.
    This class only returns all values above zero.
    """

    def __init__(self) -> None:
        self.value = 0

    def update(self, new_value: float) -> float:
        """We are only interested in values above 0 (zero)"""
        if new_value > 0:
            self.value = new_value
        else:
            self.value = 0

        return self.value

    def get(self) -> float:
        """Return the current value"""
        return self.value


class BelowZero(Calculator):
    """
    Meters can measure power, which can show a positive or negative value depending on the direction of the power.
    In certain scenarios, we want to show a graph for one direction.
    This class only returns all values below zero, however, it will invert the returned value.
    Therefore, a value of 1 will result in 0, and a value of -1 will result in 1.
    """

    def update(self, new_value: float) -> float:
        """We are only interested in values below 0 (zero), but we want to make sure that we return a positive value"""
        if new_value < 0:
            self.value = -new_value
        else:
            self.value = 0

        return self.value

    def get(self) -> float:
        """Return the current value"""
        return self.value
