from typing import ClassVar

from .base import Device, DeviceStaticConfiguration, DeviceSubtype, DeviceSwitchType, DeviceType
from .calculators import Maximum


class TemperatureDevice(Device):
    """A Domoticz Device to measure Temperature"""

    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.GENERAL,
        subtype_id=DeviceSubtype.TEMPERATURE,
        switch_type_id=DeviceSwitchType.NOT_APPLICABLE,
        options={},
        format="{:.2f}",
        calculator=Maximum,
    )
