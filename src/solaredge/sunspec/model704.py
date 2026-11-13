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


class SunSpecDeviceModel704(SunSpecDevice):
    """Definition for SunSpec Model 704 DER AC Controls"""

    class PowerFactorEnableWInjEnable(IntEnum):
        """States used by this Device"""
    
        DISABLED = 0
        ENABLED = 1
    
    class PowerFactorReversionEnableWInj(IntEnum):
        """States used by this Device"""
    
        DISABLED = 0
        ENABLED = 1
    
    class PowerFactorEnableWAbsEnable(IntEnum):
        """States used by this Device"""
    
        DISABLED = 0
        ENABLED = 1
    
    class PowerFactorReversionEnableWAbs(IntEnum):
        """States used by this Device"""
    
        DISABLED = 0
        ENABLED = 1
    
    class LimitMaxPowerPctEnable(IntEnum):
        """States used by this Device"""
    
        DISABLED = 0
        ENABLED = 1
    
    class ReversionLimitMaxPowerPctEnable(IntEnum):
        """States used by this Device"""
    
        DISABLED = 0
        ENABLED = 1
    
    class SetActivePowerEnable(IntEnum):
        """States used by this Device"""
    
        DISABLED = 0
        ENABLED = 1
    
    class SetActivePowerMode(IntEnum):
        """States used by this Device"""
    
        W_MAX_PCT = 0
        WATTS = 1
    
    class ReversionActivePowerEnable(IntEnum):
        """States used by this Device"""
    
        DISABLED = 0
        ENABLED = 1
    
    class SetReactivePowerEnable(IntEnum):
        """States used by this Device"""
    
        DISABLED = 0
        ENABLED = 1
    
    class SetReactivePowerMode(IntEnum):
        """States used by this Device"""
    
        W_MAX_PCT = 0
        VAR_MAX_PCT = 1
        VAR_AVAIL_PCT = 2
        VA_MAX_PCT = 3
        VARS = 4
    
    class ReactivePowerPriority(IntEnum):
        """States used by this Device"""
    
        ACTIVE = 0
        REACTIVE = 1
        VENDOR = 2
    
    class ReversionReactivePowerEnable(IntEnum):
        """States used by this Device"""
    
        DISABLED = 0
        ENABLED = 1
    
    class NormalRampRateReference(IntEnum):
        """States used by this Device"""
    
        A_MAX = 0
        W_MAX = 1
    
    class AntiIslandingEnable(IntEnum):
        """States used by this Device"""
    
        DISABLED = 0
        ENABLED = 1
    
    device_description: ClassVar[DeviceDescription] = DeviceDescription(
        id=704,
        name="DERCtlAC",
        label="DER AC Controls",
        description="DER AC controls model."
    )

    register_count: ClassVar[int] = 59
    register_map: ClassVar[RegisterMap] = {
        **SunSpecDevice.register_map,
        "pfwinjena": RegisterMapEntry(
            offset=2,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=PowerFactorEnableWInjEnable,
            scaling_item_id="",
            description="Power factor enable when injecting active power.",
        ),
        "pfwinjenarvrt": RegisterMapEntry(
            offset=3,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=PowerFactorReversionEnableWInj,
            scaling_item_id="",
            description="Power factor reversion timer when injecting active power enable.",
        ),
        "pfwinjrvrttms": RegisterMapEntry(
            offset=4,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Power factor reversion timer when injecting active power.",
        ),
        "pfwinjrvrtrem": RegisterMapEntry(
            offset=6,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Power factor reversion time remaining when injecting active power.",
        ),
        "pfwabsena": RegisterMapEntry(
            offset=8,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=PowerFactorEnableWAbsEnable,
            scaling_item_id="",
            description="Power factor enable when absorbing active power.",
        ),
        "pfwabsenarvrt": RegisterMapEntry(
            offset=9,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=PowerFactorReversionEnableWAbs,
            scaling_item_id="",
            description="Power factor reversion timer when absorbing active power enable.",
        ),
        "pfwabsrvrttms": RegisterMapEntry(
            offset=10,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Power factor reversion timer when absorbing active power.",
        ),
        "pfwabsrvrtrem": RegisterMapEntry(
            offset=12,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Power factor reversion time remaining when absorbing active power.",
        ),
        "wmaxlimpctena": RegisterMapEntry(
            offset=14,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=LimitMaxPowerPctEnable,
            scaling_item_id="",
            description="Limit maximum active power percent enable.",
        ),
        "wmaxlimpct": RegisterMapEntry(
            offset=15,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="wmaxlimpct_sf",
            description="Limit maximum active power percent value.",
        ),
        "wmaxlimpctrvrt": RegisterMapEntry(
            offset=16,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="wmaxlimpct_sf",
            description="Reversion limit maximum active power percent value.",
        ),
        "wmaxlimpctenarvrt": RegisterMapEntry(
            offset=17,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=ReversionLimitMaxPowerPctEnable,
            scaling_item_id="",
            description="Reversion limit maximum active power percent value enable.",
        ),
        "wmaxlimpctrvrttms": RegisterMapEntry(
            offset=18,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Limit maximum active power percent reversion time.",
        ),
        "wmaxlimpctrvrtrem": RegisterMapEntry(
            offset=20,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Limit maximum active power percent reversion time remaining.",
        ),
        "wsetena": RegisterMapEntry(
            offset=22,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=SetActivePowerEnable,
            scaling_item_id="",
            description="Set active power enable.",
        ),
        "wsetmod": RegisterMapEntry(
            offset=23,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=SetActivePowerMode,
            scaling_item_id="",
            description="Set active power mode.",
        ),
        "wset": RegisterMapEntry(
            offset=24,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT32,
            python_type=int,
            scaling_item_id="wset_sf",
            description="Active power setting value in watts.",
        ),
        "wsetrvrt": RegisterMapEntry(
            offset=26,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT32,
            python_type=int,
            scaling_item_id="wset_sf",
            description="Reversion active power setting value in watts.",
        ),
        "wsetpct": RegisterMapEntry(
            offset=28,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="wsetpct_sf",
            description="Active power setting value as percent.",
        ),
        "wsetpctrvrt": RegisterMapEntry(
            offset=29,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="wsetpct_sf",
            description="Reversion active power setting value as percent.",
        ),
        "wsetenarvrt": RegisterMapEntry(
            offset=30,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=ReversionActivePowerEnable,
            scaling_item_id="",
            description="Reversion active power function enable.",
        ),
        "wsetrvrttms": RegisterMapEntry(
            offset=31,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Set active power reversion time.",
        ),
        "wsetrvrtrem": RegisterMapEntry(
            offset=33,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Set active power reversion time remaining.",
        ),
        "varsetena": RegisterMapEntry(
            offset=35,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=SetReactivePowerEnable,
            scaling_item_id="",
            description="Set reactive power enable.",
        ),
        "varsetmod": RegisterMapEntry(
            offset=36,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=SetReactivePowerMode,
            scaling_item_id="",
            description="Set reactive power mode.",
        ),
        "varsetpri": RegisterMapEntry(
            offset=37,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=ReactivePowerPriority,
            scaling_item_id="",
            description="Reactive power priority.",
        ),
        "varset": RegisterMapEntry(
            offset=38,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT32,
            python_type=int,
            scaling_item_id="varset_sf",
            description="Reactive power setting value in vars.",
        ),
        "varsetrvrt": RegisterMapEntry(
            offset=40,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT32,
            python_type=int,
            scaling_item_id="varset_sf",
            description="Reversion reactive power setting value in vars.",
        ),
        "varsetpct": RegisterMapEntry(
            offset=42,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="varsetpct_sf",
            description="Reactive power setting value as percent.",
        ),
        "varsetpctrvrt": RegisterMapEntry(
            offset=43,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="varsetpct_sf",
            description="Reversion reactive power setting value as percent.",
        ),
        "varsetenarvrt": RegisterMapEntry(
            offset=44,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=ReversionReactivePowerEnable,
            scaling_item_id="",
            description="Reversion reactive power function enable.",
        ),
        "varsetrvrttms": RegisterMapEntry(
            offset=45,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Set reactive power reversion time.",
        ),
        "varsetrvrtrem": RegisterMapEntry(
            offset=47,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=int,
            scaling_item_id="",
            description="Set reactive power reversion time remaining.",
        ),
        "wrmp": RegisterMapEntry(
            offset=49,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Ramp rate for increases in active power during normal generation.",
        ),
        "wrmpref": RegisterMapEntry(
            offset=50,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=NormalRampRateReference,
            scaling_item_id="",
            description="Ramp rate reference unit for increases in active power or current during normal generation.",
        ),
        "varrmp": RegisterMapEntry(
            offset=51,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Ramp rate based on max reactive power per second.",
        ),
        "antiislena": RegisterMapEntry(
            offset=52,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=AntiIslandingEnable,
            scaling_item_id="",
            description="Anti-islanding enable.",
        ),
        "pf_sf": RegisterMapEntry(
            offset=53,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Power factor scale factor.",
        ),
        "wmaxlimpct_sf": RegisterMapEntry(
            offset=54,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Limit maximum power scale factor.",
        ),
        "wset_sf": RegisterMapEntry(
            offset=55,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Active power scale factor.",
        ),
        "wsetpct_sf": RegisterMapEntry(
            offset=56,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Active power pct scale factor.",
        ),
        "varset_sf": RegisterMapEntry(
            offset=57,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Reactive power scale factor.",
        ),
        "varsetpct_sf": RegisterMapEntry(
            offset=58,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Reactive power pct scale factor.",
        ),
    }
