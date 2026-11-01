from typing import ClassVar

from .base import Device, DeviceStaticConfiguration, DeviceSubtype, DeviceSwitchType, DeviceType


class EnergyExportDevice(Device):
    """A Domoticz Device to measure Exported Energy"""

    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.GENERAL,
        subtype_id=DeviceSubtype.ENERGY,
        switch_type_id=DeviceSwitchType.EXPORTING,
        options={},
        format="{:.0f};{:.0f}",
        calculator=None,
    )


class EnergyImportDevice(Device):
    """A Domoticz Device to measure Imported Energy"""

    configuration: ClassVar[DeviceStaticConfiguration] = DeviceStaticConfiguration(
        type_id=DeviceType.GENERAL,
        subtype_id=DeviceSubtype.ENERGY,
        switch_type_id=DeviceSwitchType.IMPORTING,
        options={},
        format="{:.0f};{:.0f}",
        calculator=None,
    )
