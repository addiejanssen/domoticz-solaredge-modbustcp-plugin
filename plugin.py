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
<plugin key="SolarEdge_ModbusTCP" name="SolarEdge ModbusTCP" author="Addie Janssen" version="2.0.1" externallink="https://github.com/addiejanssen/domoticz-solaredge-modbustcp-plugin">
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
                <option label="Normal" value="1" default="true" />
                <option label="Verbose" value="2"/>
                <option label="Verbose+" value="3"/>
                <option label="Verbose++" value="4"/>
            </options>
        </param>
    </params>
</plugin>
"""

from inspect import Parameter
import Domoticz
import solaredge_modbus
import json

import inverters
import meters
import batteries

from helpers import DomoLog, LogLevels, SetLogLevel
from datetime import datetime, timedelta
from enum import IntEnum, unique
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
    PREPEND_LOOKUP  = 9
    PREPEND_MATH    = 10
    LOOKUP          = 11
    MATH            = 12


#
# The BasePlugin is the actual Domoticz plugin.
# This is where the fun starts :-)
#

class BasePlugin:

    def __init__(self):

        # The device dictionary will hold an entry for the inverter and each meter and battery (if applicable)
        # For each device, it will mention a name, the actual lookup table and a device index offset

        self.device_dictionary = {}

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

        # Set the logging level

        Domoticz.Log("mode 5 = {}".format(int(Parameters["Mode5"])))
        SetLogLevel(LogLevels(int(Parameters["Mode5"])))

        # Let's go

        DomoLog(LogLevels.ALL, 
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

        self.connectToInverter()


    #
    # OnHeartbeat is called by Domoticz at a specific interval as set in onStart()
    #

    def onHeartbeat(self):
        DomoLog(LogLevels.ALL, "onHeartbeat")

        if self.inverter.connected():

            for device_name, device_details in self.device_dictionary.items():

                if device_details["table"]:

                    values = None

                    if device_details["type"] == "inverter":
                        try:
                            values = self.inverter.read_all()
                        except ConnectionException:
                            values = None
                            DomoLog(LogLevels.NORMAL, "Connection Exception when trying to communicate with: {}:{} Device Address: {}".format(Parameters["Address"], Parameters["Port"], Parameters["Mode3"]))

                    elif device_details["type"] == "meter":
                        try:
                            meter = self.inverter.meters()[device_name]
                            values = meter.read_all()
                        except ConnectionException:
                            values = None
                            DomoLog(LogLevels.NORMAL, "Connection Exception when trying to communicate with: {}:{} Device Address: {}".format(Parameters["Address"], Parameters["Port"], Parameters["Mode3"]))

                    elif device_details["type"] == "battery":
                        try:
                            battery = self.inverter.batteries()[device_name]
                            values = battery.read_all()
                        except ConnectionException:
                            values = None
                            DomoLog(LogLevels.NORMAL, "Connection Exception when trying to communicate with: {}:{} Device Address: {}".format(Parameters["Address"], Parameters["Port"], Parameters["Mode3"]))

                    if values:

                        to_log = values
                        if "c_serialnumber" in to_log:
                            to_log.pop("c_serialnumber")
                        DomoLog(LogLevels.VERBOSE, "device: {} values: {}".format(device_name, json.dumps(to_log, indent=4, sort_keys=False)))

                        self.processValues(device_details, values)
                    else:
                        DomoLog(LogLevels.NORMAL, "Inverter returned no information")

        else:
            self.connectToInverter()

    #
    # Go through the table and update matching devices
    # with the new values.
    #

    def processValues(self, device_details, values):

        if device_details["table"]:
            table = device_details["table"]
            offset = device_details["offset"]

            # Just for cosmetics in the log

            updated = 0
            device_count = 0

            # Now process each unit in the table.

            for unit in table:
                DomoLog(LogLevels.ALL, str(unit))

                # Skip a unit when the matching device got deleted.

                if (unit[Column.ID] + offset) in Devices:
                    DomoLog(LogLevels.ALL, "-> found in Devices")

                    # For certain units the table has a lookup table to replace the value with something else.

                    if unit[Column.LOOKUP]:
                        DomoLog(LogLevels.ALL, "-> looking up...")

                        lookup_table = unit[Column.LOOKUP]
                        to_lookup = int(values[unit[Column.MODBUSNAME]])

                        if to_lookup >= 0 and to_lookup < len(lookup_table):
                            value = lookup_table[to_lookup]
                        else:
                            value = "Key not found in lookup table: {}".format(to_lookup)

                    # When a math object is setup for the unit, update the samples in it and get the calculated value.

                    elif unit[Column.MATH] and Parameters["Mode4"] == "math_enabled":
                        DomoLog(LogLevels.ALL, "-> calculating...")
                        m = unit[Column.MATH]
                        if unit[Column.MODBUSSCALE]:
                            m.update(values[unit[Column.MODBUSNAME]], values[unit[Column.MODBUSSCALE]])
                        else:
                            m.update(values[unit[Column.MODBUSNAME]])

                        value = m.get()

                    # When there is no math object then just store the latest value.
                    # Some values from the inverter need to be scaled before they can be stored.

                    elif unit[Column.MODBUSSCALE]:
                        DomoLog(LogLevels.ALL, "-> scaling...")
                        # we need to do some calculation here
                        value = values[unit[Column.MODBUSNAME]] * (10 ** values[unit[Column.MODBUSSCALE]])

                    # Some values require no action but storing in Domoticz.

                    else:
                        DomoLog(LogLevels.ALL, "-> copying...")
                        value = values[unit[Column.MODBUSNAME]]

                    DomoLog(LogLevels.ALL, "value = {}".format(value))

                    # Time to store the value in Domoticz.
                    # Some devices require multiple values, in which case the plugin will combine those values.
                    # Currently, there is only a need to prepend one value with another.

                    if unit[Column.PREPEND_LOOKUP]:
                        DomoLog(LogLevels.ALL, "-> has prepend lookup")
                        prepend = Devices[unit[Column.PREPEND_LOOKUP] + offset].sValue
                        DomoLog(LogLevels.ALL, "prepend = {}".format(prepend))
                        sValue = unit[Column.FORMAT].format(prepend, value)
                    elif unit[Column.PREPEND_MATH]:
                        DomoLog(LogLevels.ALL, "-> has prepend math")
                        m = unit[Column.PREPEND_MATH]
                        if unit[Column.MODBUSSCALE]:
                            m.update(values[unit[Column.MODBUSNAME]], values[unit[Column.MODBUSSCALE]])
                        else:
                            m.update(values[unit[Column.MODBUSNAME]])
                        prepend = m.get()
                        sValue = unit[Column.FORMAT].format(prepend, value)
                    else:
                        DomoLog(LogLevels.ALL, "-> no prepend")
                        sValue = unit[Column.FORMAT].format(value)

                    DomoLog(LogLevels.ALL, "sValue = {}".format(sValue))

                    # Only store the value in Domoticz when it has changed.
                    # TODO:
                    #   We should not store certain values when the inverter is sleeping.
                    #   That results in a strange graph; it would be better just to skip it then.

                    if sValue != Devices[unit[Column.ID] + offset].sValue:
                        Devices[unit[Column.ID] + offset].Update(nValue=0, sValue=str(sValue), TimedOut=0)
                        updated += 1

                    device_count += 1

                else:
                    DomoLog(LogLevels.ALL, "-> NOT found in Devices")

            DomoLog(LogLevels.NORMAL, "Updated {} values out of {}".format(updated, device_count))
            
    #
    # Connect to the inverter and initialize the lookup tables.
    #
    
    def connectToInverter(self):

        # Do not stress the inverter when it did not respond in the previous attempt to contact it.

        if (self.inverter.connected() == False) and (self.retryafter <= datetime.now()):

            try:
                self.inverter.connect()

            except ConnectionException:

                # There are multiple reasons why this may fail.
                # - Perhaps the ip address or port are incorrect.
                # - The inverter may not be connected to the network,
                # - The inverter may be turned off.
                # - The inverter has a bad hairday....
                # Try again in the future.

                self.inverter.disconnect()
                self.retryafter = datetime.now() + self.retrydelay

                DomoLog(LogLevels.NORMAL, "Connection Exception when trying to connect to: {}:{} Device Address: {}".format(Parameters["Address"], Parameters["Port"], Parameters["Mode3"]))
                DomoLog(LogLevels.NORMAL, "Retrying to connect to inverter after: {}".format(self.retryafter))

            else:
                DomoLog(LogLevels.NORMAL, "Connection established with: {}:{} Device Address: {}".format(Parameters["Address"], Parameters["Port"], Parameters["Mode3"]))

                # Let's get some values from the inverter and
                # figure out the type of the inverter and
                # meters and batteries if there are any

                try:
                    inverter_values = self.inverter.read_all()

                except ConnectionException:
                    self.inverter.disconnect()
                    self.retryafter = datetime.now() + self.retrydelay

                    DomoLog(LogLevels.NORMAL, "Connection Exception when trying to communicate with: {}:{} Device Address: {}".format(Parameters["Address"], Parameters["Port"], Parameters["Mode3"]))
                    DomoLog(LogLevels.NORMAL, "Retrying to communicate with inverter after: {}".format(self.retryafter))

                else:
                    if inverter_values:
                        DomoLog(LogLevels.NORMAL, "Inverter returned information")

                        inverter_type = solaredge_modbus.sunspecDID(inverter_values["c_sunspec_did"])
                        DomoLog(LogLevels.NORMAL, "Inverter type: {}".format(solaredge_modbus.C_SUNSPEC_DID_MAP[str(inverter_type.value)]))

                        device_offset = 0
                        details = {
                            "type": "inverter",
                            "offset": device_offset,
                            "table": None
                        }

                        if inverter_type == solaredge_modbus.sunspecDID.SINGLE_PHASE_INVERTER:
                            details.update({"table": inverters.SINGLE_PHASE_INVERTER})
                        elif inverter_type == solaredge_modbus.sunspecDID.THREE_PHASE_INVERTER:
                            details.update({"table": inverters.THREE_PHASE_INVERTER})
                        else:
                            details.update({"table": inverters.OTHER_INVERTER})
                            DomoLog(LogLevels.NORMAL, "Unsupported inverter type: {}".format(inverter_type))

                        self.device_dictionary["Inverter"] = details
                        self.addUpdateDevices("Inverter")

                        # Let's see if there are any meters attached

                        device_offset = max(inverters.InverterUnit)
                        all_meters = self.inverter.meters()
                        for meter, params in all_meters.items():
                            meter_values = params.read_all()

                            details = {
                                "type": "meter",
                                "offset": device_offset,
                                "table": None
                            }
                            device_offset = device_offset + max(meters.MeterUnit)

                            meter_type = solaredge_modbus.sunspecDID(meter_values["c_sunspec_did"])
                            DomoLog(LogLevels.NORMAL, "Meter type: {}".format(solaredge_modbus.C_SUNSPEC_DID_MAP[str(meter_type.value)]))

                            if meter_type == solaredge_modbus.sunspecDID.SINGLE_PHASE_METER:
                                details.update({"table": meters.SINGLE_PHASE_METER})
                            elif meter_type == solaredge_modbus.sunspecDID.WYE_THREE_PHASE_METER:
                                details.update({"table": meters.WYE_THREE_PHASE_METER})
                            else:
                                details.update({"table": meters.OTHER_METER})
                                DomoLog(LogLevels.NORMAL, "Unsupported meter type: {}".format(meter_type))

                            self.device_dictionary[meter] = details
                            self.addUpdateDevices(meter)


                        # And then look for batteries

                        device_offset = max(inverters.InverterUnit) + (3 * max(meters.MeterUnit))
                        all_batteries = self.inverter.batteries()
                        for battery, params in all_batteries.items():
                            battery_values = params.read_all()

                            details = {
                                "type": "battery",
                                "offset": device_offset,
                                "table": None
                            }
                            device_offset = device_offset + max(batteries.BatteryUnit)

                            battery_type = solaredge_modbus.sunspecDID(battery_values["c_sunspec_did"])
                            DomoLog(LogLevels.NORMAL, "Battery type: {}".format(solaredge_modbus.C_SUNSPEC_DID_MAP[str(battery_type.value)]))

                            DomoLog(LogLevels.NORMAL, "Unsupported battery type: {}".format(battery_type))

#                            self.device_dictionary[battery] = details
#                            self.addUpdateDevices(battery)

                    else:
                        self.inverter.disconnect()
                        self.retryafter = datetime.now() + self.retrydelay

                        DomoLog(LogLevels.NORMAL, "Connection established with: {}:{} Device Address: {}. BUT... inverter returned no information".format(Parameters["Address"], Parameters["Port"], Parameters["Mode3"]))
                        DomoLog(LogLevels.NORMAL, "Retrying to communicate with inverter after: {}".format(self.retryafter))
        else:
            DomoLog(LogLevels.NORMAL, "Retrying to communicate with inverter after: {}".format(self.retryafter))

    #
    # Go through the table and update matching devices
    # with the new values.
    #
    
    def addUpdateDevices(self, device_name):

        if self.device_dictionary[device_name] and self.device_dictionary[device_name]["table"]:

            table = self.device_dictionary[device_name]["table"]
            offset = self.device_dictionary[device_name]["offset"]
            prepend_name = device_name + " - "

            # Set the number of samples on all the math objects.

            for unit in table:
                if unit[Column.MATH]  and Parameters["Mode4"] == "math_enabled":
                    unit[Column.MATH].set_max_samples(self.max_samples)

            # We updated some device types over time.
            # Let's make sure that we have the correct type setup.

            for unit in table:
                if (unit[Column.ID] + offset) in Devices:
                    device = Devices[unit[Column.ID] + offset]
                    if (device.Type != unit[Column.TYPE] or
                        device.SubType != unit[Column.SUBTYPE] or
                        device.SwitchType != unit[Column.SWITCHTYPE] or
                        device.Options != unit[Column.OPTIONS]):

                        DomoLog(LogLevels.NORMAL, "Updating device \"{}\"".format(device.Name))

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
                for unit in table:
                    if (unit[Column.ID] + offset) not in Devices:

                        DomoLog(LogLevels.NORMAL, "Adding device \"{}\"".format(prepend_name + unit[Column.NAME]))

                        Domoticz.Device(
                            Unit=unit[Column.ID] + offset,
                            Name=prepend_name + unit[Column.NAME],
                            Type=unit[Column.TYPE],
                            Subtype=unit[Column.SUBTYPE],
                            Switchtype=unit[Column.SWITCHTYPE],
                            Options=unit[Column.OPTIONS],
                            Used=1,
                        ).Create()

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
