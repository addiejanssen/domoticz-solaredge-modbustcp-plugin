"""
SunSpec Device Model

Author:  Addie Janssen (https://addiejanssen.com)
License: MIT

Do not modify this file - it is generated from the SunSpec Model Definitions
as published here: https://github.com/sunspec/models - commit: 90b4a33

Any changes made to this file will be lost on the next generation of the model.
"""

from enum import IntEnum
from typing import ClassVar

from ..base import DeviceDescription, ModbusDataType, ModbusWordOrder, RegisterMap, RegisterMapEntry
from .base import SunSpecDevice


class SunSpecDeviceModel711(SunSpecDevice):
    """Definition for SunSpec Model 711 DER Frequency Droop"""

    class DerFrequencyDroopModuleEnable(IntEnum):
        """States used by this Device"""
    
        DISABLED = 0
        ENABLED = 1
    
    class SetActiveControlResult(IntEnum):
        """States used by this Device"""
    
        IN_PROGRESS = 0
        COMPLETED = 1
        FAILED = 2
    
    device_description: ClassVar[DeviceDescription] = DeviceDescription(
        id=711,
        name="DERFreqDroop",
        label="DER Frequency Droop",
        description="DER Frequency Droop model."
    )

    register_count: ClassVar[int] = 14
    register_map: ClassVar[RegisterMap] = {
        **SunSpecDevice.register_map,
        "ena": RegisterMapEntry(
            offset=2,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=DerFrequencyDroopModuleEnable,
            scaling_item_id="",
            description="DER Frequency-Watt (Frequency-Droop) control enable.",
        ),
        "adptctlreq": RegisterMapEntry(
            offset=3,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Set active control. 0 = No active control.",
        ),
        "adptctlrslt": RegisterMapEntry(
            offset=4,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=SetActiveControlResult,
            scaling_item_id="",
            description="Result of last set active control operation.",
        ),
        "nctl": RegisterMapEntry(
            offset=5,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Number of stored controls supported.",
        ),
        "rvrttms": RegisterMapEntry(
            offset=6,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Reversion time in seconds.  0 = No reversion time.",
        ),
        "rvrtrem": RegisterMapEntry(
            offset=8,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Reversion time remaining in seconds.",
        ),
        "rvrtctl": RegisterMapEntry(
            offset=10,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Default control after reversion timeout.",
        ),
        "db_sf": RegisterMapEntry(
            offset=11,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Deadband scale factor.",
        ),
        "k_sf": RegisterMapEntry(
            offset=12,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Frequency change scale factor.",
        ),
        "rsptms_sf": RegisterMapEntry(
            offset=13,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Open loop response time scale factor.",
        ),
    }
