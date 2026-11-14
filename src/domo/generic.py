from typing import ClassVar

from .base import Device, DeviceStaticConfiguration, DeviceSubtype, DeviceSwitchType, DeviceType


class GenericNumberDevice(Device):
    """A Domoticz Device to display a generic number"""

    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.GENERAL,
        subtype_id=DeviceSubtype.CUSTOM,
        switch_type_id=DeviceSwitchType.NOT_APPLICABLE,
        options={},
        format="{:.2f}",
        calculator=None,
    )
