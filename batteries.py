from curses.ascii import SOH
from socket import SO_ERROR
import solaredge_modbus

from calculators import Average, Maximum
from enum import IntEnum, unique, auto

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
