from typing import ClassVar

from .base import Device, DeviceStaticConfiguration, DeviceSubtype, DeviceSwitchType, DeviceType
from .calculators import Average


class FrequencyDevice(Device):
    """A Domoticz Device to measure Frequency"""

    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.GENERAL,
        subtype_id=DeviceSubtype.CUSTOM,
        switch_type_id=DeviceSwitchType.NOT_APPLICABLE,
        options={"Custom": "1;Hz"},
        format="{:.2f}",
        calculator=Average,
    )
