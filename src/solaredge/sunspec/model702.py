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


class SunSpecDeviceModel702(SunSpecDevice):
    """Definition for SunSpec Model 702 DER Capacity"""

    class NormalOperatingCategory(IntEnum):
        """States used by this Device"""
    
        CAT_A = 0
        CAT_B = 1
    
    class AbnormalOperatingCategory(IntEnum):
        """States used by this Device"""
    
        CAT_1 = 0
        CAT_2 = 1
        CAT_3 = 2
    
    class SupportedControlModes(IntFlag):
        """Flags used by this Device"""
    
        MAX_W = 0
        FIXED_W = 1
        FIXED_VAR = 2
        FIXED_PF = 3
        VOLT_VAR = 4
        FREQ_WATT = 5
        DYN_REACT_CURR = 6
        LV_TRIP = 7
        HV_TRIP = 8
        WATT_VAR = 9
        VOLT_WATT = 10
        SCHEDULED = 11
        LF_TRIP = 12
        HF_TRIP = 13
    
    class IntentionalIslandCategories(IntFlag):
        """Flags used by this Device"""
    
        UNCATEGORIZED = 0
        INT_ISL_CAPABLE = 1
        BLACK_START_CAPABLE = 2
        ISOCH_CAPABLE = 3
    
    class IntentionalIslandCategories(IntFlag):
        """Flags used by this Device"""
    
        UNCATEGORIZED = 0
        INT_ISL_CAPABLE = 1
        BLACK_START_CAPABLE = 2
        ISOCH_CAPABLE = 3
    
    device_description: ClassVar[DeviceDescription] = DeviceDescription(
        id=702,
        name="DERCapacity",
        label="DER Capacity",
        description="DER capacity model."
    )

    register_count: ClassVar[int] = 52
    register_map: ClassVar[RegisterMap] = {
        **SunSpecDevice.register_map,
        "wmaxrtg": RegisterMapEntry(
            offset=2,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="w_sf",
            description="Maximum active power rating at unity power factor in watts.",
        ),
        "wovrextrtg": RegisterMapEntry(
            offset=3,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="w_sf",
            description="Active power rating at specified over-excited power factor in watts.",
        ),
        "wovrextrtgpf": RegisterMapEntry(
            offset=4,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="pf_sf",
            description="Specified over-excited power factor.",
        ),
        "wundextrtg": RegisterMapEntry(
            offset=5,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="w_sf",
            description="Active power rating at specified under-excited power factor in watts.",
        ),
        "wundextrtgpf": RegisterMapEntry(
            offset=6,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="pf_sf",
            description="Specified under-excited power factor.",
        ),
        "vamaxrtg": RegisterMapEntry(
            offset=7,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="va_sf",
            description="Maximum apparent power rating in voltamperes.",
        ),
        "varmaxinjrtg": RegisterMapEntry(
            offset=8,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="var_sf",
            description="Maximum injected reactive power rating in vars.",
        ),
        "varmaxabsrtg": RegisterMapEntry(
            offset=9,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="var_sf",
            description="Maximum absorbed reactive power rating in vars.",
        ),
        "wchartemaxrtg": RegisterMapEntry(
            offset=10,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="w_sf",
            description="Maximum active power charge rate in watts.",
        ),
        "wdischartemaxrtg": RegisterMapEntry(
            offset=11,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="w_sf",
            description="Maximum active power discharge rate in watts.",
        ),
        "vachartemaxrtg": RegisterMapEntry(
            offset=12,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="va_sf",
            description="Maximum apparent power charge rate in voltamperes.",
        ),
        "vadischartemaxrtg": RegisterMapEntry(
            offset=13,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="va_sf",
            description="Maximum apparent power discharge rate in voltamperes.",
        ),
        "vnomrtg": RegisterMapEntry(
            offset=14,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="AC voltage nominal rating.",
        ),
        "vmaxrtg": RegisterMapEntry(
            offset=15,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="AC voltage maximum rating.",
        ),
        "vminrtg": RegisterMapEntry(
            offset=16,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="AC voltage minimum rating.",
        ),
        "amaxrtg": RegisterMapEntry(
            offset=17,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="a_sf",
            description="AC current maximum rating in amps.",
        ),
        "pfovrextrtg": RegisterMapEntry(
            offset=18,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="pf_sf",
            description="Unused. Please use WOvrExtRtgPF.",
        ),
        "pfundextrtg": RegisterMapEntry(
            offset=19,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="pf_sf",
            description="Unused. Please use WUndExtRtgPF.",
        ),
        "reactsusceptrtg": RegisterMapEntry(
            offset=20,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="s_sf",
            description="Reactive susceptance that remains connected to the Area EPS in the cease to energize and trip state.",
        ),
        "noropcatrtg": RegisterMapEntry(
            offset=21,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=NormalOperatingCategory,
            scaling_item_id="",
            description="Normal operating performance category as specified in IEEE 1547-2018.",
        ),
        "abnopcatrtg": RegisterMapEntry(
            offset=22,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=AbnormalOperatingCategory,
            scaling_item_id="",
            description="Abnormal operating performance category as specified in IEEE 1547-2018.",
        ),
        "ctrlmodes": RegisterMapEntry(
            offset=23,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT32,
            python_type=SupportedControlModes,
            scaling_item_id="",
            description="Supported control mode functions.",
        ),
        "intislandcatrtg": RegisterMapEntry(
            offset=25,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=IntentionalIslandCategories,
            scaling_item_id="",
            description="Intentional island categories.",
        ),
        "wmax": RegisterMapEntry(
            offset=26,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="w_sf",
            description="Maximum active power setting used to adjust maximum active power setting.",
        ),
        "wmaxovrext": RegisterMapEntry(
            offset=27,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="w_sf",
            description="Active power setting at specified over-excited power factor in watts.",
        ),
        "wovrextpf": RegisterMapEntry(
            offset=28,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="pf_sf",
            description="Specified over-excited power factor.",
        ),
        "wmaxundext": RegisterMapEntry(
            offset=29,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="w_sf",
            description="Active power setting at specified under-excited power factor in watts.",
        ),
        "wundextpf": RegisterMapEntry(
            offset=30,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="pf_sf",
            description="Specified under-excited power factor.",
        ),
        "vamax": RegisterMapEntry(
            offset=31,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="va_sf",
            description="Maximum apparent power setting used to adjust maximum apparent power rating.",
        ),
        "varmaxinj": RegisterMapEntry(
            offset=32,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="var_sf",
            description="Maximum injected reactive power setting used to adjust maximum injected reactive power rating.",
        ),
        "varmaxabs": RegisterMapEntry(
            offset=33,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="var_sf",
            description="Maximum absorbed reactive power setting used to adjust maximum absorbed reactive power rating.",
        ),
        "wchartemax": RegisterMapEntry(
            offset=34,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="w_sf",
            description="Maximum active power charge rate setting used to adjust maximum active power charge rate rating.",
        ),
        "wdischartemax": RegisterMapEntry(
            offset=35,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="w_sf",
            description="Maximum active power discharge rate setting used to adjust maximum active power discharge rate rating.",
        ),
        "vachartemax": RegisterMapEntry(
            offset=36,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="va_sf",
            description="Maximum apparent power charge rate setting used to adjust maximum apparent power charge rate rating.",
        ),
        "vadischartemax": RegisterMapEntry(
            offset=37,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="va_sf",
            description="Maximum apparent power discharge rate setting used to adjust maximum apparent power discharge rate rating.",
        ),
        "vnom": RegisterMapEntry(
            offset=38,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="Nominal AC voltage setting.",
        ),
        "vmax": RegisterMapEntry(
            offset=39,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="AC voltage maximum setting used to adjust AC voltage maximum rating.",
        ),
        "vmin": RegisterMapEntry(
            offset=40,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="v_sf",
            description="AC voltage minimum setting used to adjust AC voltage minimum rating.",
        ),
        "amax": RegisterMapEntry(
            offset=41,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="a_sf",
            description="Maximum AC current setting used to adjust maximum AC current rating.",
        ),
        "pfovrext": RegisterMapEntry(
            offset=42,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="pf_sf",
            description="Unused. Please use WOvrExtPF.",
        ),
        "pfundext": RegisterMapEntry(
            offset=43,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="pf_sf",
            description="Unused. Please use WUndExtPF.",
        ),
        "intislandcat": RegisterMapEntry(
            offset=44,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=IntentionalIslandCategories,
            scaling_item_id="",
            description="Intentional island categories.",
        ),
        "w_sf": RegisterMapEntry(
            offset=45,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Active power scale factor.",
        ),
        "pf_sf": RegisterMapEntry(
            offset=46,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Power factor scale factor.",
        ),
        "va_sf": RegisterMapEntry(
            offset=47,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Apparent power scale factor.",
        ),
        "var_sf": RegisterMapEntry(
            offset=48,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Reactive power scale factor.",
        ),
        "v_sf": RegisterMapEntry(
            offset=49,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Voltage scale factor.",
        ),
        "a_sf": RegisterMapEntry(
            offset=50,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Current scale factor.",
        ),
        "s_sf": RegisterMapEntry(
            offset=51,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.INT16,
            python_type=int,
            scaling_item_id="",
            description="Susceptance scale factor.",
        ),
    }
