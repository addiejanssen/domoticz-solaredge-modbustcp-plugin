"""
SunSpec Device Model

Author:  Addie Janssen (https://addiejanssen.com)
License: MIT

Do not modify this file - it is generated from the SunSpec Model Definitions
as published here: https://github.com/sunspec/models - commit: 90b4a33

Any changes made to this file will be lost on the next generation of the model.
"""

from enum import IntEnum, IntFlag
from typing import ClassVar

from ..base import DeviceDescription, ModbusDataType, ModbusWordOrder, RegisterMap, RegisterMapEntry
from .base import SunSpecDevice


class SunSpecDeviceModel101(SunSpecDevice):
    """Definition for SunSpec Model 101 Inverter (Single Phase)"""

    class OperatingState(IntEnum):
        """States used by this Device"""
    
        OFF = 1
        SLEEPING = 2
        STARTING = 3
        MPPT = 4
        THROTTLED = 5
        SHUTTING_DOWN = 6
        FAULT = 7
        STANDBY = 8
    
    class Event1(IntFlag):
        """Flags used by this Device"""
    
        GROUND_FAULT = 0
        DC_OVER_VOLT = 1
        AC_DISCONNECT = 2
        DC_DISCONNECT = 3
        GRID_DISCONNECT = 4
        CABINET_OPEN = 5
        MANUAL_SHUTDOWN = 6
        OVER_TEMP = 7
        OVER_FREQUENCY = 8
        UNDER_FREQUENCY = 9
        AC_OVER_VOLT = 10
        AC_UNDER_VOLT = 11
        BLOWN_STRING_FUSE = 12
        UNDER_TEMP = 13
        MEMORY_LOSS = 14
        HW_TEST_FAILURE = 15
    
    device_description: ClassVar[DeviceDescription] = DeviceDescription(
        id=101,
        name="inverter_single_phase",
        label="Inverter (Single Phase)",
        description="Include this model for single phase inverter monitoring"
    )

    register_count: ClassVar[int] = 52
    register_map: ClassVar[RegisterMap] = {
        **SunSpecDevice.register_map,
        "a": RegisterMapEntry(
            offset=2,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="a_sf",
            description="AC Current",
        ),
        "apha": RegisterMapEntry(
            offset=3,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="a_sf",
            description="Phase A Current",
        ),
        "aphb": RegisterMapEntry(
            offset=4,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="a_sf",
            description="Phase B Current",
        ),
        "aphc": RegisterMapEntry(
            offset=5,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="a_sf",
            description="Phase C Current",
        ),
        "a_sf": RegisterMapEntry(
            offset=6,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="",
        ),
        "ppvphab": RegisterMapEntry(
            offset=7,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Phase Voltage AB",
        ),
        "ppvphbc": RegisterMapEntry(
            offset=8,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Phase Voltage BC",
        ),
        "ppvphca": RegisterMapEntry(
            offset=9,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Phase Voltage CA",
        ),
        "phvpha": RegisterMapEntry(
            offset=10,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Phase Voltage AN",
        ),
        "phvphb": RegisterMapEntry(
            offset=11,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Phase Voltage BN",
        ),
        "phvphc": RegisterMapEntry(
            offset=12,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Phase Voltage CN",
        ),
        "v_sf": RegisterMapEntry(
            offset=13,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="",
        ),
        "w": RegisterMapEntry(
            offset=14,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="w_sf",
            description="AC Power",
        ),
        "w_sf": RegisterMapEntry(
            offset=15,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="",
        ),
        "hz": RegisterMapEntry(
            offset=16,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="hz_sf",
            description="Line Frequency",
        ),
        "hz_sf": RegisterMapEntry(
            offset=17,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="",
        ),
        "va": RegisterMapEntry(
            offset=18,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="va_sf",
            description="AC Apparent Power",
        ),
        "va_sf": RegisterMapEntry(
            offset=19,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="",
        ),
        "var": RegisterMapEntry(
            offset=20,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="var_sf",
            description="AC Reactive Power",
        ),
        "var_sf": RegisterMapEntry(
            offset=21,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="",
        ),
        "pf": RegisterMapEntry(
            offset=22,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="pf_sf",
            description="AC Power Factor",
        ),
        "pf_sf": RegisterMapEntry(
            offset=23,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="",
        ),
        "wh": RegisterMapEntry(
            offset=24,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="wh_sf",
            description="AC Energy",
        ),
        "wh_sf": RegisterMapEntry(
            offset=26,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="",
        ),
        "dca": RegisterMapEntry(
            offset=27,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="dca_sf",
            description="DC Current",
        ),
        "dca_sf": RegisterMapEntry(
            offset=28,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="",
        ),
        "dcv": RegisterMapEntry(
            offset=29,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="dcv_sf",
            description="DC Voltage",
        ),
        "dcv_sf": RegisterMapEntry(
            offset=30,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="",
        ),
        "dcw": RegisterMapEntry(
            offset=31,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="dcw_sf",
            description="DC Power",
        ),
        "dcw_sf": RegisterMapEntry(
            offset=32,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="",
        ),
        "tmpcab": RegisterMapEntry(
            offset=33,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="tmp_sf",
            description="Cabinet Temperature",
        ),
        "tmpsnk": RegisterMapEntry(
            offset=34,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="tmp_sf",
            description="Heat Sink Temperature",
        ),
        "tmptrns": RegisterMapEntry(
            offset=35,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="tmp_sf",
            description="Transformer Temperature",
        ),
        "tmpot": RegisterMapEntry(
            offset=36,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="tmp_sf",
            description="Other Temperature",
        ),
        "tmp_sf": RegisterMapEntry(
            offset=37,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="",
        ),
        "st": RegisterMapEntry(
            offset=38,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=OperatingState,
            scaling_item_id="",
            description="Enumerated value.  Operating state",
        ),
        "stvnd": RegisterMapEntry(
            offset=39,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Vendor specific operating state code",
        ),
        "evt1": RegisterMapEntry(
            offset=40,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=Event1,
            scaling_item_id="",
            description="Bitmask value. Event fields",
        ),
        "evt2": RegisterMapEntry(
            offset=42,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Reserved for future use",
        ),
        "evtvnd1": RegisterMapEntry(
            offset=44,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Vendor defined events",
        ),
        "evtvnd2": RegisterMapEntry(
            offset=46,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Vendor defined events",
        ),
        "evtvnd3": RegisterMapEntry(
            offset=48,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Vendor defined events",
        ),
        "evtvnd4": RegisterMapEntry(
            offset=50,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Vendor defined events",
        ),
    }
