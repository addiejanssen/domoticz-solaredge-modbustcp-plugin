from typing import ClassVar

from .base import Device, DeviceStaticConfiguration, DeviceSubtype, DeviceSwitchType, DeviceType
from .calculators import Average


class CurrentDevice(Device):
    """A Domoticz Device to measure Current"""

    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.GENERAL,
        subtype_id=DeviceSubtype.CURRENT,
        switch_type_id=DeviceSwitchType.NOT_APPLICABLE,
        options={},
        format="{:.2f}",
        calculator=Average,
    )
