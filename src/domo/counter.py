from typing import ClassVar

from .base import Device, DeviceStaticConfiguration, DeviceSubtype, DeviceSwitchType, DeviceType

class ManagedCounterEnergyDevice(Device):
    """A Domoticz Managed Counter Device to measure Energy"""

    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.GENERAL,
        subtype_id=DeviceSubtype.MANAGED_COUNTER,
        switch_type_id=DeviceSwitchType.ENERGY,
        options={},
        format="-1;{}",
        calculator=None,
    )
