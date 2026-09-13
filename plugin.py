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
<plugin key="SolarEdge_ModbusTCP" name="SolarEdge ModbusTCP" author="Addie Janssen" version="1.2.0" externallink="https://github.com/addiejanssen/domoticz-solaredge-modbustcp-plugin">
    <description>
        <h2><br/>SolarEdge ModbusTCP Plugin</h2>
        <p>Version 1.2.0</p>
        <p>Reads data from SolarEdge power inverters over ModbusTCP and creates Domoticz devices for:</p>
        <ul>
            <li>Inverter status and vendor status</li>
            <li>AC/DC current, voltage and power</li>
            <li>Frequency, power factor and temperature</li>
            <li>Energy production (lifetime and daily)</li>
        </ul>
        <br/><span style="font-weight: bold;">Requirements:</span>
        <ul>
            <li>The inverter must be connected to the network (wired or wireless).</li>
            <li>Modbus/TCP must be enabled on the inverter (see inverter documentation).</li>
            <li>Python 3.x and the <i>solaredge_modbus</i> library must be installed.</li>
        </ul>
        <br/><span style="font-weight: bold;">Connection settings</span>
    </description>

    <params>
        <param field="Address" label="Inverter IP Address" width="150px" required="true">
            <description>
                <br/><span style="color: yellow;">IP address or hostname of the SolarEdge inverter.</span>
            </description>
        </param>
        <param field="Port" label="Inverter Port Number" width="100px" required="true" default="502">
            <description>
                <br/><span style="color: yellow;">Modbus TCP port of the inverter (default: 502).</span>
            </description>
        </param>
        <param field="Mode3" label="Inverter Modbus device address" width="100px" required="true" default="1">
            <description>
                <br/><span style="color: yellow;">Modbus unit/slave address of the inverter (default: 1).</span>
            </description>
        </param>
        <param field="Mode1" label="Add missing devices" width="100px" required="true" default="Yes">
            <description>
                <br/>Set to <b>Yes</b> to automatically create devices when the plugin starts.<br/>
                Set to <b>No</b> after manually deleting unused devices to prevent them from being recreated on restart.
            </description>
            <options>
                <option label="Yes" value="Yes" default="true" />
                <option label="No" value="No" />
            </options>
        </param>
        <param field="Mode2" label="Interval" width="100px" required="true" default="5">
            <description>
                <br/>How often the plugin reads data from the inverter.<br/>
                Shorter intervals give more accurate graphs but increase network traffic and inverter load.
            </description>
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
            <description>
                <br/><b>Enabled</b>: Domoticz graphs show averaged (or maximum) values over the 5-minute graph interval.<br/>
                <b>Disabled</b>: Domoticz graphs show the last retrieved value only.
            </description>
            <options>
                <option label="Enabled" value="math_enabled" default="true" />
                <option label="Disabled" value="math_disabled"/>
            </options>
        </param>
        <param field="Mode5" label="Log level" width="100px">
            <description>
                <br/><b>Normal</b>: only errors and status messages are logged.<br/>
                <b>Extra</b>: all values received from the inverter are printed in the log.<br/>
                <b>Debug</b>: full debug output including internal state.
            </description>
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
import inspect
import json
import sys
import traceback
import types

from datetime import datetime, timedelta
from enum import IntEnum, unique
from pymodbus.exceptions import ConnectionException


def _apply_pymodbus_legacy_compat():
    try:
        import pymodbus.constants as pymodbus_constants
    except ImportError:
        return

    if not hasattr(pymodbus_constants, "Endian"):
        class Endian:
            BIG = "big"
            LITTLE = "little"
            Big = "big"
            Little = "little"

        pymodbus_constants.Endian = Endian

    try:
        import pymodbus.payload
    except ImportError:
        from pymodbus.client import ModbusBaseClient

        class BinaryPayloadDecoder:
            def __init__(self, registers, byteorder="big", wordorder="big"):
                self._registers = list(registers)
                self._wordorder = wordorder

            @classmethod
            def fromRegisters(cls, registers, byteorder="big", wordorder="big"):
                return cls(registers, byteorder=byteorder, wordorder=wordorder)

            def _decode(self, data_type, count=1):
                registers = self._registers[:count]
                self._registers = self._registers[count:]
                return ModbusBaseClient.convert_from_registers(
                    registers,
                    data_type,
                    word_order=self._wordorder,
                )

            def decode_16bit_int(self):
                return self._decode(ModbusBaseClient.DATATYPE.INT16)

            def decode_16bit_uint(self):
                return self._decode(ModbusBaseClient.DATATYPE.UINT16)

            def decode_32bit_int(self):
                return self._decode(ModbusBaseClient.DATATYPE.INT32, 2)

            def decode_32bit_uint(self):
                return self._decode(ModbusBaseClient.DATATYPE.UINT32, 2)

            def decode_64bit_uint(self):
                return self._decode(ModbusBaseClient.DATATYPE.UINT64, 4)

            def decode_32bit_float(self):
                return self._decode(ModbusBaseClient.DATATYPE.FLOAT32, 2)

            def decode_string(self, size):
                register_count = (size + 1) // 2
                value = self._decode(ModbusBaseClient.DATATYPE.STRING, register_count)
                return value.encode("utf-8")

            def skip_bytes(self, count):
                register_count = (count + 1) // 2
                self._registers = self._registers[register_count:]

        class BinaryPayloadBuilder:
            def __init__(self, byteorder="big", wordorder="big"):
                self._registers = []
                self._wordorder = wordorder

            def _add(self, value, data_type):
                self._registers.extend(
                    ModbusBaseClient.convert_to_registers(
                        value,
                        data_type,
                        word_order=self._wordorder,
                    )
                )

            def add_16bit_int(self, value):
                self._add(value, ModbusBaseClient.DATATYPE.INT16)

            def add_16bit_uint(self, value):
                self._add(value, ModbusBaseClient.DATATYPE.UINT16)

            def add_32bit_int(self, value):
                self._add(value, ModbusBaseClient.DATATYPE.INT32)

            def add_32bit_uint(self, value):
                self._add(value, ModbusBaseClient.DATATYPE.UINT32)

            def add_64bit_uint(self, value):
                self._add(value, ModbusBaseClient.DATATYPE.UINT64)

            def add_32bit_float(self, value):
                self._add(value, ModbusBaseClient.DATATYPE.FLOAT32)

            def add_string(self, value):
                self._add(value, ModbusBaseClient.DATATYPE.STRING)

            def to_registers(self):
                return self._registers

        payload_module = types.ModuleType("pymodbus.payload")
        payload_module.BinaryPayloadDecoder = BinaryPayloadDecoder
        payload_module.BinaryPayloadBuilder = BinaryPayloadBuilder
        sys.modules["pymodbus.payload"] = payload_module

    try:
        import pymodbus.register_read_message
    except ImportError:
        from pymodbus.pdu.register_message import ReadHoldingRegistersResponse

        register_read_message_module = types.ModuleType("pymodbus.register_read_message")
        register_read_message_module.ReadHoldingRegistersResponse = ReadHoldingRegistersResponse
        sys.modules["pymodbus.register_read_message"] = register_read_message_module

    try:
        from pymodbus.client import ModbusSerialClient, ModbusTcpClient
    except ImportError:
        return

    if "pymodbus.client.sync" not in sys.modules:
        try:
            import pymodbus.client.sync  # noqa: F401  (still exists on some versions)
        except ImportError:
            sync_module = types.ModuleType("pymodbus.client.sync")
            sync_module.ModbusTcpClient = ModbusTcpClient
            sync_module.ModbusSerialClient = ModbusSerialClient
            try:
                from pymodbus.client import ModbusUdpClient
                sync_module.ModbusUdpClient = ModbusUdpClient
            except ImportError:
                pass
            sys.modules["pymodbus.client.sync"] = sync_module

    def _wrap_read_holding_registers(original, uses_device_id):
        def read_holding_registers(self, address, count=1, **kwargs):
            if uses_device_id:
                if "slave" in kwargs and "device_id" not in kwargs:
                    kwargs["device_id"] = kwargs.pop("slave")
                if "unit" in kwargs and "device_id" not in kwargs:
                    kwargs["device_id"] = kwargs.pop("unit")
                kwargs.pop("unit", None)
                kwargs.pop("slave", None)
                result = original(self, address, count=count, **kwargs)
            else:
                result = original(self, address, count, **kwargs)

            try:
                regs = getattr(result, "registers", None)
                Domoticz.Debug(
                    "pymodbus compat: read_holding_registers(address={}, count={}, kwargs={}) -> type={}, isError={}, registers_len={}".format(
                        address, count, kwargs, type(result).__name__,
                        result.isError() if hasattr(result, "isError") else "n/a",
                        len(regs) if regs is not None else "n/a",
                    )
                )
            except Exception:
                pass

            return result

        return read_holding_registers

    def _wrap_write_registers(original, uses_device_id):
        def write_registers(self, address, values, **kwargs):
            if uses_device_id:
                if "slave" in kwargs and "device_id" not in kwargs:
                    kwargs["device_id"] = kwargs.pop("slave")
                if "unit" in kwargs and "device_id" not in kwargs:
                    kwargs["device_id"] = kwargs.pop("unit")
                kwargs.pop("unit", None)
                kwargs.pop("slave", None)
            return original(self, address, values, **kwargs)

        return write_registers

    for client_cls in (ModbusTcpClient, ModbusSerialClient):
        if not getattr(client_cls, "_solaredge_legacy_api", False):
            uses_device_id = "device_id" in inspect.signature(client_cls.read_holding_registers).parameters
            client_cls.read_holding_registers = _wrap_read_holding_registers(
                client_cls.read_holding_registers,
                uses_device_id,
            )
            client_cls.write_registers = _wrap_write_registers(
                client_cls.write_registers,
                uses_device_id,
            )
            client_cls._solaredge_legacy_api = True

    if not getattr(ModbusSerialClient, "_solaredge_legacy_init", False):
        original_serial_init = ModbusSerialClient.__init__
        accepts_method = "method" in inspect.signature(original_serial_init).parameters

        if not accepts_method:
            def serial_init(self, *args, **kwargs):
                kwargs.pop("method", None)
                original_serial_init(self, *args, **kwargs)

            ModbusSerialClient.__init__ = serial_init

        ModbusSerialClient._solaredge_legacy_init = True


_apply_pymodbus_legacy_compat()

import solaredge_modbus

#
# Domoticz shows graphs with intervals of 5 minutes.
# When collecting information from the inverter more frequently than that, then it makes no sense to only show the last value.
#
# The Average class can be used to calculate the average value based on a sliding window of samples.
# The number of samples stored depends on the interval used to collect the value from the inverter itself.
#

class SlidingWindow:

    def __init__(self):
        self.samples = []
        self.max_samples = 30

    def set_max_samples(self, count):
        self.max_samples = count
        if self.max_samples < 1:
            self.max_samples = 1

    def update(self, new_value, scale=0):
        self.samples.append(new_value * (10 ** scale))
        self.samples = self.samples[-self.max_samples:]

        Domoticz.Debug("{}: {} - {} values".format(self.__class__.__name__, self.get(), len(self.samples)))

    def get(self):
        raise NotImplementedError


class Average(SlidingWindow):

    def get(self):
        if not self.samples:
            return 0
        return sum(self.samples) / len(self.samples)

#
# Domoticz shows graphs with intervals of 5 minutes.
# When collecting information from the inverter more frequently than that, then it makes no sense to only show the last value.
#
# The Maximum class can be used to calculate the highest value based on a sliding window of samples.
# The number of samples stored depends on the interval used to collect the value from the inverter itself.
#

class Maximum(SlidingWindow):

    def get(self):
        if not self.samples:
            return 0
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
    [Unit.L1_CURRENT,      "L1 Current",        0xF3,  0x17,     0x00,       {},                     "l1_current",      "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.L1_VOLTAGE,      "L1 Voltage",        0xF3,  0x08,     0x00,       {},                     "l1_voltage",      "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.L1N_VOLTAGE,     "L1-N Voltage",      0xF3,  0x08,     0x00,       {},                     "l1n_voltage",     "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_AC,        "Power",             0xF8,  0x01,     0x00,       {},                     "power_ac",        "power_ac_scale",       "{:.2f}",  None,           None,                                  Average() ],
    [Unit.FREQUENCY,       "Frequency",         0xF3,  0x1F,     0x00,       { "Custom": "1;Hz"  },  "frequency",       "frequency_scale",      "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_APPARENT,  "Power (Apparent)",  0xF3,  0x1F,     0x00,       { "Custom": "1;VA"  },  "power_apparent",  "power_apparent_scale", "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_REACTIVE,  "Power (Reactive)",  0xF3,  0x1F,     0x00,       { "Custom": "1;VAr" },  "power_reactive",  "power_reactive_scale", "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_FACTOR,    "Power Factor",      0xF3,  0x06,     0x00,       {},                     "power_factor",    "power_factor_scale",   "{:.2f}",  None,           None,                                  Average() ],
    [Unit.ENERGY_TOTAL,    "Total Energy",      0xF3,  0x1D,     0x04,       {},                     "energy_total",    "energy_total_scale",   "{};{}",   Unit.POWER_AC,  None,                                  None      ],
    [Unit.CURRENT_DC,      "DC Current",        0xF3,  0x17,     0x00,       {},                     "current_dc",      "current_dc_scale",     "{:.2f}",  None,           None,                                  Average() ],
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
    [Unit.L1_CURRENT,      "L1 Current",        0xF3,  0x17,     0x00,       {},                     "l1_current",      "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.L2_CURRENT,      "L2 Current",        0xF3,  0x17,     0x00,       {},                     "l2_current",      "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.L3_CURRENT,      "L3 Current",        0xF3,  0x17,     0x00,       {},                     "l3_current",      "current_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.L1_VOLTAGE,      "L1 Voltage",        0xF3,  0x08,     0x00,       {},                     "l1_voltage",      "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.L2_VOLTAGE,      "L2 Voltage",        0xF3,  0x08,     0x00,       {},                     "l2_voltage",      "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.L3_VOLTAGE,      "L3 Voltage",        0xF3,  0x08,     0x00,       {},                     "l3_voltage",      "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.L1N_VOLTAGE,     "L1-N Voltage",      0xF3,  0x08,     0x00,       {},                     "l1n_voltage",     "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.L2N_VOLTAGE,     "L2-N Voltage",      0xF3,  0x08,     0x00,       {},                     "l2n_voltage",     "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.L3N_VOLTAGE,     "L3-N Voltage",      0xF3,  0x08,     0x00,       {},                     "l3n_voltage",     "voltage_scale",        "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_AC,        "Power",             0xF8,  0x01,     0x00,       {},                     "power_ac",        "power_ac_scale",       "{:.2f}",  None,           None,                                  Average() ],
    [Unit.FREQUENCY,       "Frequency",         0xF3,  0x1F,     0x00,       { "Custom": "1;Hz"  },  "frequency",       "frequency_scale",      "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_APPARENT,  "Power (Apparent)",  0xF3,  0x1F,     0x00,       { "Custom": "1;VA"  },  "power_apparent",  "power_apparent_scale", "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_REACTIVE,  "Power (Reactive)",  0xF3,  0x1F,     0x00,       { "Custom": "1;VAr" },  "power_reactive",  "power_reactive_scale", "{:.2f}",  None,           None,                                  Average() ],
    [Unit.POWER_FACTOR,    "Power Factor",      0xF3,  0x06,     0x00,       {},                     "power_factor",    "power_factor_scale",   "{:.2f}",  None,           None,                                  Average() ],
    [Unit.ENERGY_TOTAL,    "Total Energy",      0xF3,  0x1D,     0x04,       {},                     "energy_total",    "energy_total_scale",   "{};{}",   Unit.POWER_AC,  None,                                  None      ],
    [Unit.CURRENT_DC,      "DC Current",        0xF3,  0x17,     0x00,       {},                     "current_dc",      "current_dc_scale",     "{:.2f}",  None,           None,                                  Average() ],
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

        # The Domoticz image ID for the SolarEdge icon.

        self.imageID = 0

        # When there is an issue contacting the inverter, the plugin will retry after a certain retry delay.
        # The actual time after which the plugin will try again is stored in the retry after variable.
        # According to the documenation, the inverter may need up to 2 minutes to "reset".

        self.retrydelay = timedelta(minutes = 2)
        self.retryafter = datetime.now() - timedelta(seconds = 1)

    #
    # onStart is called by Domoticz to start the processing of the plugin.
    #

    def onStart(self):

        self.add_devices = Parameters["Mode1"] == "Yes"

        _IMAGE = "solaredge"
        creating_new_icon = _IMAGE not in Images
        Domoticz.Image(f"{_IMAGE}.zip").Create()

        if _IMAGE in Images:
            self.imageID = Images[_IMAGE].ID
            if creating_new_icon:
                Domoticz.Log("Icons created and loaded.")
            else:
                Domoticz.Log(f"Icons found in database (ImageID={self.imageID}).")
        else:
            Domoticz.Error(f"Unable to load icon pack '{_IMAGE}.zip'")


        # Domoticz will generate graphs showing an interval of 5 minutes.
        # Calculate the number of samples to store over a period of 5 minutes.

        self.max_samples = 300 // int(Parameters["Mode2"])

        # Now set the interval at which the information is collected accordingly.

        Domoticz.Heartbeat(int(Parameters["Mode2"]))

        if "Mode5" in Parameters and Parameters["Mode5"] == "Debug":
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
            port=int(Parameters["Port"]),
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

            inverter_values = None
            try:
                inverter_values = self.readInverterValues()
            except ConnectionException as e:
                inverter_values = None
                self._LOOKUP_TABLE = None
                self.retryafter = datetime.now() + self.retrydelay
                self.disconnectInverter()
                Domoticz.Error("ConnectionException: {}; retrying after: {}".format(e, self.retryafter))
            else:

                if inverter_values:

                    if "Mode5" in Parameters and (Parameters["Mode5"] == "Extra" or Parameters["Mode5"] == "Debug"):
                        to_log = dict(inverter_values)
                        if "c_serialnumber" in to_log:
                            to_log.pop("c_serialnumber")
                        Domoticz.Log("inverter values: {}".format(json.dumps(to_log, indent=4, sort_keys=False)))

                    # Just for cosmetics in the log

                    updated = 0
                    device_count = 0
                    missing_keys = []

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
                                try:
                                    to_lookup = int(inverter_values[unit[Column.MODBUSNAME]])
                                except KeyError as e:
                                    to_lookup = -1
                                    missing_keys.append(str(e))
                                    continue #data is missing, skip this device

                                if to_lookup >= 0 and to_lookup < len(lookup_table):
                                    value = lookup_table[to_lookup]
                                else:
                                    value = "Key not found in lookup table: {}".format(to_lookup)

                            # When a math object is setup for the unit, update the samples in it and get the calculated value.

                            elif unit[Column.MATH] and Parameters["Mode4"] == "math_enabled":
                                Domoticz.Debug("-> calculating...")
                                m = unit[Column.MATH]
                                try:
                                    if unit[Column.MODBUSSCALE]:
                                        m.update(inverter_values[unit[Column.MODBUSNAME]], inverter_values[unit[Column.MODBUSSCALE]])
                                    else:
                                        m.update(inverter_values[unit[Column.MODBUSNAME]])

                                    value = m.get()
                                except KeyError as e:
                                    missing_keys.append(str(e))
                                    continue
                                    
                            # When there is no math object then just store the latest value.
                            # Some values from the inverter need to be scaled before they can be stored.

                            elif unit[Column.MODBUSSCALE]:
                                Domoticz.Debug("-> scaling...")
                                # we need to do some calculation here
                                try:
                                    value = inverter_values[unit[Column.MODBUSNAME]] * (10 ** inverter_values[unit[Column.MODBUSSCALE]])
                                except KeyError as e:
                                    missing_keys.append(str(e))
                                    continue

                            # Some values require no action but storing in Domoticz.

                            else:
                                Domoticz.Debug("-> copying...")
                                try:
                                    value = inverter_values[unit[Column.MODBUSNAME]]
                                except KeyError as e:
                                    missing_keys.append(str(e))
                                    continue

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

                    if missing_keys:
                        Domoticz.Error(
                            "Inverter returned incomplete data; {} field(s) missing: {}. "
                            "This can happen when the inverter is sleeping (e.g. at night) or when there is a communication issue.".format(
                                len(missing_keys), ", ".join(missing_keys)
                            )
                        )

                    if "Mode5" in Parameters and Parameters["Mode5"] == "Extra":
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
                inverter_values = self.readInverterValues()
            except ConnectionException as e:

                # There are multiple reasons why this may fail.
                # - Perhaps the ip address or port are incorrect.
                # - The inverter may not be connected to the networ,
                # - The inverter may be turned off.
                # - The inverter has a bad hairday....
                # Try again in the future.

                self.retryafter = datetime.now() + self.retrydelay
                inverter_values = None
                self.disconnectInverter()

                Domoticz.Log("Connection Exception when trying to contact: {}:{} Device Address: {} ({})".format(Parameters["Address"], Parameters["Port"], Parameters["Mode3"], e))
                Domoticz.Log("Retrying to communicate with inverter after: {}".format(self.retryafter))
                return

            else:

                if inverter_values:
                    Domoticz.Log("Connection established with: {}:{} Device Address: {}".format(Parameters["Address"], Parameters["Port"], Parameters["Mode3"]))
                    Domoticz.Debug("inverter_values = '" +format(inverter_values)+"'")

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
                            if unit[Column.MATH] and Parameters["Mode4"] == "math_enabled":
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
                                        Image=self.imageID
                                    ).Create()
                else:
                    Domoticz.Log("Connection established with: {}:{} Device Address: {}. BUT... inverter returned no information".format(Parameters["Address"], Parameters["Port"], Parameters["Mode3"]))
                    self.retryafter = datetime.now() + self.retrydelay
                    Domoticz.Log("Retrying to communicate with inverter after: {}".format(self.retryafter))
                    Domoticz.Debug("inverter_values = '" +format(inverter_values)+"'")
        else:
            Domoticz.Log("Retrying to communicate with inverter after: {}".format(self.retryafter))

    def readInverterValues(self):
        try:
            return self.inverter.read_all()
        except ConnectionException as first_error:
            Domoticz.Debug("ConnectionException during read_all; reconnecting once before retry: {}".format(first_error))
            self.disconnectInverter()
            try:
                values = self.inverter.read_all()
            except ConnectionException:
                raise
            else:
                Domoticz.Log("Recovered Modbus TCP connection after reconnect.")
                return values


    #
    # onStop is called by Domoticz when the plugin is stopped.
    #

    def onStop(self):
        Domoticz.Debug("onStop")
        self.disconnectInverter()

    def disconnectInverter(self):
        try:
            if self.inverter and self.inverter.client:
                self.inverter.client.close()
        except Exception as e:
            Domoticz.Debug("disconnectInverter: {}".format(e))


#
# Instantiate the plugin and register the supported callbacks.
#

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()
