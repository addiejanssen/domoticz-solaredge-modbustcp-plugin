from typing import ClassVar

from .base import Device, DeviceStaticConfiguration, DeviceSubtype, DeviceSwitchType, DeviceType
from .calculators import Above

class EnergyDevice(Device):
    """A Domoticz Device to measure (bi-directional) Energy"""

    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.GENERAL,
        subtype_id=DeviceSubtype.ENERGY,
        switch_type_id=DeviceSwitchType.EXPORTING,
        options={},
        format="{:.0f};{:.0f}",
        calculator=None,
    )


class EnergyExportDevice(Device):
    """
    A Domoticz Device to measure Exported Energy.
    The primary input for this device is the current power.
    The calculator will only show values of current power that are above 0.
    """

    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.GENERAL,
        subtype_id=DeviceSubtype.ENERGY,
        switch_type_id=DeviceSwitchType.EXPORTING,
        options={},
        format="{:.0f};{:.0f}",
        calculator=Above(base=0, multiplier=1),
    )


class EnergyImportDevice(Device):
    """
    A Domoticz Device to measure Imported Energy.
    The primary input for this device is the current power.
    The calculator will only show values of the current power that are below 0 and
    it will invert the value to show the negative values as positives in the graphs.
    """

    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.GENERAL,
        subtype_id=DeviceSubtype.ENERGY,
        switch_type_id=DeviceSwitchType.IMPORTING,
        options={},
        format="{:.0f};{:.0f}",
        calculator=Above(base=0, multiplier=-1),
    )
