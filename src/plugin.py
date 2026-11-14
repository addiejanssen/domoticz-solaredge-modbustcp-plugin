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
<plugin key="SolarEdge_ModbusTCP-DEV" name="SolarEdge ModbusTCP-DEV" author="Addie Janssen" version="3.0.0-dev.3">
    <description>
        <hr/>
        <h2>SolarEdge ModbusTCP Plugin</h2>
        <hr/>
        <p>
            This plugin allows reading data from a SolarEdge inverter using the Modbus protocol over the local (wired or wireless) network.
        </p>
        <p>
            More information can be found in the GitHub wiki:
            <a href="https://github.com/addiejanssen/domoticz-solaredge-modbustcp-plugin/wiki/" target="_blank">
                https://github.com/addiejanssen/domoticz-solaredge-modbustcp-plugin/wiki/
            </a>
        </p>
        <p>
            Questions and feedback can be discussed on this Domoticz forum post:
            <a href="https://forum.domoticz.com/viewtopic.php?t=34039" target="_blank">
                https://forum.domoticz.com/viewtopic.php?t=34039
            </a>
        </p>

        <h3>Security warning</h3>
        <p>
            Connecting a SolarEdge inverter to your network and enabling Modbus on it, allows anyone that has
            access to your network to interact with the inverter.
            The SolarEdge Modbus protocols do not support any kind of authentication or authorization and as such,
            anyone with access to the network is also going to be able change settings!
        </p>
        <p>
            Here's some advise:
            <ul>
                <li>Don't allow access to your inverter from the internet.</li>
                <li>If possible, use a trusted LAN or VLAN.</li>
            </ul>
        </p>
        <hr/>
    </description>

    <params>
        <param field="Address" label="Inverter IP Address" width="150px" required="true">
            <description>IP address or hostname of your SolarEdge inverter.</description>
        </param>

        <param field="Port" label="Inverter Port Number" width="150px" required="true" default="502" type="number">
            <description>The Modbus port as configured on the inverter. Common values are 502 and 1502.</description>
        </param>

        <param field="Mode3" label="Inverter Modbus device address" width="150px" required="true" default="1" type="number">
            <description>The Modbus device id assigned to the inverter. Default is 1.</description>
        </param>

        <param field="Mode1" label="Add missing devices" width="150px" required="true" default="Yes">
            <description>
                By default, the plugin will add a device to Domoticz for each measurable item the inverter supports.
                When, manually, deleting a device from Domoticz, the device will be recreated again on the next start of the plugin.
                When this setting is turned off, the plugin will not add any device that is missing from Domoticz when it starts.
            </description>
            <options>
                <option label="Yes" value="Yes" default="true" />
                <option label="No"  value="No"                 />
            </options>
        </param>

        <param field="Mode2" label="Interval" width="150px" required="true" default="5">
            <description>
                The interval at which the plugin will retrieve information from the inverter.
                Short intervals will provide frequent updates of the information.
                However, it also introduces load on both the inverter and Domoticz.
                Only use short intervals when, visually, monitoring the values.
                If you only look at the Domoticz graphs every now and then, than use a longer interval period.
                Long interval periods have no major impact on the graphs, as Domoticz only stores information in steps of 5 minutes.
            </description>
            <options>
                <option label="1  second"  value="1"                />
                <option label="2  seconds" value="2"                />
                <option label="3  seconds" value="3"                />
                <option label="4  seconds" value="4"                />
                <option label="5  seconds" value="5" default="true" />
                <option label="10 seconds" value="10"               />
                <option label="20 seconds" value="20"               />
                <option label="30 seconds" value="30"               />
                <option label="60 seconds" value="60"               />
            </options>
        </param>

        <param field="Mode5" label="Log level" width="150px">
            <description>
                Defines which and how much information is logged by the plugin. In general "Normal" will do.
                "Info" will already produce a lot of additional information.
                And "Debug" adds a lot more, mainly technical, information.
            </description>
            <options>
                <option label="Normal" value="0" default="true" />
                <option label="Info"   value="1"                />
                <option label="Debug"  value="2"                />
            </options>
        </param>
    </params>
</plugin>
"""

#
# Instantiate the plugin and register the supported callbacks.
#

from base import SolarEdgeModbusPlugin

_plugin = SolarEdgeModbusPlugin()

def onStart() -> None:
    _plugin.onStart(parameters=Parameters, devices=Devices)

def onHeartbeat() -> None:
    _plugin.onHeartbeat()

def onStop() -> None:
    _plugin.onStop()
