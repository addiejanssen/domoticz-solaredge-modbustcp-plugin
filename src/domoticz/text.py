from typing import ClassVar

from .base import Device, DeviceStaticConfiguration, DeviceSubtype, DeviceSwitchType, DeviceType


class TextStatusDevice(Device):
    """A Domoticz Device to keep track of a status as text"""

    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.GENERAL,
        subtype_id=DeviceSubtype.TEXT_STATUS,
        switch_type_id=DeviceSwitchType.NOT_APPLICABLE,
        options={},
        format="{}",
        calculator=None,
    )
