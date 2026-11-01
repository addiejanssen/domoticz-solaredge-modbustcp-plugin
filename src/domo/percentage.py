from typing import ClassVar

from .base import Device, DeviceStaticConfiguration, DeviceSubtype, DeviceSwitchType, DeviceType
from .calculators import Average


class PercentageDevice(Device):
    """A Domoticz Device to log Percentages"""

    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.GENERAL,
        subtype_id=DeviceSubtype.PERCENTAGE,
        switch_type_id=DeviceSwitchType.NOT_APPLICABLE,
        options={},
        format="{:.2f}",
        calculator=Average,
    )
