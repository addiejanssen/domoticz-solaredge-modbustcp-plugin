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


class SunSpecDeviceModel701(SunSpecDevice):
    """Definition for SunSpec Model 701 DER AC Measurement"""

    class AcWiringType(IntEnum):
        """States used by this Device"""
    
        SINGLE_PHASE = 0
        SPLIT_PHASE = 1
        THREE_PHASE = 2
    
    class OperatingState(IntEnum):
        """States used by this Device"""
    
        OFF = 0
        ON = 1
    
    class InverterState(IntEnum):
        """States used by this Device"""
    
        OFF = 0
        SLEEPING = 1
        STARTING = 2
        RUNNING = 3
        THROTTLED = 4
        SHUTTING_DOWN = 5
        FAULT = 6
        STANDBY = 7
    
    class GridConnectionState(IntEnum):
        """States used by this Device"""
    
        DISCONNECTED = 0
        CONNECTED = 1
    
    class AlarmBitfield(IntFlag):
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
        MANUFACTURER_ALRM = 16
    
    class DerOperationalCharacteristics(IntFlag):
        """Flags used by this Device"""
    
        GRID_FOLLOWING = 0
        GRID_FORMING = 1
        PV_CLIPPED = 2
    
    class ThrottleSourceInformation(IntFlag):
        """Flags used by this Device"""
    
        MAX_W = 0
        FIXED_W = 1
        FIXED_VAR = 2
        FIXED_PF = 3
        VOLT_VAR = 4
        FREQ_WATT = 5
        DYN_REACT_CURR = 6
        LVRT = 7
        HVRT = 8
        WATT_VAR = 9
        VOLT_WATT = 10
        SCHEDULED = 11
        LFRT = 12
        HFRT = 13
        DERATED = 14
    
    device_description: ClassVar[DeviceDescription] = DeviceDescription(
        id=701,
        name="DERMeasureAC",
        label="DER AC Measurement",
        description="DER AC measurement model."
    )

    register_count: ClassVar[int] = 155
    register_map: ClassVar[RegisterMap] = {
        **SunSpecDevice.register_map,
        "actype": RegisterMapEntry(
            offset=2,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=AcWiringType,
            scaling_item_id="",
            description="AC wiring type.",
        ),
        "st": RegisterMapEntry(
            offset=3,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=OperatingState,
            scaling_item_id="",
            description="Operating state of the DER.",
        ),
        "invst": RegisterMapEntry(
            offset=4,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=InverterState,
            scaling_item_id="",
            description="Enumerated value.  Inverter state.",
        ),
        "connst": RegisterMapEntry(
            offset=5,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=GridConnectionState,
            scaling_item_id="",
            description="Grid connection state of the DER.",
        ),
        "alrm": RegisterMapEntry(
            offset=6,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=AlarmBitfield,
            scaling_item_id="",
            description="Active alarms for the DER.",
        ),
        "dermode": RegisterMapEntry(
            offset=8,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=DerOperationalCharacteristics,
            scaling_item_id="",
            description="Current operational characteristics of the DER.",
        ),
        "w": RegisterMapEntry(
            offset=10,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="w_sf",
            description="Total active power. Active power is positive for DER generation and negative for absorption.",
        ),
        "va": RegisterMapEntry(
            offset=11,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="va_sf",
            description="Total apparent power.",
        ),
        "var": RegisterMapEntry(
            offset=12,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="var_sf",
            description="Total reactive power.",
        ),
        "pf": RegisterMapEntry(
            offset=13,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="pf_sf",
            description="Power factor. The sign of power factor should be the sign of active power.",
        ),
        "a": RegisterMapEntry(
            offset=14,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="a_sf",
            description="Total AC current.",
        ),
        "llv": RegisterMapEntry(
            offset=15,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Line to line AC voltage as an average of active phases.",
        ),
        "lnv": RegisterMapEntry(
            offset=16,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Line to neutral AC voltage as an average of active phases.",
        ),
        "hz": RegisterMapEntry(
            offset=17,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="hz_sf",
            description="AC frequency.",
        ),
        "totwhinj": RegisterMapEntry(
            offset=19,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totwh_sf",
            description="Total active energy injected (Quadrants 1 & 4).",
        ),
        "totwhabs": RegisterMapEntry(
            offset=23,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totwh_sf",
            description="Total active energy absorbed (Quadrants 2 & 3).",
        ),
        "totvarhinj": RegisterMapEntry(
            offset=27,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totvarh_sf",
            description="Total reactive energy injected (Quadrants 1 & 2).",
        ),
        "totvarhabs": RegisterMapEntry(
            offset=31,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totvarh_sf",
            description="Total reactive energy absorbed (Quadrants 3 & 4).",
        ),
        "tmpamb": RegisterMapEntry(
            offset=35,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="tmp_sf",
            description="Ambient temperature.",
        ),
        "tmpcab": RegisterMapEntry(
            offset=36,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="tmp_sf",
            description="Cabinet temperature.",
        ),
        "tmpsnk": RegisterMapEntry(
            offset=37,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="tmp_sf",
            description="Heat sink temperature.",
        ),
        "tmptrns": RegisterMapEntry(
            offset=38,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="tmp_sf",
            description="Transformer temperature.",
        ),
        "tmpsw": RegisterMapEntry(
            offset=39,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="tmp_sf",
            description="IGBT/MOSFET temperature.",
        ),
        "tmpot": RegisterMapEntry(
            offset=40,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="tmp_sf",
            description="Other temperature.",
        ),
        "wl1": RegisterMapEntry(
            offset=41,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="w_sf",
            description="Active power L1.",
        ),
        "val1": RegisterMapEntry(
            offset=42,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="va_sf",
            description="Apparent power L1.",
        ),
        "varl1": RegisterMapEntry(
            offset=43,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="var_sf",
            description="Reactive power L1.",
        ),
        "pfl1": RegisterMapEntry(
            offset=44,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="pf_sf",
            description="Power factor phase L1.",
        ),
        "al1": RegisterMapEntry(
            offset=45,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="a_sf",
            description="Current phase L1.",
        ),
        "vl1l2": RegisterMapEntry(
            offset=46,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Phase voltage L1-L2.",
        ),
        "vl1": RegisterMapEntry(
            offset=47,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Phase voltage L1-N.",
        ),
        "totwhinjl1": RegisterMapEntry(
            offset=48,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totwh_sf",
            description="Total active energy injected L1.",
        ),
        "totwhabsl1": RegisterMapEntry(
            offset=52,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totwh_sf",
            description="Total active energy absorbed L1.",
        ),
        "totvarhinjl1": RegisterMapEntry(
            offset=56,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totvarh_sf",
            description="Total reactive energy injected L1.",
        ),
        "totvarhabsl1": RegisterMapEntry(
            offset=60,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totvarh_sf",
            description="Total reactive energy absorbed L1.",
        ),
        "wl2": RegisterMapEntry(
            offset=64,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="w_sf",
            description="Active power L2.",
        ),
        "val2": RegisterMapEntry(
            offset=65,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="va_sf",
            description="Apparent power L2.",
        ),
        "varl2": RegisterMapEntry(
            offset=66,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="var_sf",
            description="Reactive power L2.",
        ),
        "pfl2": RegisterMapEntry(
            offset=67,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="pf_sf",
            description="Power factor L2.",
        ),
        "al2": RegisterMapEntry(
            offset=68,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="a_sf",
            description="Current L2.",
        ),
        "vl2l3": RegisterMapEntry(
            offset=69,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Phase voltage L2-L3.",
        ),
        "vl2": RegisterMapEntry(
            offset=70,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Phase voltage L2-N.",
        ),
        "totwhinjl2": RegisterMapEntry(
            offset=71,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totwh_sf",
            description="Total active energy injected L2.",
        ),
        "totwhabsl2": RegisterMapEntry(
            offset=75,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totwh_sf",
            description="Total active energy absorbed L2.",
        ),
        "totvarhinjl2": RegisterMapEntry(
            offset=79,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totvarh_sf",
            description="Total reactive energy injected L2.",
        ),
        "totvarhabsl2": RegisterMapEntry(
            offset=83,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totvarh_sf",
            description="Total reactive energy absorbed L2.",
        ),
        "wl3": RegisterMapEntry(
            offset=87,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="w_sf",
            description="Active power L3.",
        ),
        "val3": RegisterMapEntry(
            offset=88,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="va_sf",
            description="Apparent power L3.",
        ),
        "varl3": RegisterMapEntry(
            offset=89,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="var_sf",
            description="Reactive power L3.",
        ),
        "pfl3": RegisterMapEntry(
            offset=90,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="pf_sf",
            description="Power factor L3.",
        ),
        "al3": RegisterMapEntry(
            offset=91,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="a_sf",
            description="Current L3.",
        ),
        "vl3l1": RegisterMapEntry(
            offset=92,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Phase voltage L3-L1.",
        ),
        "vl3": RegisterMapEntry(
            offset=93,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Phase voltage L3-N.",
        ),
        "totwhinjl3": RegisterMapEntry(
            offset=94,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totwh_sf",
            description="Total active energy injected L3.",
        ),
        "totwhabsl3": RegisterMapEntry(
            offset=98,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totwh_sf",
            description="Total active energy absorbed L3.",
        ),
        "totvarhinjl3": RegisterMapEntry(
            offset=102,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totvarh_sf",
            description="Total reactive energy injected L3.",
        ),
        "totvarhabsl3": RegisterMapEntry(
            offset=106,
            size=4,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="totvarh_sf",
            description="Total reactive energy absorbed L3.",
        ),
        "throtpct": RegisterMapEntry(
            offset=110,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Throttling in pct of maximum active power.",
        ),
        "throtsrc": RegisterMapEntry(
            offset=111,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=ThrottleSourceInformation,
            scaling_item_id="",
            description="Active throttling source.",
        ),
        "a_sf": RegisterMapEntry(
            offset=113,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Current scale factor.",
        ),
        "v_sf": RegisterMapEntry(
            offset=114,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Voltage scale factor.",
        ),
        "hz_sf": RegisterMapEntry(
            offset=115,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Frequency scale factor.",
        ),
        "w_sf": RegisterMapEntry(
            offset=116,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Active power scale factor.",
        ),
        "pf_sf": RegisterMapEntry(
            offset=117,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Power factor scale factor.",
        ),
        "va_sf": RegisterMapEntry(
            offset=118,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Apparent power scale factor.",
        ),
        "var_sf": RegisterMapEntry(
            offset=119,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Reactive power scale factor.",
        ),
        "totwh_sf": RegisterMapEntry(
            offset=120,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Active energy scale factor.",
        ),
        "totvarh_sf": RegisterMapEntry(
            offset=121,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Reactive energy scale factor.",
        ),
        "tmp_sf": RegisterMapEntry(
            offset=122,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Temperature scale factor.",
        ),
        "mnalrminfo": RegisterMapEntry(
            offset=123,
            size=32,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.STRING,
            python_type=str,
            scaling_item_id="",
            description="Manufacturer alarm information. Valid if MANUFACTURER_ALRM indication is active.",
        ),
    }
