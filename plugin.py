#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SolarEdge ModbusTCP
#
# Source:  https://github.com/addiejanssen/domoticz-solaredge-modbustcp-plugin
# Author:  Addie Janssen (https://addiejanssen.com)
# License: MIT
#

"""
<plugin key="SolarEdge_ModbusTCP" name="SolarEdge ModbusTCP" author="Addie Janssen" version="1.0.3" externallink="https://github.com/addiejanssen/domoticz-solaredge-modbustcp-plugin">
    <params>
        <param field="Address" label="Inverter IP Address" width="150px" required="true" />
        <param field="Port" label="Inverter Port Number" width="100px" required="true" default="502" />
        <param field="Mode1" label="Add missing devices" width="100px" required="true" default="Yes" >
            <options>
                <option label="Yes" value="Yes" default="true" />
                <option label="No" value="No" />
            </options>
        </param>
        <param field="Mode2" label="Interval" width="100px" required="true" default="5" >
            <options>
                <option label="5  seconds" value="5" default="true" />
                <option label="10 seconds" value="10" />
                <option label="20 seconds" value="20" />
                <option label="30 seconds" value="30" />
                <option label="60 seconds" value="60" />
            </options>
        </param>
        <param field="Mode6" label="Debug" width="100px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true" />
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import solaredge_modbus
import json

from datetime import datetime, timedelta
from enum import IntEnum, unique, auto
from pymodbus.exceptions import ConnectionException

#
# Domoticz shows graphs with intervals of 5 minutes.
# When collecting information from the inverter more frequently than that, then it makes no sense to only show the last value.
#
# The Average class can be used to calculate the average value based on a sliding window of samples.
# The number of samples stored depends on the interval used to collect the value from the inverter itself.
#

class Average:

    def __init__(self):
        self.samples = []
        self.max_samples = 30

    def set_max_samples(self, max):
        self.max_samples = max
        if self.max_samples < 1:
            self.max_samples = 1

    def update(self, new_value, scale = 0):
        self.samples.append(new_value * (10 ** scale))
        while (len(self.samples) > self.max_samples):
            del self.samples[0]

        Domoticz.Debug("Average: {} - {} values".format(self.get(), len(self.samples)))

    def get(self):
        return sum(self.samples) / len(self.samples)

#
# Domoticz shows graphs with intervals of 5 minutes.
# When collecting information from the inverter more frequently than that, then it makes no sense to only show the last value.
#
# The Maximum class can be used to calculate the highest value based on a sliding window of samples.
# The number of samples stored depends on the interval used to collect the value from the inverter itself.
#

class Maximum:

    def __init__(self):
        self.samples = []
        self.max_samples = 30

    def set_max_samples(self, max):
        self.max_samples = max
        if self.max_samples < 1:
            self.max_samples = 1

    def update(self, new_value, scale = 0):
        self.samples.append(new_value * (10 ** scale))
        while (len(self.samples) > self.max_samples):
            del self.samples[0]

        Domoticz.Debug("Maximum: {} - {} values".format(self.get(), len(self.samples)))

    def get(self):
        return max(self.samples)

#
# The Unit class lists all possible pieces of information that can be retrieved from the inverter.
#
# Not all inverters will support all these options.
# The class is used to generate a unique id for each device in Domoticz.
#

@unique
class Unit(IntEnum):

    STATUS          = 1
    VENDOR_STATUS   = 2
    CURRENT         = 3
    P1_CURRENT      = 4
    P2_CURRENT      = 5
    P3_CURRENT      = 6
    P1_VOLTAGE      = 7
    P2_VOLTAGE      = 8
    P3_VOLTAGE      = 9
    P1N_VOLTAGE     = 10
    P2N_VOLTAGE     = 11
    P3N_VOLTAGE     = 12
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
# The plugin is using a few tables to setup Domoticz and to process the feedback from the inverter.
# The Column class is used to easily identify the columns in those tables.
#

@unique
class Column(IntEnum):

    ID              = 0
    NAME            = 1
    TYPE            = 2
    SUBTYPE         = 3
    SWITCHTYPE      = 4
    OPTIONS         = 5
    MODBUSNAME      = 6
    MODBUSSCALE     = 7
    FORMAT          = 8
    PREPEND         = 9
    LOOKUP          = 10
    MATH            = 11

#
# This table represents a single phase inverter.
#

SINGLE_PHASE_INVERTER = [
#   ID,                    NAME,                TYPE,  SUBTYPE,  SWITCHTYPE, OPTIONS,                MODBUSNAME,        MODBUSSCALE,            FORMAT,    PREPEND,        LOOKUP,                                MATH
    [Unit.STATUS,          "Status",            0xF3,  0x13,     0x00,       {},                     "status",          None,                   "{}",      None,           solaredge_modbus.INVERTER_STATUS_MAP,  None      ],
    [Unit.VENDOR_STATUS,   "Vendor Status",     0xF3,  0x13,     0x00,       {},                     "vendor_status",   None,                   "{}",      None,           None,                                  None      ],
    [Unit.CURRENT,         "Current",           0xF3,  0x17,     0x00,       {},                     "current",         "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.P1_CURRENT,      "P1 Current",        0xF3,  0x17,     0x00,       {},                     "p1_current",      "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.P1_VOLTAGE,      "P1 Voltage",        0xF3,  0x08,     0x00,       {},                     "p1_voltage",      "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.P1N_VOLTAGE,     "P1-N Voltage",      0xF3,  0x08,     0x00,       {},                     "p1n_voltage",     "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_AC,        "Power",             0xF8,  0x01,     0x00,       {},                     "power_ac",        "power_ac_scale",       "{:.2f}",  None,           None,                                  Average() ],
    [Unit.FREQUENCY,       "Frequency",         0xF3,  0x1F,     0x00,       { "Custom": "1;Hz"  },  "frequency",       "frequency_scale",      "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_APPARENT,  "Power (Apparent)",  0xF3,  0x1F,     0x00,       { "Custom": "1;VA"  },  "power_apparent",  "power_apparent_scale", "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_REACTIVE,  "Power (Reactive)",  0xF3,  0x1F,     0x00,       { "Custom": "1;VAr" },  "power_reactive",  "power_reactive_scale", "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_FACTOR,    "Power Factor",      0xF3,  0x06,     0x00,       {},                     "power_factor",    "power_factor_scale",   "{:.2f}",  None,           None,                                  Average() ],
    [Unit.ENERGY_TOTAL,    "Total Energy",      0xF3,  0x1D,     0x04,       {},                     "energy_total",    "energy_total_scale",   "{};{}",   Unit.POWER_AC,  None,                                  Average() ],
    [Unit.CURRENT_DC,      "DC Current",        0xF3,  0x17,     0x00,       {},                     "current_dc",      "current_dc_scale",     "{:.2f}",  None,           None,                                  None      ],
    [Unit.VOLTAGE_DC,      "DC Voltage",        0xF3,  0x08,     0x00,       {},                     "voltage_dc",      "voltage_dc_scale",     "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_DC,        "DC Power",          0xF8,  0x01,     0x00,       {},                     "power_dc",        "power_dc_scale",       "{:.2f}",  None,           None,                                  Average() ],
    [Unit.TEMPERATURE,     "Temperature",       0xF3,  0x05,     0x00,       {},                     "temperature",     "temperature_scale",    "{:.2f}",  None,           None,                                  Maximum() ]
]

#
# This table represents a three phase inverter.
#

THREE_PHASE_INVERTER = [
#   ID,                    NAME,                TYPE,  SUBTYPE,  SWITCHTYPE, OPTIONS,                MODBUSNAME,        MODBUSSCALE,            FORMAT,    PREPEND,        LOOKUP,                                MATH
    [Unit.STATUS,          "Status",            0xF3,  0x13,     0x00,       {},                     "status",          None,                   "{}",      None,           solaredge_modbus.INVERTER_STATUS_MAP,  None      ],
    [Unit.VENDOR_STATUS,   "Vendor Status",     0xF3,  0x13,     0x00,       {},                     "vendor_status",   None,                   "{}",      None,           None,                                  None      ],
    [Unit.CURRENT,         "Current",           0xF3,  0x17,     0x00,       {},                     "current",         "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.P1_CURRENT,      "P1 Current",        0xF3,  0x17,     0x00,       {},                     "p1_current",      "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.P2_CURRENT,      "P2 Current",        0xF3,  0x17,     0x00,       {},                     "p2_current",      "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.P3_CURRENT,      "P3 Current",        0xF3,  0x17,     0x00,       {},                     "p3_current",      "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.P1_VOLTAGE,      "P1 Voltage",        0xF3,  0x08,     0x00,       {},                     "p1_voltage",      "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.P2_VOLTAGE,      "P2 Voltage",        0xF3,  0x08,     0x00,       {},                     "p2_voltage",      "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.P3_VOLTAGE,      "P3 Voltage",        0xF3,  0x08,     0x00,       {},                     "p3_voltage",      "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.P1N_VOLTAGE,     "P1-N Voltage",      0xF3,  0x08,     0x00,       {},                     "p1n_voltage",     "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.P2N_VOLTAGE,     "P2-N Voltage",      0xF3,  0x08,     0x00,       {},                     "p2n_voltage",     "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.P3N_VOLTAGE,     "P3-N Voltage",      0xF3,  0x08,     0x00,       {},                     "p3n_voltage",     "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_AC,        "Power",             0xF8,  0x01,     0x00,       {},                     "power_ac",        "power_ac_scale",       "{:.2f}",  None,           None,                                  Average() ],
    [Unit.FREQUENCY,       "Frequency",         0xF3,  0x1F,     0x00,       { "Custom": "1;Hz"  },  "frequency",       "frequency_scale",      "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_APPARENT,  "Power (Apparent)",  0xF3,  0x1F,     0x00,       { "Custom": "1;VA"  },  "power_apparent",  "power_apparent_scale", "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_REACTIVE,  "Power (Reactive)",  0xF3,  0x1F,     0x00,       { "Custom": "1;VAr" },  "power_reactive",  "power_reactive_scale", "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_FACTOR,    "Power Factor",      0xF3,  0x06,     0x00,       {},                     "power_factor",    "power_factor_scale",   "{:.2f}",  None,           None,                                  Average() ],
    [Unit.ENERGY_TOTAL,    "Total Energy",      0xF3,  0x1D,     0x04,       {},                     "energy_total",    "energy_total_scale",   "{};{}",   Unit.POWER_AC,  None,                                  Average() ],
    [Unit.CURRENT_DC,      "DC Current",        0xF3,  0x17,     0x00,       {},                     "current_dc",      "current_dc_scale",     "{:.2f}",  None,           None,                                  None      ],
    [Unit.VOLTAGE_DC,      "DC Voltage",        0xF3,  0x08,     0x00,       {},                     "voltage_dc",      "voltage_dc_scale",     "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_DC,        "DC Power",          0xF8,  0x01,     0x00,       {},                     "power_dc",        "power_dc_scale",       "{:.2f}",  None,           None,                                  Average() ],
    [Unit.TEMPERATURE,     "Temperature",       0xF3,  0x05,     0x00,       {},                     "temperature",     "temperature_scale",    "{:.2f}",  None,           None,                                  Maximum() ]
]

#
# The BasePlugin is the actual Domoticz plugin.
# This is where the fun starts :-)
#

class BasePlugin:

    def __init__(self):

        # The _LOOKUP_TABLE will point to one of the tables above, depending on the type of inverter.

        self._LOOKUP_TABLE = None

        # This is the solaredge_modbus Inverter object that will be used to communicate with the inverter.

        self.inverter = None

        # Default heartbeat is 10 seconds; therefore 30 samples in 5 minutes.

        self.max_samples = 30

        # Whether the plugin should add missing devices.
        # If set to True, a deleted device will be added on the next restart of Domoticz.

        self.add_devices = False

        # When there is an issue contacting the inverter, the plugin will retry after a certain retry delay.
        # The actual time after which the plugin will try again is stored in the retry after variable.
        # According to the documenation, the inverter may need up to 2 minutes to "reset".

        self.retrydelay = timedelta(minutes = 2)
        self.retryafter = datetime.now() - timedelta(seconds = 1)

    #
    # onStart is called by Domoticz to start the processing of the plugin.
    #

    def onStart(self):

        self.add_devices = bool(Parameters["Mode1"])

        # Domoticz will generate graphs showing an interval of 5 minutes.
        # Calculate the number of samples to store over a period of 5 minutes.

        self.max_samples = 300 / int(Parameters["Mode2"])

        # Now set the interval at which the information is collected accordingly.

        Domoticz.Heartbeat(int(Parameters["Mode2"]))

        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
        else:
            Domoticz.Debugging(0)

        Domoticz.Debug(
            "onStart Address: {} Port: {}".format(
                Parameters["Address"],
                Parameters["Port"]
            )
        )

        self.inverter = solaredge_modbus.Inverter(
            host=Parameters["Address"],
            port=Parameters["Port"],
            timeout=3,
            unit=1
        )

        # Lets get in touch with the inverter.

        self.contactInverter()


    #
    # OnHeartbeat is called by Domoticz at a specific interval as set in onStart()
    #

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat")

        # We need to make sure that we have a table to work with.
        # This will be set by contactInverter and will be None till it is clear
        # that the inverter responds and that a matching table is available.

        if self._LOOKUP_TABLE:

            inverter_values = None
            try:
                inverter_values = self.inverter.read_all()
            except ConnectionException:
                inverter_values = None
                Domoticz.Debug("ConnectionException")
            else:

                if inverter_values:

                    Domoticz.Debug(json.dumps(inverter_values, indent=4, sort_keys=True))

                    # Just for cosmetics in the log

                    updated = 0
                    device_count = 0

                    # Now process each unit in the table.

                    for unit in self._LOOKUP_TABLE:
                        Domoticz.Debug(str(unit))

                        # Skip a unit when the matching device got deleted.

                        if unit[Column.ID] in Devices:
                            Domoticz.Debug("-> found in Devices")

                            # For certain units the table has a lookup table to replace the value with something else.

                            if unit[Column.LOOKUP]:
                                Domoticz.Debug("-> looking up...")

                                lookup_table = unit[Column.LOOKUP]
                                to_lookup = int(inverter_values[unit[Column.MODBUSNAME]])

                                if to_lookup < len(lookup_table):
                                    value = lookup_table[to_lookup]
                                else:
                                    value = "Key not found in lookup table: {}".format(to_lookup)

                            # When a math object is setup for the unit, update the samples in it and get the calculated value.

                            elif unit[Column.MATH]:
                                Domoticz.Debug("-> calculating...")
                                m = unit[Column.MATH]
                                if unit[Column.MODBUSSCALE]:
                                    m.update(inverter_values[unit[Column.MODBUSNAME]], inverter_values[unit[Column.MODBUSSCALE]])
                                else:
                                    m.update(inverter_values[unit[Column.MODBUSNAME]])

                                value = m.get()

                            # When there is no math object then just store the latest value.
                            # Some values from the inverter need to be scaled before they can be stored.

                            elif unit[Column.MODBUSSCALE]:
                                Domoticz.Debug("-> calculating...")
                                # we need to do some calculation here
                                value = inverter_values[unit[Column.MODBUSNAME]] * (10 ** inverter_values[unit[Column.MODBUSSCALE]])

                            # Some values require no action but storing in Domoticz.

                            else:
                                Domoticz.Debug("-> copying...")
                                value = inverter_values[unit[Column.MODBUSNAME]]

                            Domoticz.Debug("value = {}".format(value))

                            # Time to store the value in Domoticz.
                            # Some devices require multiple values, in which case the plugin will combine those values.
                            # Currently, there is only a need to prepend one value with another.

                            if unit[Column.PREPEND]:
                                Domoticz.Debug("-> has prepend")
                                prepend = Devices[unit[Column.PREPEND]].sValue
                                Domoticz.Debug("prepend = {}".format(prepend))
                                sValue = unit[Column.FORMAT].format(prepend, value)
                            else:
                                Domoticz.Debug("-> no prepend")
                                sValue = unit[Column.FORMAT].format(value)

                            Domoticz.Debug("sValue = {}".format(sValue))

                            # Only store the value in Domoticz when it has changed.
                            # TODO:
                            #   We should not store certain values when the inverter is sleeping.
                            #   That results in a strange graph; it would be better just to skip it then.

                            if sValue != Devices[unit[Column.ID]].sValue:
                                Devices[unit[Column.ID]].Update(nValue=0, sValue=str(sValue), TimedOut=0)
                                updated += 1

                            device_count += 1

                        else:
                            Domoticz.Debug("-> NOT found in Devices")

                    Domoticz.Log("Updated {} values out of {}".format(updated, device_count))
                else:
                    Domoticz.Log("Inverter returned no information")

        # Try to contact the inverter when the lookup table is not yet initialized.

        else:
            self.contactInverter()


    #
    # Contact the inverter and find out what type it is.
    # Initialize the lookup table when the type is supported.
    #
    
    def contactInverter(self):

        # Do not stress the inverter when it did not respond in the previous attempt to contact it.

        if self.retryafter <= datetime.now():

            # Here we go...
            inverter_values = None
            try:
                inverter_values = self.inverter.read_all()
            except ConnectionException:

                # There are multiple reasons why this may fail.
                # - Perhaps the ip address or port are incorrect.
                # - The inverter may not be connected to the networ,
                # - The inverter may be turned off.
                # - The inverter has a bad hairday....
                # Try again in the future.

                self.retryafter = datetime.now() + self.retrydelay
                inverter_values = None

                Domoticz.Log("Connection Exception when trying to contact: {}:{}".format(Parameters["Address"], Parameters["Port"]))
                Domoticz.Log("Retrying to communicate with inverter after: {}".format(self.retryafter))

            else:

                if inverter_values:
                    Domoticz.Log("Connection established with: {}:{}".format(Parameters["Address"], Parameters["Port"]))

                    inverter_type = solaredge_modbus.sunspecDID(inverter_values["c_sunspec_did"])
                    Domoticz.Log("Inverter type: {}".format(inverter_type))

                    # The plugin currently has 2 supported types.
                    # This may be updated in the future based on user feedback.

                    if inverter_type == solaredge_modbus.sunspecDID.SINGLE_PHASE_INVERTER:
                        self._LOOKUP_TABLE = SINGLE_PHASE_INVERTER
                    elif inverter_type == solaredge_modbus.sunspecDID.THREE_PHASE_INVERTER:
                        self._LOOKUP_TABLE = THREE_PHASE_INVERTER
                    else:
                        Domoticz.Log("Unsupported inverter type: {}".format(inverter_type))

                    if self._LOOKUP_TABLE:

                        # Set the number of samples on all the math objects.

                        for unit in self._LOOKUP_TABLE:
                            if unit[Column.MATH]:
                                unit[Column.MATH].set_max_samples(self.max_samples)


                        # We updated some device types over time.
                        # Let's make sure that we have the correct type setup.

                        for unit in self._LOOKUP_TABLE:
                            if unit[Column.ID] in Devices:
                                device = Devices[unit[Column.ID]]
                                
                                if (device.Type != unit[Column.TYPE] or
                                    device.SubType != unit[Column.SUBTYPE] or
                                    device.SwitchType != unit[Column.SWITCHTYPE] or
                                    device.Options != unit[Column.OPTIONS]):

                                    Domoticz.Log("Updating device \"{}\"".format(device.Name))

                                    nValue = device.nValue
                                    sValue = device.sValue

                                    device.Update(
                                            Type=unit[Column.TYPE],
                                            Subtype=unit[Column.SUBTYPE],
                                            Switchtype=unit[Column.SWITCHTYPE],
                                            Options=unit[Column.OPTIONS],
                                            nValue=nValue,
                                            sValue=sValue
                                    )

                        # Add missing devices if needed.

                        if self.add_devices:
                            for unit in self._LOOKUP_TABLE:
                                if unit[Column.ID] not in Devices:
                                    Domoticz.Device(
                                        Unit=unit[Column.ID],
                                        Name=unit[Column.NAME],
                                        Type=unit[Column.TYPE],
                                        Subtype=unit[Column.SUBTYPE],
                                        Switchtype=unit[Column.SWITCHTYPE],
                                        Options=unit[Column.OPTIONS],
                                        Used=1,
                                    ).Create()
                else:
                    Domoticz.Log("Connection established with: {}:{}. BUT... inverter returned no information".format(Parameters["Address"], Parameters["Port"]))
                    Domoticz.Log("Retrying to communicate with inverter after: {}".format(self.retryafter))
        else:
            Domoticz.Log("Retrying to communicate with inverter after: {}".format(self.retryafter))


#
# Instantiate the plugin and register the supported callbacks.
# Currently that is only onStart() and onHeartbeat()
#

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()
