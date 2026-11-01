from typing import ClassVar

from .base import Device, DeviceStaticConfiguration, DeviceSubtype, DeviceSwitchType, DeviceType
from .calculators import Average


class VoltageDevice(Device):
    """A Domoticz Device to measure Voltage"""
    
    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.GENERAL,
        subtype_id=DeviceSubtype.VOLTAGE,
        switch_type_id=DeviceSwitchType.NOT_APPLICABLE,
        options={},
        format="{:.2f}",
        calculator=Average,
    )
