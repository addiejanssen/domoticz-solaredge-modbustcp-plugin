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


class SunSpecDeviceModel709(SunSpecDevice):
    """Definition for SunSpec Model 709 DER Trip LF"""

    class DerTripLfModuleEnable(IntEnum):
        """States used by this Device"""
    
        DISABLED = 0
        ENABLED = 1
    
    class AdoptCurveResult(IntEnum):
        """States used by this Device"""
    
        IN_PROGRESS = 0
        COMPLETED = 1
        FAILED = 2
    
    device_description: ClassVar[DeviceDescription] = DeviceDescription(
        id=709,
        name="DERTripLF",
        label="DER Trip LF",
        description="DER low frequency trip model."
    )

    register_count: ClassVar[int] = 9
    register_map: ClassVar[RegisterMap] = {
        **SunSpecDevice.register_map,
        "ena": RegisterMapEntry(
            offset=2,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=DerTripLfModuleEnable,
            scaling_item_id="",
            description="DER low frequency trip control enable.",
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
        "ncrvset": RegisterMapEntry(
            offset=6,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Number of stored curves supported.",
        ),
        "hz_sf": RegisterMapEntry(
            offset=7,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Scale factor for curve frequency points.",
        ),
        "tms_sf": RegisterMapEntry(
            offset=8,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Scale factor for curve time points.",
        ),
    }
