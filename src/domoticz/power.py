"""
The Three Types of AC Power:

In an AC system, electricity does not always flow in a straight, simple line. Total power is split into three parts:
- Active Power (Real Power, P): Measured in Watts (W). This is the actual energy that does useful work—like turning a motor shaft, lighting a bulb, or heating a stove.
- Reactive Power (Q): Measured in Volt-Amperes Reactive (VAR). This energy surges back and forth between the power source and magnetic/electric fields in devices like motors and transformers. It does no net useful work, but it is required to keep machines running.
- Apparent Power (S): Measured in Volt-Amperes (VA). This is the combined total of active power and reactive power.

The Beer Analogy

Think of a glass of poured beer:
- The Liquid Beer (Active Power): The part you actually drink and enjoy (the useful work).
- The Foamy Head (Reactive Power): The part that takes up space in the glass but isn't liquid beer (the necessary field energy).
- The Total Volume in the Glass (Apparent Power): The combined space of both the beer and the foam that the glass has to hold.
"""

from typing import ClassVar

from .base import Device, DeviceStaticConfiguration, DeviceSubtype, DeviceSwitchType, DeviceType
from .calculators import Average


class PowerDevice(Device):
    """A Domoticz Device to measure Power"""

    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.USAGE,
        subtype_id=DeviceSubtype.ELECTRIC,
        switch_type_id=DeviceSwitchType.NOT_APPLICABLE,
        options={},
        format="{:.0f}",
        calculator=Average,
    )


class ReactivePowerDevice(Device):
    """A Domoticz Device to measure Reactive Power"""

    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.GENERAL,
        subtype_id=DeviceSubtype.CUSTOM,
        switch_type_id=DeviceSwitchType.NOT_APPLICABLE,
        options={"Custom": "1;var"},
        format="{:.0f}",
        calculator=Average,
    )


class ApparentPowerDevice(Device):
    """A Domoticz Device to measure Apparent Power"""

    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.GENERAL,
        subtype_id=DeviceSubtype.CUSTOM,
        switch_type_id=DeviceSwitchType.NOT_APPLICABLE,
        options={"Custom": "1;VA"},
        format="{:.0f}",
        calculator=Average,
    )
