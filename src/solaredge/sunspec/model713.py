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


class SunSpecDeviceModel713(SunSpecDevice):
    """Definition for SunSpec Model 713 DER Storage Capacity"""

    class Status(IntEnum):
        """States used by this Device"""
    
        OK = 0
        WARNING = 1
        ERROR = 2
    
    device_description: ClassVar[DeviceDescription] = DeviceDescription(
        id=713,
        name="DERStorageCapacity",
        label="DER Storage Capacity",
        description="DER storage capacity."
    )

    register_count: ClassVar[int] = 9
    register_map: ClassVar[RegisterMap] = {
        **SunSpecDevice.register_map,
        "whrtg": RegisterMapEntry(
            offset=2,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="wh_sf",
            description="Energy rating of the DER storage.",
        ),
        "whavail": RegisterMapEntry(
            offset=3,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="wh_sf",
            description="Energy available of the DER storage (WHAvail = WHRtg * SoC * SoH)",
        ),
        "soc": RegisterMapEntry(
            offset=4,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="pct_sf",
            description="State of charge of the DER storage.",
        ),
        "soh": RegisterMapEntry(
            offset=5,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="pct_sf",
            description="State of health of the DER storage.",
        ),
        "sta": RegisterMapEntry(
            offset=6,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=Status,
            scaling_item_id="",
            description="Storage status.",
        ),
        "wh_sf": RegisterMapEntry(
            offset=7,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Scale factor for energy capacity.",
        ),
        "pct_sf": RegisterMapEntry(
            offset=8,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Scale factor for percentage.",
        ),
    }
