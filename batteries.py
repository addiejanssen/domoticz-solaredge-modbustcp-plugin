import solaredge_modbus

from helpers import Timestamp
from enum import IntEnum, unique

@unique
class BatteryUnit(IntEnum):

    STATUS                      = 1
    STATUS_INTERNAL             = 2
    EVENT_LOG                   = 3
    EVENT_LOG_INTERNAL          = 4
    RATED_ENERGY                = 5
    MAX_CHARGE_CONT_POWER       = 6
    MAX_DISCHARGE_CONT_POWER    = 7
    MAX_CHARGE_PEAK_POWER       = 8
    MAX_DISCHARGE_PEAK_POWER    = 9
    AVERAGE_TEMP                = 10
    MAX_TEMP                    = 11
    INSTANT_VOLTAGE             = 12
    INSTANT_CURRENT             = 13
    INSTANT_POWER               = 14
    LIFE_EXPORT_ENERGY_COUNT    = 15
    LIFE_IMPORT_ENERGY_COUNT    = 16
    MAX_ENERGY                  = 17
    AVAILABLE_ENERGY            = 18
    SOH                         = 19
    SOE                         = 20

#
# This lists all implemented options, but a battery may not return all of them.
# We may want to define specific battery types in the future.
# However, we have no further information for those types of batteries yet.
# Let's wait till somebody can help out sharing the actual values returned.
#

OTHER_BATTERY = [
#   ID,                                    NAME,                                 TYPE, SUBTYPE, SWITCHTYPE, OPTIONS, MODBUSNAME,                           MODBUSSCALE, FORMAT,    PREPEND_ROW, PREPEND_MATH, APPEND_MATH, LOOKUP,                              MATH
    [BatteryUnit.STATUS,                   "Status",                             0xF3, 0x13,    0x00,       {},      "status",                             None,        "{}",      None,        None,         None,        solaredge_modbus.BATTERY_STATUS_MAP, None      ],
    [BatteryUnit.STATUS_INTERNAL,          "Internal Status",                    0xF3, 0x13,    0x00,       {},      "status_internal",                    None,        "{}",      None,        None,         None,        solaredge_modbus.BATTERY_STATUS_MAP, None      ],
    [BatteryUnit.EVENT_LOG,                "Event Log",                          0xF3, 0x13,    0x00,       {},      "event_log",                          None,        "{}",      None,        None,         None,        None,                                None      ],
    [BatteryUnit.EVENT_LOG_INTERNAL,       "Internal Event Log",                 0xF3, 0x13,    0x00,       {},      "event_log_internal",                 None,        "{}",      None,        None,         None,        None,                                None      ],
    [BatteryUnit.RATED_ENERGY,             "Rated Energy",                       0xF3, 0x21,    0x00,       {},      "rated_energy",                       None,        "-1;{}",   None,        None,         None,        None,                                None      ],
    [BatteryUnit.MAX_CHARGE_CONT_POWER,    "Maximum Charge Continuous Power",    0xF8, 0x01,    0x00,       {},      "maximum_charge_continuous_power",    None,        "{}",      None,        None,         None,        None,                                None      ],
    [BatteryUnit.MAX_DISCHARGE_CONT_POWER, "Maximum Discharge Continuous Power", 0xF8, 0x01,    0x00,       {},      "maximum_discharge_continuous_power", None,        "{}",      None,        None,         None,        None,                                None      ],
    [BatteryUnit.MAX_CHARGE_PEAK_POWER,    "Maximum Charge Peak Power",          0xF8, 0x01,    0x00,       {},      "maximum_charge_peak_power",          None,        "{}",      None,        None,         None,        None,                                None      ],
    [BatteryUnit.MAX_DISCHARGE_PEAK_POWER, "Maximum Discharge Peak Power",       0xF8, 0x01,    0x00,       {},      "maximum_discharge_peak_power",       None,        "{}",      None,        None,         None,        None,                                None      ],
    [BatteryUnit.AVERAGE_TEMP,             "Average Temperature",                0xF3, 0x05,    0x00,       {},      "average_temperature",                None,        "{:.2f}",  None,        None,         None,        None,                                None      ],
    [BatteryUnit.MAX_TEMP,                 "Maximum Temperature",                0xF3, 0x05,    0x00,       {},      "maximum_temperature",                None,        "{:.2f}",  None,        None,         None,        None,                                None      ],
    [BatteryUnit.INSTANT_VOLTAGE,          "Instantaneous Voltage",              0xF3, 0x08,    0x00,       {},      "instantaneous_voltage",              None,        "{:.2f}",  None,        None,         None,        None,                                None      ],
    [BatteryUnit.INSTANT_CURRENT,          "Instantaneous Current",              0xF3, 0x17,    0x00,       {},      "instantaneous_current",              None,        "{:.2f}",  None,        None,         None,        None,                                None      ],
    [BatteryUnit.INSTANT_POWER,            "Instantaneous Power",                0xF8, 0x01,    0x00,       {},      "instantaneous_power",                None,        "{}",      None,        None,         None,        None,                                None      ],
    [BatteryUnit.LIFE_EXPORT_ENERGY_COUNT, "Total Exported Energy",              0xF3, 0x1D,    0x00,       {},      "lifetime_export_energy_counter",     None,        "{};{}",   13,          None,         None,        None,                                None      ],
    [BatteryUnit.LIFE_IMPORT_ENERGY_COUNT, "Total Imported Energy",              0xF3, 0x1D,    0x00,       {},      "lifetime_import_energy_counter",     None,        "{};{}",   13,          None,         None,        None,                                None      ],
    [BatteryUnit.MAX_ENERGY,               "Maximum Energy",                     0xF3, 0x21,    0x00,       {},      "maximum_energy",                     None,        "-1;{}",   None,        None,         None,        None,                                None      ],
    [BatteryUnit.AVAILABLE_ENERGY,         "Available Energy",                   0xF3, 0x21,    0x00,       {},      "available_energy",                   None,        "-1;{}",   None,        None,         None,        None,                                None      ],
    [BatteryUnit.SOH,                      "State of Health",                    0xF3, 0x06,    0x00,       {},      "soh",                                None,        "{}",      None,        None,         None,        None,                                None      ],
    [BatteryUnit.SOE,                      "State of Energy",                    0xF3, 0x06,    0x00,       {},      "soe",                                None,        "{}",      None,        None,         None,        None,                                None      ]
]