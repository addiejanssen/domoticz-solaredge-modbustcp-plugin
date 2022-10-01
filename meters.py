import solaredge_modbus

from calculators import Average, Delta
from enum import IntEnum, unique

@unique
class MeterUnit(IntEnum):

    CURRENT                         = 1
    L1_CURRENT                      = 2
    L2_CURRENT                      = 3
    L3_CURRENT                      = 4
    LN_VOLTAGE                      = 5
    L1N_VOLTAGE                     = 6
    L2N_VOLTAGE                     = 7
    L3N_VOLTAGE                     = 8
    LL_VOLTAGE                      = 9
    L12_VOLTAGE                     = 10
    L23_VOLTAGE                     = 11
    L31_VOLTAGE                     = 12
    FREQUENCY                       = 13
    POWER                           = 14
    L1_POWER                        = 15
    L2_POWER                        = 16
    L3_POWER                        = 17
    POWER_APPARENT                  = 18
    L1_POWER_APPARENT               = 19
    L2_POWER_APPARENT               = 20
    L3_POWER_APPARENT               = 21
    POWER_REACTIVE                  = 22
    L1_POWER_REACTIVE               = 23
    L2_POWER_REACTIVE               = 24
    L3_POWER_REACTIVE               = 25
    POWER_FACTOR                    = 26
    L1_POWER_FACTOR                 = 27
    L2_POWER_FACTOR                 = 28
    L3_POWER_FACTOR                 = 29
    EXPORT_ENERGY_ACTIVE            = 30
    L1_EXPORT_ENERGY_ACTIVE         = 31
    L2_EXPORT_ENERGY_ACTIVE         = 32
    L3_EXPORT_ENERGY_ACTIVE         = 33
    IMPORT_ENERGY_ACTIVE            = 34
    L1_IMPORT_ENERGY_ACTIVE         = 35
    L2_IMPORT_ENERGY_ACTIVE         = 36
    L3_IMPORT_ENERGY_ACTIVE         = 37
    EXPORT_ENERGY_APPARENT          = 38
    L1_EXPORT_ENERGY_APPARENT       = 39
    L2_EXPORT_ENERGY_APPARENT       = 40
    L3_EXPORT_ENERGY_APPARENT       = 41
    IMPORT_ENERGY_APPARENT          = 42
    L1_IMPORT_ENERGY_APPARENT       = 43
    L2_IMPORT_ENERGY_APPARENT       = 44
    L3_IMPORT_ENERGY_APPARENT       = 45
    IMPORT_ENERGY_REACTIVE_Q1       = 46
    L1_IMPORT_ENERGY_REACTIVE_Q1    = 47
    L2_IMPORT_ENERGY_REACTIVE_Q1    = 48
    L3_IMPORT_ENERGY_REACTIVE_Q1    = 49
    IMPORT_ENERGY_REACTIVE_Q2       = 50
    L1_IMPORT_ENERGY_REACTIVE_Q2    = 51
    L2_IMPORT_ENERGY_REACTIVE_Q2    = 52
    L3_IMPORT_ENERGY_REACTIVE_Q2    = 53
    EXPORT_ENERGY_REACTIVE_Q3       = 54
    L1_EXPORT_ENERGY_REACTIVE_Q3    = 55
    L2_EXPORT_ENERGY_REACTIVE_Q3    = 56
    L3_EXPORT_ENERGY_REACTIVE_Q3    = 57
    EXPORT_ENERGY_REACTIVE_Q4       = 58
    L1_EXPORT_ENERGY_REACTIVE_Q4    = 59
    L2_EXPORT_ENERGY_REACTIVE_Q4    = 60
    L3_EXPORT_ENERGY_REACTIVE_Q4    = 61

WYE_THREE_PHASE_METER = [
#   ID,                                 NAME,                               TYPE,  SUBTYPE,  SWITCHTYPE, OPTIONS,                MODBUSNAME,                MODBUSSCALE,            FORMAT,    PREPEND, APPEND,             LOOKUP, MATH
    [MeterUnit.CURRENT,                 "Current",                          0xF3,  0x17,     0x00,       {},                     "current",                 "current_scale",        "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L1_CURRENT,              "L1 Current",                       0xF3,  0x17,     0x00,       {},                     "l1_current",              "current_scale",        "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L2_CURRENT,              "L2 Current",                       0xF3,  0x17,     0x00,       {},                     "l2_current",              "current_scale",        "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L3_CURRENT,              "L3 Current",                       0xF3,  0x17,     0x00,       {},                     "l3_current",              "current_scale",        "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.LN_VOLTAGE,              "LN Voltage",                       0xF3,  0x08,     0x00,       {},                     "voltage_ln",              "voltage_scale",        "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L1N_VOLTAGE,             "L1-N Voltage",                     0xF3,  0x08,     0x00,       {},                     "l1n_voltage",             "voltage_scale",        "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L2N_VOLTAGE,             "L2-N Voltage",                     0xF3,  0x08,     0x00,       {},                     "l2n_voltage",             "voltage_scale",        "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L3N_VOLTAGE,             "L3-N Voltage",                     0xF3,  0x08,     0x00,       {},                     "l3n_voltage",             "voltage_scale",        "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.LL_VOLTAGE,              "LL Voltage",                       0xF3,  0x08,     0x00,       {},                     "voltage_ll",              "voltage_scale",        "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L12_VOLTAGE,             "L1-2 Voltage",                     0xF3,  0x08,     0x00,       {},                     "l12_voltage",             "voltage_scale",        "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L23_VOLTAGE,             "L2-3 Voltage",                     0xF3,  0x08,     0x00,       {},                     "l23_voltage",             "voltage_scale",        "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L31_VOLTAGE,             "L3-1 Voltage",                     0xF3,  0x08,     0x00,       {},                     "l31_voltage",             "voltage_scale",        "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.FREQUENCY,               "Frequency",                        0xF3,  0x1F,     0x00,       { "Custom": "1;Hz"  },  "frequency",               "frequency_scale",      "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.POWER,                   "Power",                            0xF8,  0x01,     0x00,       {},                     "power",                   "power_scale",          "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L1_POWER,                "L1 Power",                         0xF8,  0x01,     0x00,       {},                     "l1_power",                "power_scale",          "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L2_POWER,                "L2 Power",                         0xF8,  0x01,     0x00,       {},                     "l2_power",                "power_scale",          "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L3_POWER,                "L3 Power",                         0xF8,  0x01,     0x00,       {},                     "l3_power",                "power_scale",          "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.POWER_APPARENT,          "Power (Apparent)",                 0xF3,  0x1F,     0x00,       { "Custom": "1;VA"  },  "power_apparent",          "power_apparent_scale", "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L1_POWER_APPARENT,       "L1 Power (Apparent)",              0xF3,  0x1F,     0x00,       { "Custom": "1;VA"  },  "l1_power_apparent",       "power_apparent_scale", "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L2_POWER_APPARENT,       "L2 Power (Apparent)",              0xF3,  0x1F,     0x00,       { "Custom": "1;VA"  },  "l2_power_apparent",       "power_apparent_scale", "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L3_POWER_APPARENT,       "L3 Power (Apparent)",              0xF3,  0x1F,     0x00,       { "Custom": "1;VA"  },  "l3_power_apparent",       "power_apparent_scale", "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.POWER_REACTIVE,          "Power (Reactive)",                 0xF3,  0x1F,     0x00,       { "Custom": "1;VAr" },  "power_reactive",          "power_reactive_scale", "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L1_POWER_REACTIVE,       "L1 Power (Reactive)",              0xF3,  0x1F,     0x00,       { "Custom": "1;VAr" },  "l1_power_reactive",       "power_reactive_scale", "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L2_POWER_REACTIVE,       "L2 Power (Reactive)",              0xF3,  0x1F,     0x00,       { "Custom": "1;VAr" },  "l2_power_reactive",       "power_reactive_scale", "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L3_POWER_REACTIVE,       "L3 Power (Reactive)",              0xF3,  0x1F,     0x00,       { "Custom": "1;VAr" },  "l3_power_reactive",       "power_reactive_scale", "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.POWER_FACTOR,            "Power Factor",                     0xF3,  0x06,     0x00,       {},                     "power_factor",            "power_factor_scale",   "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L1_POWER_FACTOR,         "L1 Power Factor",                  0xF3,  0x06,     0x00,       {},                     "l1_power_factor",         "power_factor_scale",   "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L2_POWER_FACTOR,         "L2 Power Factor",                  0xF3,  0x06,     0x00,       {},                     "l2_power_factor",         "power_factor_scale",   "{:.2f}",  None,    None,                None,   Average() ],
    [MeterUnit.L3_POWER_FACTOR,         "L3 Power Factor",                  0xF3,  0x06,     0x00,       {},                     "l3_power_factor",         "power_factor_scale",   "{:.2f}",  None,    None,                None,   Average() ],
#
# import and export values should be "Usage" or "Return" in Domoticz
# => need to look at the correct values for SWITCHTYPE
#
# also not sure if this is the right TYPE/SUBTYPE to use for these values
# is there/what is the relation with the POWER values?
# perhaps this should become a regulare counter type of meter?
#
    [MeterUnit.EXPORT_ENERGY_ACTIVE,    "Total Exported Energy (Active)",   0xF3,  0x1D,     0x04,       {},                     "export_energy_active",    "energy_active_scale",   "{};{}",  None,    Delta(),                None,   None      ],
    [MeterUnit.L1_EXPORT_ENERGY_ACTIVE, "L1 Exported Energy (Active)",      0xF3,  0x1D,     0x04,       {},                     "l1_export_energy_active", "energy_active_scale",   "0;{}",   None,    None,                None,   None      ],
    [MeterUnit.L2_EXPORT_ENERGY_ACTIVE, "L2 Exported Energy (Active)",      0xF3,  0x1D,     0x04,       {},                     "l2_export_energy_active", "energy_active_scale",   "0;{}",   None,    None,                None,   None      ],
    [MeterUnit.L3_EXPORT_ENERGY_ACTIVE, "L3 Exported Energy (Active)",      0xF3,  0x1D,     0x04,       {},                     "l3_export_energy_active", "energy_active_scale",   "0;{}",   None,    None,                None,   None      ],
    [MeterUnit.IMPORT_ENERGY_ACTIVE,    "Total Imported Energy (Active)",   0xF3,  0x1D,     0x00,       {},                     "import_energy_active",    "energy_active_scale",   "{};{}",  None,    Delta(),             None,   None      ],
    [MeterUnit.L1_IMPORT_ENERGY_ACTIVE, "L1 Imported Energy (Active)",      0xF3,  0x21,     0x00,       {},                     "l1_import_energy_active", "energy_active_scale",   "0;{}",   None,    None,                None,   None      ],
    [MeterUnit.L2_IMPORT_ENERGY_ACTIVE, "L2 Imported Energy (Active)",      0xF3,  0x21,     0x00,       {},                     "l2_import_energy_active", "energy_active_scale",   "0;{}",   None,    None,                None,   None      ],
    [MeterUnit.L3_IMPORT_ENERGY_ACTIVE, "L3 Imported Energy (Active)",      0xF3,  0x21,     0x00,       {},                     "l3_import_energy_active", "energy_active_scale",   "0;{}",   None,    None,                None,   None      ]



#    [MeterUnit.STATUS,          "Status",            0xF3,  0x13,     0x00,       {},                     "status",          None,                   "{}",      None,           solaredge_modbus.INVERTER_STATUS_MAP,  None      ],
#    [MeterUnit.VENDOR_STATUS,   "Vendor Status",     0xF3,  0x13,     0x00,       {},                     "vendor_status",   None,                   "{}",      None,           None,                                  None      ],
#    [MeterUnit.L1_VOLTAGE,      "L1 Voltage",        0xF3,  0x08,     0x00,       {},                     "l1_voltage",      "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
#    [MeterUnit.L2_VOLTAGE,      "L2 Voltage",        0xF3,  0x08,     0x00,       {},                     "l2_voltage",      "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
#    [MeterUnit.L3_VOLTAGE,      "L3 Voltage",        0xF3,  0x08,     0x00,       {},                     "l3_voltage",      "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
#    [MeterUnit.L1N_VOLTAGE,     "L1-N Voltage",      0xF3,  0x08,     0x00,       {},                     "l1n_voltage",     "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
#    [MeterUnit.L2N_VOLTAGE,     "L2-N Voltage",      0xF3,  0x08,     0x00,       {},                     "l2n_voltage",     "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
#    [MeterUnit.L3N_VOLTAGE,     "L3-N Voltage",      0xF3,  0x08,     0x00,       {},                     "l3n_voltage",     "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
#    [MeterUnit.ENERGY_TOTAL,    "Total Energy",      0xF3,  0x1D,     0x04,       {},                     "energy_total",    "energy_total_scale",   "{};{}",   MeterUnit.POWER_AC,  None,                          None      ],
#    [MeterUnit.CURRENT_DC,      "DC Current",        0xF3,  0x17,     0x00,       {},                     "current_dc",      "current_dc_scale",     "{:.2f}",  None,           None,                                  Average() ],
#    [MeterUnit.VOLTAGE_DC,      "DC Voltage",        0xF3,  0x08,     0x00,       {},                     "voltage_dc",      "voltage_dc_scale",     "{:.2f}",  None,           None,                                  Average() ],
#    [MeterUnit.POWER_DC,        "DC Power",          0xF8,  0x01,     0x00,       {},                     "power_dc",        "power_dc_scale",       "{:.2f}",  None,           None,                                  Average() ],
#    [MeterUnit.TEMPERATURE,     "Temperature",       0xF3,  0x05,     0x00,       {},                     "temperature",     "temperature_scale",    "{:.2f}",  None,           None,                                  Maximum() ]
]


#MeterUnit.EXPORT_ENERGY_APPARENT,
#MeterUnit.L1_EXPORT_ENERGY_APPARENT,
#MeterUnit.L2_EXPORT_ENERGY_APPARENT,
#MeterUnit.L3_EXPORT_ENERGY_APPARENT,
#MeterUnit.IMPORT_ENERGY_APPARENT,
#MeterUnit.L1_IMPORT_ENERGY_APPARENT,
#MeterUnit.L2_IMPORT_ENERGY_APPARENT,
#MeterUnit.L3_IMPORT_ENERGY_APPARENT,
#MeterUnit.IMPORT_ENERGY_REACTIVE_Q1,
#MeterUnit.L1_IMPORT_ENERGY_REACTIVE_Q1,
#MeterUnit.L2_IMPORT_ENERGY_REACTIVE_Q1,
#MeterUnit.L3_IMPORT_ENERGY_REACTIVE_Q1,
#MeterUnit.IMPORT_ENERGY_REACTIVE_Q2,
#MeterUnit.L1_IMPORT_ENERGY_REACTIVE_Q2,
#MeterUnit.L2_IMPORT_ENERGY_REACTIVE_Q2,
#MeterUnit.L3_IMPORT_ENERGY_REACTIVE_Q2,
#MeterUnit.EXPORT_ENERGY_REACTIVE_Q3,
#MeterUnit.L1_EXPORT_ENERGY_REACTIVE_Q3,
#MeterUnit.L2_EXPORT_ENERGY_REACTIVE_Q3,
#MeterUnit.L3_EXPORT_ENERGY_REACTIVE_Q3,
#MeterUnit.EXPORT_ENERGY_REACTIVE_Q4,
#MeterUnit.L1_EXPORT_ENERGY_REACTIVE_Q4,
#MeterUnit.L2_EXPORT_ENERGY_REACTIVE_Q4,
#MeterUnit.L3_EXPORT_ENERGY_REACTIVE_Q4,