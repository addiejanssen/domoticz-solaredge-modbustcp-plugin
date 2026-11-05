from dataclasses import dataclass
from enum import IntEnum, StrEnum, unique
from typing import TypeAlias

import domo
import solaredge
import solaredge.sunspec
import solaredge.vendor


class UnitEnum(IntEnum):
    """Group individual IntEnum under this class so we can use this as a single type"""

    pass

DeviceMapping: TypeAlias = dict[UnitEnum, tuple[str, type, list[str]]]

@unique
class DeviceTypeMapping(StrEnum):
    """Lists the types of devices supported by SolarEdge"""

    INVERTER = "Inverter"
    METER    = "Meter"
    BATTERY  = "Battery"


@dataclass
class MapDetails:
    """Result of matching a SolarEdge Device with the Domoticz maps here"""

    start_offset: int
    max_offset: int
    max_devices: int
    device_type: DeviceTypeMapping
    mapping: DeviceMapping


@unique
class InverterUnit(UnitEnum):
    """Lists the individual measurements supported by Inverters"""

    STATUS              = 1
    VENDOR_STATUS       = 2
    CURRENT             = 3
    L1_CURRENT          = 4
    L2_CURRENT          = 5
    L3_CURRENT          = 6
    L1_VOLTAGE          = 7
    L2_VOLTAGE          = 8
    L3_VOLTAGE          = 9
    L1N_VOLTAGE         = 10
    L2N_VOLTAGE         = 11
    L3N_VOLTAGE         = 12
    POWER_AC            = 13
    FREQUENCY           = 14
    POWER_APPARENT      = 15
    POWER_REACTIVE      = 16
    POWER_FACTOR        = 17
    ENERGY_TOTAL        = 18
    CURRENT_DC          = 19
    VOLTAGE_DC          = 20
    POWER_DC            = 21
    TEMPERATURE         = 22
# Removed for now - we will bring these back once we start to look into power control
    RRCR_STATE          = 23
    ACTIVE_POWER_LIMIT  = 24
    COSPHI              = 25

InverterStartOffset:int = 0
InverterMaxOffset:int = max(InverterUnit)
InverterMaxDevices:int = 1

SinglePhaseInverterDeviceMap: DeviceMapping = {
    InverterUnit.STATUS:         ("Status",           domo.TextStatusDevice,    ["st"]     ),
    InverterUnit.VENDOR_STATUS:  ("Vendor Status",    domo.TextStatusDevice,    ["stvnd"]  ),
    InverterUnit.CURRENT:        ("Current",          domo.CurrentDevice,       ["a"]      ),
    InverterUnit.L1_CURRENT:     ("L1 Current",       domo.CurrentDevice,       ["apha"]   ),
    InverterUnit.L1_VOLTAGE:     ("L1 Voltage",       domo.VoltageDevice,       ["ppvphab"]),
    InverterUnit.L1N_VOLTAGE:    ("L1-N Voltage",     domo.VoltageDevice,       ["phvpha"] ),
    InverterUnit.POWER_AC:       ("Power",            domo.PowerDevice,         ["w"]      ),
    InverterUnit.FREQUENCY:      ("Frequency",        domo.FrequencyDevice,     ["hz"]     ),
    InverterUnit.POWER_APPARENT: ("Power (Apparent)", domo.ApparentPowerDevice, ["va"]     ),
    InverterUnit.POWER_REACTIVE: ("Power (Reactive)", domo.ReactivePowerDevice, ["var"]    ),
    InverterUnit.POWER_FACTOR:   ("Power Factor",     domo.PercentageDevice,    ["pf"]     ),
    InverterUnit.ENERGY_TOTAL:   ("Total Energy",     domo.EnergyDevice,        ["w","wh"] ),
    InverterUnit.CURRENT_DC:     ("DC Current",       domo.CurrentDevice,       ["dca"]    ),
    InverterUnit.VOLTAGE_DC:     ("DC Voltage",       domo.VoltageDevice,       ["dcv"]    ),
    InverterUnit.POWER_DC:       ("DC Power",         domo.PowerDevice,         ["dcw"]    ),
    InverterUnit.TEMPERATURE:    ("Temperature",      domo.TemperatureDevice,   ["tmpsnk"] ),
}

# This mapping needs verification - it's a best guess for now
TwoPhaseInverterDeviceMap: DeviceMapping = {
    InverterUnit.STATUS:         ("Status",           domo.TextStatusDevice,    ["st"]     ),
    InverterUnit.VENDOR_STATUS:  ("Vendor Status",    domo.TextStatusDevice,    ["stvnd"]  ),
    InverterUnit.CURRENT:        ("Current",          domo.CurrentDevice,       ["a"]      ),
    InverterUnit.L1_CURRENT:     ("L1 Current",       domo.CurrentDevice,       ["apha"]   ),
    InverterUnit.L2_CURRENT:     ("L2 Current",       domo.CurrentDevice,       ["aphb"]   ),
    InverterUnit.L1_VOLTAGE:     ("L1 Voltage",       domo.VoltageDevice,       ["ppvphab"]),
    InverterUnit.L2_VOLTAGE:     ("L2 Voltage",       domo.VoltageDevice,       ["ppvphbc"]),
    InverterUnit.L1N_VOLTAGE:    ("L1-N Voltage",     domo.VoltageDevice,       ["phvpha"] ),
    InverterUnit.L2N_VOLTAGE:    ("L2-N Voltage",     domo.VoltageDevice,       ["phvphb"] ),
    InverterUnit.POWER_AC:       ("Power",            domo.PowerDevice,         ["w"]      ),
    InverterUnit.FREQUENCY:      ("Frequency",        domo.FrequencyDevice,     ["hz"]     ),
    InverterUnit.POWER_APPARENT: ("Power (Apparent)", domo.ApparentPowerDevice, ["va"]     ),
    InverterUnit.POWER_REACTIVE: ("Power (Reactive)", domo.ReactivePowerDevice, ["var"]    ),
    InverterUnit.POWER_FACTOR:   ("Power Factor",     domo.PercentageDevice,    ["pf"]     ),
    InverterUnit.ENERGY_TOTAL:   ("Total Energy",     domo.EnergyDevice,        ["w","wh"] ),
    InverterUnit.CURRENT_DC:     ("DC Current",       domo.CurrentDevice,       ["dca"]    ),
    InverterUnit.VOLTAGE_DC:     ("DC Voltage",       domo.VoltageDevice,       ["dcv"]    ),
    InverterUnit.POWER_DC:       ("DC Power",         domo.PowerDevice,         ["dcw"]    ),
    InverterUnit.TEMPERATURE:    ("Temperature",      domo.TemperatureDevice,   ["tmpsnk"] ),
}

ThreePhaseInverterDeviceMap: DeviceMapping = {
    InverterUnit.STATUS:         ("Status",           domo.TextStatusDevice,    ["st"]     ),
    InverterUnit.VENDOR_STATUS:  ("Vendor Status",    domo.TextStatusDevice,    ["stvnd"]  ),
    InverterUnit.CURRENT:        ("Current",          domo.CurrentDevice,       ["a"]      ),
    InverterUnit.L1_CURRENT:     ("L1 Current",       domo.CurrentDevice,       ["apha"]   ),
    InverterUnit.L2_CURRENT:     ("L2 Current",       domo.CurrentDevice,       ["aphb"]   ),
    InverterUnit.L3_CURRENT:     ("L3 Current",       domo.CurrentDevice,       ["aphc"]   ),
    InverterUnit.L1_VOLTAGE:     ("L1 Voltage",       domo.VoltageDevice,       ["ppvphab"]),
    InverterUnit.L2_VOLTAGE:     ("L2 Voltage",       domo.VoltageDevice,       ["ppvphbc"]),
    InverterUnit.L3_VOLTAGE:     ("L3 Voltage",       domo.VoltageDevice,       ["ppvphca"]),
    InverterUnit.L1N_VOLTAGE:    ("L1-N Voltage",     domo.VoltageDevice,       ["phvpha"] ),
    InverterUnit.L2N_VOLTAGE:    ("L2-N Voltage",     domo.VoltageDevice,       ["phvphb"] ),
    InverterUnit.L3N_VOLTAGE:    ("L3-N Voltage",     domo.VoltageDevice,       ["phvphc"] ),
    InverterUnit.POWER_AC:       ("Power",            domo.PowerDevice,         ["w"]      ),
    InverterUnit.FREQUENCY:      ("Frequency",        domo.FrequencyDevice,     ["hz"]     ),
    InverterUnit.POWER_APPARENT: ("Power (Apparent)", domo.ApparentPowerDevice, ["va"]     ),
    InverterUnit.POWER_REACTIVE: ("Power (Reactive)", domo.ReactivePowerDevice, ["var"]    ),
    InverterUnit.POWER_FACTOR:   ("Power Factor",     domo.PercentageDevice,    ["pf"]     ),
    InverterUnit.ENERGY_TOTAL:   ("Total Energy",     domo.EnergyDevice,        ["w","wh"] ),
    InverterUnit.CURRENT_DC:     ("DC Current",       domo.CurrentDevice,       ["dca"]    ),
    InverterUnit.VOLTAGE_DC:     ("DC Voltage",       domo.VoltageDevice,       ["dcv"]    ),
    InverterUnit.POWER_DC:       ("DC Power",         domo.PowerDevice,         ["dcw"]    ),
    InverterUnit.TEMPERATURE:    ("Temperature",      domo.TemperatureDevice,   ["tmpsnk"] ),
}

@unique
class MeterUnit(UnitEnum):
    """Lists the individual measurements supported by Meters"""

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
#
# The values below have been defined but not implemented.
# For now, we will leave room in the device ids just in
# case we ever have a reason to implement them.
#
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


MeterStartOffset:int = InverterMaxDevices*InverterMaxOffset
MeterMaxOffset:int = max(MeterUnit)
MeterMaxDevices:int = 3

SinglePhaseMeterDeviceMap: DeviceMapping = {
    MeterUnit.CURRENT:                 ("Current",                        domo.CurrentDevice,       ["a"]              ),
    MeterUnit.L1_CURRENT:              ("L1 Current",                     domo.CurrentDevice,       ["apha"]           ),
    MeterUnit.LN_VOLTAGE:              ("LN Voltage",                     domo.VoltageDevice,       ["phv"]            ),
    MeterUnit.L1N_VOLTAGE:             ("L1-N Voltage",                   domo.VoltageDevice,       ["phvpha"]         ),
    MeterUnit.LL_VOLTAGE:              ("LL Voltage",                     domo.VoltageDevice,       ["ppv"]            ),
    MeterUnit.L12_VOLTAGE:             ("L1-2 Voltage",                   domo.VoltageDevice,       ["phvphab"]        ),
    MeterUnit.FREQUENCY:               ("Frequency",                      domo.FrequencyDevice,     ["hz"]             ),
    MeterUnit.POWER:                   ("Power",                          domo.PowerDevice,         ["w"]              ),
    MeterUnit.L1_POWER:                ("L1 Power",                       domo.PowerDevice,         ["wpha"]           ),
    MeterUnit.POWER_APPARENT:          ("Power (Apparent)",               domo.ApparentPowerDevice, ["va"]             ),
    MeterUnit.L1_POWER_APPARENT:       ("L1 Power (Apparent)",            domo.ApparentPowerDevice, ["vapha"]          ),
    MeterUnit.POWER_REACTIVE:          ("Power (Reactive)",               domo.ReactivePowerDevice, ["var"]            ),
    MeterUnit.L1_POWER_REACTIVE:       ("L1 Power (Reactive)",            domo.ReactivePowerDevice, ["varpha"]         ),
    MeterUnit.POWER_FACTOR:            ("Power Factor",                   domo.PercentageDevice,    ["pf"]             ),
    MeterUnit.L1_POWER_FACTOR:         ("L1 Power Factor",                domo.PercentageDevice,    ["pfpha"]          ),
    MeterUnit.EXPORT_ENERGY_ACTIVE:    ("Total Exported Energy (Active)", domo.EnergyExportDevice,  ["w","totwhexp"]   ),
    MeterUnit.L1_EXPORT_ENERGY_ACTIVE: ("L1 Exported Energy (Active)",    domo.EnergyExportDevice,  ["w","totwhexppha"]),
    MeterUnit.IMPORT_ENERGY_ACTIVE:    ("Total Imported Energy (Active)", domo.EnergyImportDevice,  ["w","totwhimp"]   ),
    MeterUnit.L1_IMPORT_ENERGY_ACTIVE: ("L1 Imported Energy (Active)",    domo.EnergyImportDevice,  ["w","totwhimppha"]),
}

# This mapping needs verification - it's a best guess for now
# A split single-phase (ABN) meter is to measure two independent phases
# which carry alternating current 180 degrees out of phase.
SplitPhaseMeterDeviceMap: DeviceMapping = {
    MeterUnit.CURRENT:                 ("Current",                        domo.CurrentDevice,       ["a"]              ),
    MeterUnit.L1_CURRENT:              ("L1 Current",                     domo.CurrentDevice,       ["apha"]           ),
    MeterUnit.L2_CURRENT:              ("L2 Current",                     domo.CurrentDevice,       ["aphb"]           ),
    MeterUnit.LN_VOLTAGE:              ("LN Voltage",                     domo.VoltageDevice,       ["phv"]            ),
    MeterUnit.L1N_VOLTAGE:             ("L1-N Voltage",                   domo.VoltageDevice,       ["phvpha"]         ),
    MeterUnit.L2N_VOLTAGE:             ("L2-N Voltage",                   domo.VoltageDevice,       ["phvphb"]         ),
    MeterUnit.LL_VOLTAGE:              ("LL Voltage",                     domo.VoltageDevice,       ["ppv"]            ),
    MeterUnit.L12_VOLTAGE:             ("L1-2 Voltage",                   domo.VoltageDevice,       ["phvphab"]        ),
    MeterUnit.L23_VOLTAGE:             ("L2-3 Voltage",                   domo.VoltageDevice,       ["phvphbc"]        ),
    MeterUnit.FREQUENCY:               ("Frequency",                      domo.FrequencyDevice,     ["hz"]             ),
    MeterUnit.POWER:                   ("Power",                          domo.PowerDevice,         ["w"]              ),
    MeterUnit.L1_POWER:                ("L1 Power",                       domo.PowerDevice,         ["wpha"]           ),
    MeterUnit.L2_POWER:                ("L2 Power",                       domo.PowerDevice,         ["wphb"]           ),
    MeterUnit.POWER_APPARENT:          ("Power (Apparent)",               domo.ApparentPowerDevice, ["va"]             ),
    MeterUnit.L1_POWER_APPARENT:       ("L1 Power (Apparent)",            domo.ApparentPowerDevice, ["vapha"]          ),
    MeterUnit.L2_POWER_APPARENT:       ("L2 Power (Apparent)",            domo.ApparentPowerDevice, ["vaphb"]          ),
    MeterUnit.POWER_REACTIVE:          ("Power (Reactive)",               domo.ReactivePowerDevice, ["var"]            ),
    MeterUnit.L1_POWER_REACTIVE:       ("L1 Power (Reactive)",            domo.ReactivePowerDevice, ["varpha"]         ),
    MeterUnit.L2_POWER_REACTIVE:       ("L2 Power (Reactive)",            domo.ReactivePowerDevice, ["varphb"]         ),
    MeterUnit.POWER_FACTOR:            ("Power Factor",                   domo.PercentageDevice,    ["pf"]             ),
    MeterUnit.L1_POWER_FACTOR:         ("L1 Power Factor",                domo.PercentageDevice,    ["pfpha"]          ),
    MeterUnit.L2_POWER_FACTOR:         ("L2 Power Factor",                domo.PercentageDevice,    ["pfphb"]          ),
    MeterUnit.EXPORT_ENERGY_ACTIVE:    ("Total Exported Energy (Active)", domo.EnergyExportDevice,  ["w","totwhexp"]   ),
    MeterUnit.L1_EXPORT_ENERGY_ACTIVE: ("L1 Exported Energy (Active)",    domo.EnergyExportDevice,  ["w","totwhexppha"]),
    MeterUnit.L2_EXPORT_ENERGY_ACTIVE: ("L2 Exported Energy (Active)",    domo.EnergyExportDevice,  ["w","totwhexpphb"]),
    MeterUnit.IMPORT_ENERGY_ACTIVE:    ("Total Imported Energy (Active)", domo.EnergyImportDevice,  ["w","totwhimp"]   ),
    MeterUnit.L1_IMPORT_ENERGY_ACTIVE: ("L1 Imported Energy (Active)",    domo.EnergyImportDevice,  ["w","totwhimppha"]),
    MeterUnit.L2_IMPORT_ENERGY_ACTIVE: ("L2 Imported Energy (Active)",    domo.EnergyImportDevice,  ["w","totwhimpphb"]),
}

WyeThreePhaseMeterDeviceMap: DeviceMapping = {
    MeterUnit.CURRENT:                 ("Current",                        domo.CurrentDevice,       ["a"]              ),
    MeterUnit.L1_CURRENT:              ("L1 Current",                     domo.CurrentDevice,       ["apha"]           ),
    MeterUnit.L2_CURRENT:              ("L2 Current",                     domo.CurrentDevice,       ["aphb"]           ),
    MeterUnit.L3_CURRENT:              ("L3 Current",                     domo.CurrentDevice,       ["aphc"]           ),
    MeterUnit.LN_VOLTAGE:              ("LN Voltage",                     domo.VoltageDevice,       ["phv"]            ),
    MeterUnit.L1N_VOLTAGE:             ("L1-N Voltage",                   domo.VoltageDevice,       ["phvpha"]         ),
    MeterUnit.L2N_VOLTAGE:             ("L2-N Voltage",                   domo.VoltageDevice,       ["phvphb"]         ),
    MeterUnit.L3N_VOLTAGE:             ("L3-N Voltage",                   domo.VoltageDevice,       ["phvphc"]         ),
    MeterUnit.LL_VOLTAGE:              ("LL Voltage",                     domo.VoltageDevice,       ["ppv"]            ),
    MeterUnit.L12_VOLTAGE:             ("L1-2 Voltage",                   domo.VoltageDevice,       ["phvphab"]        ),
    MeterUnit.L23_VOLTAGE:             ("L2-3 Voltage",                   domo.VoltageDevice,       ["phvphbc"]        ),
    MeterUnit.L31_VOLTAGE:             ("L3-1 Voltage",                   domo.VoltageDevice,       ["phvphca"]        ),
    MeterUnit.FREQUENCY:               ("Frequency",                      domo.FrequencyDevice,     ["hz"]             ),
    MeterUnit.POWER:                   ("Power",                          domo.PowerDevice,         ["w"]              ),
    MeterUnit.L1_POWER:                ("L1 Power",                       domo.PowerDevice,         ["wpha"]           ),
    MeterUnit.L2_POWER:                ("L2 Power",                       domo.PowerDevice,         ["wphb"]           ),
    MeterUnit.L3_POWER:                ("L3 Power",                       domo.PowerDevice,         ["wphc"]           ),
    MeterUnit.POWER_APPARENT:          ("Power (Apparent)",               domo.ApparentPowerDevice, ["va"]             ),
    MeterUnit.L1_POWER_APPARENT:       ("L1 Power (Apparent)",            domo.ApparentPowerDevice, ["vapha"]          ),
    MeterUnit.L2_POWER_APPARENT:       ("L2 Power (Apparent)",            domo.ApparentPowerDevice, ["vaphb"]          ),
    MeterUnit.L3_POWER_APPARENT:       ("L3 Power (Apparent)",            domo.ApparentPowerDevice, ["vaphc"]          ),
    MeterUnit.POWER_REACTIVE:          ("Power (Reactive)",               domo.ReactivePowerDevice, ["var"]            ),
    MeterUnit.L1_POWER_REACTIVE:       ("L1 Power (Reactive)",            domo.ReactivePowerDevice, ["varpha"]         ),
    MeterUnit.L2_POWER_REACTIVE:       ("L2 Power (Reactive)",            domo.ReactivePowerDevice, ["varphb"]         ),
    MeterUnit.L3_POWER_REACTIVE:       ("L3 Power (Reactive)",            domo.ReactivePowerDevice, ["varphc"]         ),
    MeterUnit.POWER_FACTOR:            ("Power Factor",                   domo.PercentageDevice,    ["pf"]             ),
    MeterUnit.L1_POWER_FACTOR:         ("L1 Power Factor",                domo.PercentageDevice,    ["pfpha"]          ),
    MeterUnit.L2_POWER_FACTOR:         ("L2 Power Factor",                domo.PercentageDevice,    ["pfphb"]          ),
    MeterUnit.L3_POWER_FACTOR:         ("L3 Power Factor",                domo.PercentageDevice,    ["pfphc"]          ),
    MeterUnit.EXPORT_ENERGY_ACTIVE:    ("Total Exported Energy (Active)", domo.EnergyExportDevice,  ["w","totwhexp"]   ),
    MeterUnit.L1_EXPORT_ENERGY_ACTIVE: ("L1 Exported Energy (Active)",    domo.EnergyExportDevice,  ["w","totwhexppha"]),
    MeterUnit.L2_EXPORT_ENERGY_ACTIVE: ("L2 Exported Energy (Active)",    domo.EnergyExportDevice,  ["w","totwhexpphb"]),
    MeterUnit.L3_EXPORT_ENERGY_ACTIVE: ("L3 Exported Energy (Active)",    domo.EnergyExportDevice,  ["w","totwhexpphc"]),
    MeterUnit.IMPORT_ENERGY_ACTIVE:    ("Total Imported Energy (Active)", domo.EnergyImportDevice,  ["w","totwhimp"]   ),
    MeterUnit.L1_IMPORT_ENERGY_ACTIVE: ("L1 Imported Energy (Active)",    domo.EnergyImportDevice,  ["w","totwhimppha"]),
    MeterUnit.L2_IMPORT_ENERGY_ACTIVE: ("L2 Imported Energy (Active)",    domo.EnergyImportDevice,  ["w","totwhimpphb"]),
    MeterUnit.L3_IMPORT_ENERGY_ACTIVE: ("L3 Imported Energy (Active)",    domo.EnergyImportDevice,  ["w","totwhimpphc"]),
}

# This mapping needs verification - it's a best guess for now
# A delta connect three phase (ABC) meter is measuring 3-phase power system
# where there's no neutral conductor.
DeltaConnectThreePhaseMeterDeviceMap: DeviceMapping = {
    MeterUnit.CURRENT:                 ("Current",                        domo.CurrentDevice,       ["a"]              ),
    MeterUnit.L1_CURRENT:              ("L1 Current",                     domo.CurrentDevice,       ["apha"]           ),
    MeterUnit.L2_CURRENT:              ("L2 Current",                     domo.CurrentDevice,       ["aphb"]           ),
    MeterUnit.L3_CURRENT:              ("L3 Current",                     domo.CurrentDevice,       ["aphc"]           ),
    MeterUnit.LL_VOLTAGE:              ("LL Voltage",                     domo.VoltageDevice,       ["ppv"]            ),
    MeterUnit.L12_VOLTAGE:             ("L1-2 Voltage",                   domo.VoltageDevice,       ["phvphab"]        ),
    MeterUnit.L23_VOLTAGE:             ("L2-3 Voltage",                   domo.VoltageDevice,       ["phvphbc"]        ),
    MeterUnit.L31_VOLTAGE:             ("L3-1 Voltage",                   domo.VoltageDevice,       ["phvphca"]        ),
    MeterUnit.FREQUENCY:               ("Frequency",                      domo.FrequencyDevice,     ["hz"]             ),
    MeterUnit.POWER:                   ("Power",                          domo.PowerDevice,         ["w"]              ),
    MeterUnit.L1_POWER:                ("L1 Power",                       domo.PowerDevice,         ["wpha"]           ),
    MeterUnit.L2_POWER:                ("L2 Power",                       domo.PowerDevice,         ["wphb"]           ),
    MeterUnit.L3_POWER:                ("L3 Power",                       domo.PowerDevice,         ["wphc"]           ),
    MeterUnit.POWER_APPARENT:          ("Power (Apparent)",               domo.ApparentPowerDevice, ["va"]             ),
    MeterUnit.L1_POWER_APPARENT:       ("L1 Power (Apparent)",            domo.ApparentPowerDevice, ["vapha"]          ),
    MeterUnit.L2_POWER_APPARENT:       ("L2 Power (Apparent)",            domo.ApparentPowerDevice, ["vaphb"]          ),
    MeterUnit.L3_POWER_APPARENT:       ("L3 Power (Apparent)",            domo.ApparentPowerDevice, ["vaphc"]          ),
    MeterUnit.POWER_REACTIVE:          ("Power (Reactive)",               domo.ReactivePowerDevice, ["var"]            ),
    MeterUnit.L1_POWER_REACTIVE:       ("L1 Power (Reactive)",            domo.ReactivePowerDevice, ["varpha"]         ),
    MeterUnit.L2_POWER_REACTIVE:       ("L2 Power (Reactive)",            domo.ReactivePowerDevice, ["varphb"]         ),
    MeterUnit.L3_POWER_REACTIVE:       ("L3 Power (Reactive)",            domo.ReactivePowerDevice, ["varphc"]         ),
    MeterUnit.POWER_FACTOR:            ("Power Factor",                   domo.PercentageDevice,    ["pf"]             ),
    MeterUnit.L1_POWER_FACTOR:         ("L1 Power Factor",                domo.PercentageDevice,    ["pfpha"]          ),
    MeterUnit.L2_POWER_FACTOR:         ("L2 Power Factor",                domo.PercentageDevice,    ["pfphb"]          ),
    MeterUnit.L3_POWER_FACTOR:         ("L3 Power Factor",                domo.PercentageDevice,    ["pfphc"]          ),
    MeterUnit.EXPORT_ENERGY_ACTIVE:    ("Total Exported Energy (Active)", domo.EnergyExportDevice,  ["w","totwhexp"]   ),
    MeterUnit.L1_EXPORT_ENERGY_ACTIVE: ("L1 Exported Energy (Active)",    domo.EnergyExportDevice,  ["w","totwhexppha"]),
    MeterUnit.L2_EXPORT_ENERGY_ACTIVE: ("L2 Exported Energy (Active)",    domo.EnergyExportDevice,  ["w","totwhexpphb"]),
    MeterUnit.L3_EXPORT_ENERGY_ACTIVE: ("L3 Exported Energy (Active)",    domo.EnergyExportDevice,  ["w","totwhexpphc"]),
    MeterUnit.IMPORT_ENERGY_ACTIVE:    ("Total Imported Energy (Active)", domo.EnergyImportDevice,  ["w","totwhimp"]   ),
    MeterUnit.L1_IMPORT_ENERGY_ACTIVE: ("L1 Imported Energy (Active)",    domo.EnergyImportDevice,  ["w","totwhimppha"]),
    MeterUnit.L2_IMPORT_ENERGY_ACTIVE: ("L2 Imported Energy (Active)",    domo.EnergyImportDevice,  ["w","totwhimpphb"]),
    MeterUnit.L3_IMPORT_ENERGY_ACTIVE: ("L3 Imported Energy (Active)",    domo.EnergyImportDevice,  ["w","totwhimpphc"]),
}

@unique
class BatteryUnit(UnitEnum):
    """Lists the individual measurements supported by Batteries"""

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

BatteryStartOffset:int = (InverterMaxDevices*InverterMaxOffset) + (MeterMaxDevices*MeterMaxOffset)
BatteryMaxOffset:int = max(BatteryUnit)
BatteryMaxDevices:int = 2

BatteryDeviceMap: DeviceMapping = {
    BatteryUnit.STATUS:                   ("Status",                             domo.TextStatusDevice,           ["status"]   ),
    BatteryUnit.STATUS_INTERNAL:          ("Internal Status",                    domo.TextStatusDevice,           ["sti"]      ),
    BatteryUnit.EVENT_LOG:                ("Event Log",                          domo.TextStatusDevice,           ["el"]       ),
    BatteryUnit.EVENT_LOG_INTERNAL:       ("Internal Event Log",                 domo.TextStatusDevice,           ["eli"]      ),
    BatteryUnit.RATED_ENERGY:             ("Rated Energy",                       domo.ManagedCounterEnergyDevice, ["re"]       ),
    BatteryUnit.MAX_CHARGE_CONT_POWER:    ("Maximum Charge Continuous Power",    domo.PowerDevice,                ["mccp"]     ),
    BatteryUnit.MAX_DISCHARGE_CONT_POWER: ("Maximum Discharge Continuous Power", domo.PowerDevice,                ["mdcp"]     ),
    BatteryUnit.MAX_CHARGE_PEAK_POWER:    ("Maximum Charge Peak Power",          domo.PowerDevice,                ["mcpp"]     ),
    BatteryUnit.MAX_DISCHARGE_PEAK_POWER: ("Maximum Discharge Peak Power",       domo.PowerDevice,                ["mdpp"]     ),
    BatteryUnit.AVERAGE_TEMP:             ("Average Temperature",                domo.TemperatureDevice,          ["at"]       ),
    BatteryUnit.MAX_TEMP:                 ("Maximum Temperature",                domo.TemperatureDevice,          ["mt"]       ),
    BatteryUnit.INSTANT_VOLTAGE:          ("Instantaneous Voltage",              domo.VoltageDevice,              ["iv"]       ),
    BatteryUnit.INSTANT_CURRENT:          ("Instantaneous Current",              domo.CurrentDevice,              ["ic"]       ),
    BatteryUnit.INSTANT_POWER:            ("Instantaneous Power",                domo.PowerDevice,                ["ip"]       ),
    BatteryUnit.LIFE_EXPORT_ENERGY_COUNT: ("Total Exported Energy",              domo.EnergyExportDevice,         ["ip","leec"]),
    BatteryUnit.LIFE_IMPORT_ENERGY_COUNT: ("Total Imported Energy",              domo.EnergyImportDevice,         ["ip","liec"]),
    BatteryUnit.MAX_ENERGY:               ("Maximum Energy",                     domo.ManagedCounterEnergyDevice, ["me"]       ),
    BatteryUnit.AVAILABLE_ENERGY:         ("Available Energy",                   domo.ManagedCounterEnergyDevice, ["ae"]       ),
    BatteryUnit.SOH:                      ("State of Health",                    domo.PercentageDevice,           ["soh"]      ),
    BatteryUnit.SOE:                      ("State of Energy",                    domo.PercentageDevice,           ["soe"]      ),
}



def Map(solaredge_device: solaredge.Device) -> MapDetails|None:
    """Map a SolarEdge device to the plugin device"""
    result: MapDetails | None = None

    match solaredge_device:
        case solaredge.sunspec.SunSpecDeviceModel101():
            result = MapDetails(
                start_offset=InverterStartOffset,
                max_offset=InverterMaxOffset,
                max_devices=InverterMaxDevices,
                device_type=DeviceTypeMapping.INVERTER,
                mapping = SinglePhaseInverterDeviceMap
                )
        case solaredge.sunspec.SunSpecDeviceModel102():
            result = MapDetails(
                start_offset=InverterStartOffset,
                max_offset=InverterMaxOffset,
                max_devices=InverterMaxDevices,
                device_type=DeviceTypeMapping.INVERTER,
                mapping = TwoPhaseInverterDeviceMap
                )
        case solaredge.sunspec.SunSpecDeviceModel103():
            result = MapDetails(
                start_offset=InverterStartOffset,
                max_offset=InverterMaxOffset,
                max_devices=InverterMaxDevices,
                device_type=DeviceTypeMapping.INVERTER,
                mapping = ThreePhaseInverterDeviceMap
                )
        case solaredge.sunspec.SunSpecDeviceModel201:
            result = MapDetails(
                start_offset=MeterStartOffset,
                max_offset=MeterMaxOffset,
                max_devices=MeterMaxDevices,
                device_type=DeviceTypeMapping.METER,
                mapping = SinglePhaseMeterDeviceMap
                )
        case solaredge.sunspec.SunSpecDeviceModel202:
            result = MapDetails(
                start_offset=MeterStartOffset,
                max_offset=MeterMaxOffset,
                max_devices=MeterMaxDevices,
                device_type=DeviceTypeMapping.METER,
                mapping = SplitPhaseMeterDeviceMap
                )
        case solaredge.sunspec.SunSpecDeviceModel203:
            result = MapDetails(
                start_offset=MeterStartOffset,
                max_offset=MeterMaxOffset,
                max_devices=MeterMaxDevices,
                device_type=DeviceTypeMapping.METER,
                mapping = WyeThreePhaseMeterDeviceMap
                )
        case solaredge.sunspec.SunSpecDeviceModel204:
            result = MapDetails(
                start_offset=MeterStartOffset,
                max_offset=MeterMaxOffset,
                max_devices=MeterMaxDevices,
                device_type=DeviceTypeMapping.METER,
                mapping = DeltaConnectThreePhaseMeterDeviceMap
                )

        case solaredge.vendor.VendorBattery:
            result = MapDetails(
                start_offset=BatteryStartOffset,
                max_offset=BatteryMaxOffset,
                max_devices=BatteryMaxDevices,
                device_type=DeviceTypeMapping.BATTERY,
                mapping = BatteryDeviceMap
                )
        case _:
            pass

    return result
