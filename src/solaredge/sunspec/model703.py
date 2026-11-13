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


class SunSpecDeviceModel703(SunSpecDevice):
    """Definition for SunSpec Model 703 Enter Service"""

    class PermitEnterService(IntEnum):
        """States used by this Device"""
    
        DISABLED = 0
        ENABLED = 1
    
    device_description: ClassVar[DeviceDescription] = DeviceDescription(
        id=703,
        name="DEREnterService",
        label="Enter Service",
        description="Enter service model."
    )

    register_count: ClassVar[int] = 19
    register_map: ClassVar[RegisterMap] = {
        **SunSpecDevice.register_map,
        "es": RegisterMapEntry(
            offset=2,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=PermitEnterService,
            scaling_item_id="",
            description="Permit enter service.",
        ),
        "esvhi": RegisterMapEntry(
            offset=3,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Enter service voltage high threshold as percent of normal voltage.",
        ),
        "esvlo": RegisterMapEntry(
            offset=4,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Enter service voltage low threshold as percent of normal voltage.",
        ),
        "eshzhi": RegisterMapEntry(
            offset=5,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="hz_sf",
            description="Enter service frequency high threshold.",
        ),
        "eshzlo": RegisterMapEntry(
            offset=7,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="hz_sf",
            description="Enter service frequency low threshold.",
        ),
        "esdlytms": RegisterMapEntry(
            offset=9,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Enter service delay time in seconds.",
        ),
        "esrndtms": RegisterMapEntry(
            offset=11,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Enter service random delay in seconds.",
        ),
        "esrmptms": RegisterMapEntry(
            offset=13,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Enter service ramp time in seconds.",
        ),
        "esdlyremtms": RegisterMapEntry(
            offset=15,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Enter service delay time remaining in seconds.",
        ),
        "v_sf": RegisterMapEntry(
            offset=17,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Voltage percentage scale factor.",
        ),
        "hz_sf": RegisterMapEntry(
            offset=18,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Frequency scale factor.",
        ),
    }
