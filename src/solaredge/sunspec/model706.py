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


class SunSpecDeviceModel706(SunSpecDevice):
    """Definition for SunSpec Model 706 DER Volt-Watt"""

    class DerVoltWattModuleEnable(IntEnum):
        """States used by this Device"""
    
        DISABLED = 0
        ENABLED = 1
    
    class AdoptCurveResult(IntEnum):
        """States used by this Device"""
    
        IN_PROGRESS = 0
        COMPLETED = 1
        FAILED = 2
    
    device_description: ClassVar[DeviceDescription] = DeviceDescription(
        id=706,
        name="DERVoltWatt",
        label="DER Volt-Watt",
        description="DER Volt-Watt model."
    )

    register_count: ClassVar[int] = 15
    register_map: ClassVar[RegisterMap] = {
        **SunSpecDevice.register_map,
        "ena": RegisterMapEntry(
            offset=2,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=DerVoltWattModuleEnable,
            scaling_item_id="",
            description="Volt-Watt control enable.",
        ),
        "adptcrvreq": RegisterMapEntry(
            offset=3,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Index of curve points to adopt. First curve index is 1.",
        ),
        "adptcrvrslt": RegisterMapEntry(
            offset=4,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=AdoptCurveResult,
            scaling_item_id="",
            description="Result of last adopt curve operation.",
        ),
        "npt": RegisterMapEntry(
            offset=5,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Number of curve points supported.",
        ),
        "ncrv": RegisterMapEntry(
            offset=6,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Number of stored curves supported.",
        ),
        "rvrttms": RegisterMapEntry(
            offset=7,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Reversion time in seconds.  0 = No reversion time.",
        ),
        "rvrtrem": RegisterMapEntry(
            offset=9,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Reversion time remaining in seconds.",
        ),
        "rvrtcrv": RegisterMapEntry(
            offset=11,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Default curve after reversion timeout.",
        ),
        "v_sf": RegisterMapEntry(
            offset=12,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Scale factor for curve voltage points.",
        ),
        "deptref_sf": RegisterMapEntry(
            offset=13,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Scale factor for curve watt points.",
        ),
        "rsptms_sf": RegisterMapEntry(
            offset=14,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Open loop response time scale factor.",
        ),
    }
