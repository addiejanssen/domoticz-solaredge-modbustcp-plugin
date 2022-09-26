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
<plugin key="SolarEdge_ModbusTCP" name="SolarEdge ModbusTCP" author="Addie Janssen" version="2.0.0" externallink="https://github.com/addiejanssen/domoticz-solaredge-modbustcp-plugin">
    <params>
        <param field="Address" label="Inverter IP Address" width="150px" required="true" />
        <param field="Port" label="Inverter Port Number" width="100px" required="true" default="502" />
        <param field="Mode3" label="Inverter Modbus device address" width="100px" required="true" default="1" />
        <param field="Mode1" label="Add missing devices" width="100px" required="true" default="Yes" >
            <options>
                <option label="Yes" value="Yes" default="true" />
                <option label="No" value="No" />
            </options>
        </param>
        <param field="Mode2" label="Interval" width="100px" required="true" default="5" >
            <options>
                <option label="1  second"  value="1" />
                <option label="2  seconds" value="2" />
                <option label="3  seconds" value="3" />
                <option label="4  seconds" value="4" />
                <option label="5  seconds" value="5" default="true" />
                <option label="10 seconds" value="10" />
                <option label="20 seconds" value="20" />
                <option label="30 seconds" value="30" />
                <option label="60 seconds" value="60" />
            </options>
        </param>
        <param field="Mode4" label="Auto Avg/Max math" width="100px">
            <options>
                <option label="Enabled" value="math_enabled" default="true" />
                <option label="Disabled" value="math_disabled"/>
            </options>
        </param>
        <param field="Mode5" label="Log level" width="100px">
            <options>
                <option label="Normal" value="Normal" default="true" />
                <option label="Extra" value="Extra"/>
                <option label="Debug" value="Debug"/>
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import solaredge_modbus
import json

import inverter_tables
import meter_tables

from datetime import datetime, timedelta
from enum import IntEnum, unique, auto
from pymodbus.exceptions import ConnectionException

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

        if Parameters["Mode5"] == "Debug":
            Domoticz.Debugging(1)
        else:
            Domoticz.Debugging(0)

        Domoticz.Debug(
            "onStart Address: {} Port: {} Device Address: {}".format(
                Parameters["Address"],
                Parameters["Port"],
                Parameters["Mode3"]
            )
        )

        self.inverter = solaredge_modbus.Inverter(
            host=Parameters["Address"],
            port=Parameters["Port"],
            timeout=5,
            unit=int(Parameters["Mode3"]) if Parameters["Mode3"] else 1
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

#            inverter_values = None
            meter_values = None
            try:
#                inverter_values = self.inverter.read_all()

                meter1 = self.inverter.meters()['Meter1']
                meter_values = meter1.read_all()
            except ConnectionException:
#                inverter_values = None
                meter_values = None
                Domoticz.Debug("ConnectionException")
            else:

#                if inverter_values:
                if meter_values:

                    if "Mode5" in Parameters and (Parameters["Mode5"] == "Extra" or Parameters["Mode5"] == "Debug"):
#                        to_log = inverter_values
                        to_log = meter_values
                        if "c_serialnumber" in to_log:
                            to_log.pop("c_serialnumber")
#                        Domoticz.Log("inverter values: {}".format(json.dumps(to_log, indent=4, sort_keys=False)))
                        Domoticz.Log("meter values: {}".format(json.dumps(to_log, indent=4, sort_keys=False)))

#                    self.process(self._DEVICE_OFFSET, self._LOOKUP_TABLE, inverter_values)
                    self.process(self._DEVICE_OFFSET, self._LOOKUP_TABLE, meter_values)
                else:
                    Domoticz.Log("Inverter returned no information")

        # Try to contact the inverter when the lookup table is not yet initialized.

        else:
            self.contactInverter()



    #
    # Go through the table and update matching devices
    # with the new values.
    #
    
    def process(self, offset, table, values):

        # Just for cosmetics in the log

        updated = 0
        device_count = 0

        # Now process each unit in the table.

        for unit in table:
            Domoticz.Debug(str(unit))

            # Skip a unit when the matching device got deleted.

            if (unit[Column.ID] + offset) in Devices:
                Domoticz.Debug("-> found in Devices")

                # For certain units the table has a lookup table to replace the value with something else.

                if unit[Column.LOOKUP]:
                    Domoticz.Debug("-> looking up...")

                    lookup_table = unit[Column.LOOKUP]
                    to_lookup = int(values[unit[Column.MODBUSNAME]])

                    if to_lookup >= 0 and to_lookup < len(lookup_table):
                        value = lookup_table[to_lookup]
                    else:
                        value = "Key not found in lookup table: {}".format(to_lookup)

                # When a math object is setup for the unit, update the samples in it and get the calculated value.

                elif unit[Column.MATH] and Parameters["Mode4"] == "math_enabled":
                    Domoticz.Debug("-> calculating...")
                    m = unit[Column.MATH]
                    if unit[Column.MODBUSSCALE]:
                        m.update(values[unit[Column.MODBUSNAME]], values[unit[Column.MODBUSSCALE]])
                    else:
                        m.update(values[unit[Column.MODBUSNAME]])

                    value = m.get()

                # When there is no math object then just store the latest value.
                # Some values from the inverter need to be scaled before they can be stored.

                elif unit[Column.MODBUSSCALE]:
                    Domoticz.Debug("-> scaling...")
                    # we need to do some calculation here
                    value = values[unit[Column.MODBUSNAME]] * (10 ** values[unit[Column.MODBUSSCALE]])

                # Some values require no action but storing in Domoticz.

                else:
                    Domoticz.Debug("-> copying...")
                    value = values[unit[Column.MODBUSNAME]]

                Domoticz.Debug("value = {}".format(value))

                # Time to store the value in Domoticz.
                # Some devices require multiple values, in which case the plugin will combine those values.
                # Currently, there is only a need to prepend one value with another.

                if unit[Column.PREPEND]:
                    Domoticz.Debug("-> has prepend")
                    prepend = Devices[unit[Column.PREPEND] + offset].sValue
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

                if sValue != Devices[unit[Column.ID] + offset].sValue:
                    Devices[unit[Column.ID] + offset].Update(nValue=0, sValue=str(sValue), TimedOut=0)
                    updated += 1

                device_count += 1

            else:
                Domoticz.Debug("-> NOT found in Devices")

        Domoticz.Log("Updated {} values out of {}".format(updated, device_count))


    #
    # Contact the inverter and find out what type it is.
    # Initialize the lookup table when the type is supported.
    #
    
    def contactInverter(self):

        # Do not stress the inverter when it did not respond in the previous attempt to contact it.

        if self.retryafter <= datetime.now():

            # Here we go...
#            inverter_values = None
            meter_values = None
            try:
#                inverter_values = self.inverter.read_all()

                meter1 = self.inverter.meters()['Meter1']
                meter_values = meter1.read_all()
            except ConnectionException:

                # There are multiple reasons why this may fail.
                # - Perhaps the ip address or port are incorrect.
                # - The inverter may not be connected to the networ,
                # - The inverter may be turned off.
                # - The inverter has a bad hairday....
                # Try again in the future.

                self.retryafter = datetime.now() + self.retrydelay
#                inverter_values = None
                meter_values = None

                Domoticz.Log("Connection Exception when trying to contact: {}:{} Device Address: {}".format(Parameters["Address"], Parameters["Port"], Parameters["Mode3"]))
                Domoticz.Log("Retrying to communicate with inverter after: {}".format(self.retryafter))

            else:

 #               if inverter_values:
                if meter_values:
                    Domoticz.Log("Connection established with: {}:{} Device Address: {}".format(Parameters["Address"], Parameters["Port"], Parameters["Mode3"]))

#                    inverter_type = solaredge_modbus.sunspecDID(inverter_values["c_sunspec_did"])
#                    Domoticz.Log("Inverter type: {}".format(inverter_type))
                    meter_type = solaredge_modbus.sunspecDID(meter_values["c_sunspec_did"])
                    Domoticz.Log("Meter type: {}".format(meter_type))

                    # The plugin currently has 2 supported types.
                    # This may be updated in the future based on user feedback.

#                    if inverter_type == solaredge_modbus.sunspecDID.SINGLE_PHASE_INVERTER:
#                        self._LOOKUP_TABLE = inverter_tables.SINGLE_PHASE_INVERTER
#                    elif inverter_type == solaredge_modbus.sunspecDID.THREE_PHASE_INVERTER:
#                        self._LOOKUP_TABLE = inverter_tables.THREE_PHASE_INVERTER
#                    else:
#                        Domoticz.Log("Unsupported inverter type: {}".format(inverter_type))
#                    self._DEVICE_OFFSET = 50      # for testing purposes only

                    if meter_type == solaredge_modbus.sunspecDID.WYE_THREE_PHASE_METER:
                        self._LOOKUP_TABLE = meter_tables.WYE_THREE_PHASE_METER
                    else:
                        Domoticz.Log("Unsupported meter type: {}".format(meter_type))
                    self._DEVICE_OFFSET = 150      # for testing purposes only

                    if self._LOOKUP_TABLE:

                        # Set the number of samples on all the math objects.

                        for unit in self._LOOKUP_TABLE:
                            if unit[Column.MATH]  and Parameters["Mode4"] == "math_enabled":
                                unit[Column.MATH].set_max_samples(self.max_samples)


                        # We updated some device types over time.
                        # Let's make sure that we have the correct type setup.

                        for unit in self._LOOKUP_TABLE:

                            Domoticz.Log("Updating devices if needed")
                            if (unit[Column.ID] + self._DEVICE_OFFSET) in Devices:
                                device = Devices[unit[Column.ID] + self._DEVICE_OFFSET]

                                Domoticz.Log("Device name: \"{}\"".format(device.Name))

                                if (device.Name != "Meter 1 - " + unit[Column.NAME],
                                    device.Type != unit[Column.TYPE] or
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
                                if (unit[Column.ID] +self._DEVICE_OFFSET) not in Devices:
                                    Domoticz.Device(
                                        Unit=unit[Column.ID] + self._DEVICE_OFFSET,
                                        Name="Meter 1 - " + unit[Column.NAME],
                                        Type=unit[Column.TYPE],
                                        Subtype=unit[Column.SUBTYPE],
                                        Switchtype=unit[Column.SWITCHTYPE],
                                        Options=unit[Column.OPTIONS],
                                        Used=1,
                                    ).Create()
                else:
                    Domoticz.Log("Connection established with: {}:{} Device Address: {}. BUT... inverter returned no information".format(Parameters["Address"], Parameters["Port"], Parameters["Mode3"]))
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
