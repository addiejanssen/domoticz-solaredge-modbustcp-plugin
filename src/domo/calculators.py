from datetime import datetime, timedelta

class Calculator:
    """Base class for all calculator classes"""

    pass


class TimedSampleList(Calculator):
    """
    A class to store samples with timestamps and provide methods to update and retrieve values based on a sliding window of time.
    The samples are stored as a list of tuples, where each tuple contains a timestamp and a corresponding value.
    On update, the class appends a new sample and removes any samples that are older than 5 minutes.
    """

    def __init__(self) -> None:
        self.samples: list[tuple[datetime, float]] = []
        self.max_time: timedelta = timedelta(minutes=5)

    def update(self, append_value: float) -> float:
        """
        Update the sample list with a new value and remove any samples that are older than the maximum time window.
        """
        now: datetime = datetime.now()
        self.samples.append((now, append_value))

        self.prune()

        return self.get()

    def get(self) -> float:
        """
        Abstract method to retrieve a value based on the stored samples.
        This method should be implemented by subclasses to provide specific calculations (e.g., average, maximum)
        """
        raise NotImplementedError("Subclasses must implement the get method.")

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


class Above(Calculator):
    """
    Meters can measure power, which can show a positive or negative value depending on the direction of the power.
    In certain scenarios, we want to show a graph with only positive values for both flows of power.
    This class filters values based on a base threshold and a multiplier.
    If the value multiplied by the multiplier is greater than or equal to the base threshold,
    the method returns the multiplied value; otherwise, it returns 0.
    """

    def __init__(self, base: float, multiplier: int) -> None:
        self.base: float = base
        self.multiplier: int = multiplier

    def get(self, value: float) -> float:
        """
        Filter the input value based on the base threshold and multiplier.

        Returns
        -------
            float: The filtered value, or 0 if the condition is not met.
        """
        if (value * self.multiplier) >= self.base:
            return value * self.multiplier
        else:
            return 0
