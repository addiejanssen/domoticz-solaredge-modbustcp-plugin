import solaredge_modbus

from calculators import Average, Maximum
from enum import IntEnum, unique, auto

@unique
class InverterUnit(IntEnum):

    STATUS          = 1
    VENDOR_STATUS   = 2
    CURRENT         = 3
    L1_CURRENT      = 4
    L2_CURRENT      = 5
    L3_CURRENT      = 6
    L1_VOLTAGE      = 7
    L2_VOLTAGE      = 8
    L3_VOLTAGE      = 9
    L1N_VOLTAGE     = 10
    L2N_VOLTAGE     = 11
    L3N_VOLTAGE     = 12
    POWER_AC        = 13
    FREQUENCY       = 14
    POWER_APPARENT  = 15
    POWER_REACTIVE  = 16
    POWER_FACTOR    = 17
    ENERGY_TOTAL    = 18
    CURRENT_DC      = 19
    VOLTAGE_DC      = 20
    POWER_DC        = 21
    TEMPERATURE     = 22

#
# This table represents a single phase inverter.
#

SINGLE_PHASE_INVERTER = [
#   ID,                            NAME,                TYPE,  SUBTYPE,  SWITCHTYPE, OPTIONS,                MODBUSNAME,        MODBUSSCALE,            FORMAT,    PREPEND,        LOOKUP,                                MATH
    [InverterUnit.STATUS,          "Status",            0xF3,  0x13,     0x00,       {},                     "status",          None,                   "{}",      None,           solaredge_modbus.INVERTER_STATUS_MAP,  None      ],
    [InverterUnit.VENDOR_STATUS,   "Vendor Status",     0xF3,  0x13,     0x00,       {},                     "vendor_status",   None,                   "{}",      None,           None,                                  None      ],
    [InverterUnit.CURRENT,         "Current",           0xF3,  0x17,     0x00,       {},                     "current",         "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.L1_CURRENT,      "L1 Current",        0xF3,  0x17,     0x00,       {},                     "l1_current",      "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.L1_VOLTAGE,      "L1 Voltage",        0xF3,  0x08,     0x00,       {},                     "l1_voltage",      "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.L1N_VOLTAGE,     "L1-N Voltage",      0xF3,  0x08,     0x00,       {},                     "l1n_voltage",     "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.POWER_AC,        "Power",             0xF8,  0x01,     0x00,       {},                     "power_ac",        "power_ac_scale",       "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.FREQUENCY,       "Frequency",         0xF3,  0x1F,     0x00,       { "Custom": "1;Hz"  },  "frequency",       "frequency_scale",      "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.POWER_APPARENT,  "Power (Apparent)",  0xF3,  0x1F,     0x00,       { "Custom": "1;VA"  },  "power_apparent",  "power_apparent_scale", "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.POWER_REACTIVE,  "Power (Reactive)",  0xF3,  0x1F,     0x00,       { "Custom": "1;VAr" },  "power_reactive",  "power_reactive_scale", "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.POWER_FACTOR,    "Power Factor",      0xF3,  0x06,     0x00,       {},                     "power_factor",    "power_factor_scale",   "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.ENERGY_TOTAL,    "Total Energy",      0xF3,  0x1D,     0x04,       {},                     "energy_total",    "energy_total_scale",   "{};{}",   InverterUnit.POWER_AC,  None,                          None      ],
    [InverterUnit.CURRENT_DC,      "DC Current",        0xF3,  0x17,     0x00,       {},                     "current_dc",      "current_dc_scale",     "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.VOLTAGE_DC,      "DC Voltage",        0xF3,  0x08,     0x00,       {},                     "voltage_dc",      "voltage_dc_scale",     "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.POWER_DC,        "DC Power",          0xF8,  0x01,     0x00,       {},                     "power_dc",        "power_dc_scale",       "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.TEMPERATURE,     "Temperature",       0xF3,  0x05,     0x00,       {},                     "temperature",     "temperature_scale",    "{:.2f}",  None,           None,                                  Maximum() ]
]

#
# This table represents a three phase inverter.
#

THREE_PHASE_INVERTER = [
#   ID,                            NAME,                TYPE,  SUBTYPE,  SWITCHTYPE, OPTIONS,                MODBUSNAME,        MODBUSSCALE,            FORMAT,    PREPEND,        LOOKUP,                                MATH
    [InverterUnit.STATUS,          "Status",            0xF3,  0x13,     0x00,       {},                     "status",          None,                   "{}",      None,           solaredge_modbus.INVERTER_STATUS_MAP,  None      ],
    [InverterUnit.VENDOR_STATUS,   "Vendor Status",     0xF3,  0x13,     0x00,       {},                     "vendor_status",   None,                   "{}",      None,           None,                                  None      ],
    [InverterUnit.CURRENT,         "Current",           0xF3,  0x17,     0x00,       {},                     "current",         "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.L1_CURRENT,      "L1 Current",        0xF3,  0x17,     0x00,       {},                     "l1_current",      "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.L2_CURRENT,      "L2 Current",        0xF3,  0x17,     0x00,       {},                     "l2_current",      "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.L3_CURRENT,      "L3 Current",        0xF3,  0x17,     0x00,       {},                     "l3_current",      "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.L1_VOLTAGE,      "L1 Voltage",        0xF3,  0x08,     0x00,       {},                     "l1_voltage",      "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.L2_VOLTAGE,      "L2 Voltage",        0xF3,  0x08,     0x00,       {},                     "l2_voltage",      "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.L3_VOLTAGE,      "L3 Voltage",        0xF3,  0x08,     0x00,       {},                     "l3_voltage",      "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.L1N_VOLTAGE,     "L1-N Voltage",      0xF3,  0x08,     0x00,       {},                     "l1n_voltage",     "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.L2N_VOLTAGE,     "L2-N Voltage",      0xF3,  0x08,     0x00,       {},                     "l2n_voltage",     "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.L3N_VOLTAGE,     "L3-N Voltage",      0xF3,  0x08,     0x00,       {},                     "l3n_voltage",     "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.POWER_AC,        "Power",             0xF8,  0x01,     0x00,       {},                     "power_ac",        "power_ac_scale",       "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.FREQUENCY,       "Frequency",         0xF3,  0x1F,     0x00,       { "Custom": "1;Hz"  },  "frequency",       "frequency_scale",      "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.POWER_APPARENT,  "Power (Apparent)",  0xF3,  0x1F,     0x00,       { "Custom": "1;VA"  },  "power_apparent",  "power_apparent_scale", "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.POWER_REACTIVE,  "Power (Reactive)",  0xF3,  0x1F,     0x00,       { "Custom": "1;VAr" },  "power_reactive",  "power_reactive_scale", "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.POWER_FACTOR,    "Power Factor",      0xF3,  0x06,     0x00,       {},                     "power_factor",    "power_factor_scale",   "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.ENERGY_TOTAL,    "Total Energy",      0xF3,  0x1D,     0x04,       {},                     "energy_total",    "energy_total_scale",   "{};{}",   InverterUnit.POWER_AC,  None,                          None      ],
    [InverterUnit.CURRENT_DC,      "DC Current",        0xF3,  0x17,     0x00,       {},                     "current_dc",      "current_dc_scale",     "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.VOLTAGE_DC,      "DC Voltage",        0xF3,  0x08,     0x00,       {},                     "voltage_dc",      "voltage_dc_scale",     "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.POWER_DC,        "DC Power",          0xF8,  0x01,     0x00,       {},                     "power_dc",        "power_dc_scale",       "{:.2f}",  None,           None,                                  Average() ],
    [InverterUnit.TEMPERATURE,     "Temperature",       0xF3,  0x05,     0x00,       {},                     "temperature",     "temperature_scale",    "{:.2f}",  None,           None,                                  Maximum() ]
]