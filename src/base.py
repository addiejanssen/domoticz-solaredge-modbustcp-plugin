"""
This is where the actual work of the SolarEdge ModbusTCP plugin is done.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta

import mapper
from domo import Device as DomoDevice
from domo.logging import DomoLog, LogLevels, SetLogLevel
from Domoticz import Device as DomoticzDevice
from Domoticz import Heartbeat as DomoticzHeartbeat
from pymodbus.exceptions import ConnectionException
from solaredge import Device as SolarEdgeDevice
from solaredge import SolarEdge


@dataclass
class PluginDeviceDetails:
    """
    This class holds the details of the devices as reported by the inverter
    and the matching devices in Domoticz.
    """

    mapper_device_type: mapper.DeviceTypeMapping
    solaredge_device: SolarEdgeDevice
    domoticz_unit_name: str
    domoticz_unit_offset: int
    domoticz_devices: dict[int, DomoDevice]


class SolarEdgeModbusPlugin:
    """This is where all the hard work of the Domoticz plugin is done"""

    def __init__(self) -> None:
        # This is the solaredge_modbus Inverter object that will be used to communicate with the inverter.
        self._inverter: SolarEdge | None = None
        self._inverter_address: str = ""
        self._inverter_port: int = -1
        self._inverter_device_id: int = -1

        # When there is an issue contacting the inverter, the plugin will retry after a certain retry delay.
        # The actual time after which the plugin will try again is stored in the retry after variable.
        # According to the documentation, the inverter may need up to 2 minutes to "reset".
        self.retry_delay: timedelta = timedelta(minutes=2)
        self.retry_after: datetime = datetime.now() - timedelta(seconds=1)

        # The device dictionary will hold an entry for the SunSpec devices and batteries (if applicable).
        self.device_dictionary: dict[str, PluginDeviceDetails] = {}

        # Whether the plugin should add missing devices.
        # If set to True, a deleted device will be added on the next restart of Domoticz.
        self._add_devices = False

    def onStart(self, parameters: dict[str, object], devices: dict[int, DomoticzDevice]) -> None:
        # onStart is called by Domoticz to start the processing of the plugin.

        DomoLog(level=LogLevels.DEBUG, message="Entered onStart()")

        self._domoticz_parameters: dict[str, object] = parameters
        self._domoticz_devices: dict[int, DomoticzDevice] = devices

        # Get the choices of the user and turn them into something we can use

        # Mode 1 defines if we should add missing devices or not
        if self._domoticz_parameters["Mode1"] == "Yes":
            self._add_devices = True
        else:
            self._add_devices = False

        # Now set the interval at which the information is collected accordingly.
        DomoticzHeartbeat(int(self._domoticz_parameters["Mode2"]))

        # Set the logging level
        # Version 1.x.x of the plugin used text values for Mode5 to define the logging level.
        # Version 2.x.x of the plugin uses integer values for Mode5 to define the logging level.
        # The following code will check if the user is using the old or new version and set the logging level accordingly.
        # The old version will be removed in a future release.

        if "Mode5" in self._domoticz_parameters:
            match self._domoticz_parameters["Mode5"]:
                case "Normal":
                    SetLogLevel(level=LogLevels.NORMAL)
                case "Extra":
                    SetLogLevel(level=LogLevels.INFO)
                case "Debug":
                    SetLogLevel(level=LogLevels.DEBUG)
                case _:
                    SetLogLevel(level=LogLevels(value=int(self._domoticz_parameters["Mode5"])))

        # Lets get in touch with the inverter.

        self._inverter_address = self._domoticz_parameters["Address"]
        self._inverter_port = self._domoticz_parameters["Port"]
        self._inverter_device_id = int(self._domoticz_parameters["Mode3"])
        self._inverter = SolarEdge(hostname=self._inverter_address, port_number=self._inverter_port, timeout=15)

        self.connectToInverter()

        DomoLog(level=LogLevels.DEBUG, message="Leaving onStart()")

    def onStop(self) -> None:
        # onStop is called by Domoticz to stop the processing of the plugin.

        DomoLog(level=LogLevels.DEBUG, message="Entered onStop()")

        if self._inverter:
            self._inverter.disconnect()
            DomoLog(
                level=LogLevels.NORMAL,
                message=f"Disconnected from: {self._inverter_address}:{self._inverter_port} Device Address: {self._inverter_device_id}",
            )

        DomoLog(level=LogLevels.DEBUG, message="Leaving onStop()")

    def onHeartbeat(self) -> None:
        # OnHeartbeat is called by Domoticz at a specific interval as set in onStart()

        DomoLog(level=LogLevels.DEBUG, message="Entered onHeartbeat()")

        if len(self.device_dictionary) > 0:
            DomoLog(level=LogLevels.INFO, message=f"We have {len(self.device_dictionary)} devices")

            now: datetime = datetime.now()

            update_count: int = 0

            for plugin_device_name in self.device_dictionary:
                details: PluginDeviceDetails = self.device_dictionary[plugin_device_name]

                DomoLog(level=LogLevels.INFO, message=f"Start processing [{plugin_device_name}]")

                # Contact the inverter and get the data for this SolarEdge device
                try:
                    details.solaredge_device.read()

                    for device_key in details.domoticz_devices:
                        device: DomoDevice = details.domoticz_devices[device_key]
                        if device.updateDomoticzValue(domoticz_devices=self._domoticz_devices, now=now):
                            update_count += 1

                except Exception as exc:
                    DomoLog(level=LogLevels.DEBUG, message=f"Exception while reading [{plugin_device_name}]")
                    DomoLog(level=LogLevels.DEBUG, message=f"{exc}")
                    DomoLog(level=LogLevels.DEBUG, message="Skipping this device and moving on")

                DomoLog(level=LogLevels.INFO, message=f"Finished processing [{plugin_device_name}]")

            DomoLog(level=LogLevels.NORMAL, message=f"Updated [{update_count}] values.")
        else:
            DomoLog(level=LogLevels.NORMAL, message=f"Nothing to do - we have 0 devices")

        DomoLog(level=LogLevels.DEBUG, message="Leaving onHeartbeat()")

    def connectToInverter(self) -> None:
        # (Try to) connect to the inverter and figure out which devices it represents.

        DomoLog(level=LogLevels.DEBUG, message="Entered connectToInverter()")

        # Do not stress the inverter when it did not respond in the previous attempt to contact it.
        if self._inverter and not self._inverter.connected and self.retry_after <= datetime.now():
            DomoLog(
                level=LogLevels.NORMAL,
                message=f"Connection established with: {self._inverter_address}:{self._inverter_port} Device Address: {self._inverter_device_id}",
            )

            devices: list[SolarEdgeDevice] | None = None

            try:
                devices = self._inverter.scan(device_id=self._inverter_device_id)

            except ConnectionException:
                self.retry_after = datetime.now() + self.retry_delay

                DomoLog(
                    level=LogLevels.NORMAL,
                    message=f"Connection Exception when trying to communicate with: {self._inverter_address}:{self._inverter_port} Device Address: {self._inverter_device_id}",
                )
                DomoLog(level=LogLevels.NORMAL, message=f"Retrying to communicate with inverter after: {self.retry_after}")

            else:
                if devices:
                    DomoLog(level=LogLevels.NORMAL, message="Inverter returned device information")

                    inverter_count: int = 0
                    meter_count: int = 0
                    battery_count: int = 0

                    for device in devices:
                        domoticz_devices: dict[int, DomoDevice] = {}

                        mapper_device_type: mapper.DeviceTypeMapping
                        domoticz_unit_name: str = ""
                        domoticz_unit_offset: int = -1

                        mapping: mapper.DeviceMapping | None = None

                        DomoLog(level=LogLevels.NORMAL, message=f"Found [{device.device_description.label}]")

                        map_details: mapper.MapDetails | None = mapper.Map(solaredge_device=device)
                        if map_details:
                            mapping = map_details.mapping
                            domoticz_unit_name = map_details.device_type.value

                            mapper_device_type = map_details.device_type

                            match mapper_device_type:
                                case mapper.DeviceTypeMapping.INVERTER:
                                    if inverter_count < map_details.max_devices:
                                        domoticz_unit_offset = map_details.start_offset * (inverter_count * map_details.max_offset)
                                        inverter_count += 1

                                case mapper.DeviceTypeMapping.METER:
                                    if meter_count < map_details.max_devices:
                                        domoticz_unit_offset = map_details.start_offset * (meter_count * map_details.max_offset)
                                        meter_count += 1
                                        domoticz_unit_name = f"{map_details.device_type.value}_{meter_count}"

                                case mapper.DeviceTypeMapping.BATTERY:
                                    if battery_count < map_details.max_devices:
                                        domoticz_unit_offset = map_details.start_offset * (battery_count * map_details.max_offset)
                                        battery_count += 1
                                        domoticz_unit_name = f"{map_details.device_type.value}_{battery_count}"

                        if domoticz_unit_offset > -1 and mapping:
                            DomoLog(level=LogLevels.INFO, message=f"Found a [{mapper_device_type.value}]")

                            for unit_id in mapping:
                                unit_name, domo_type, registers = mapping[unit_id]
                                domo_device = domo_type(id=domoticz_unit_offset + unit_id, name=unit_name, device=device, registers=registers)

                                DomoLog(level=LogLevels.INFO, message=f" Found [{unit_name}]")
                                domo_device.updateDomoticzDevice(self._add_devices, self._domoticz_devices)
                                domoticz_devices[domo_device.id] = domo_device

                            details = PluginDeviceDetails(
                                mapper_device_type=mapper_device_type,
                                solaredge_device=device,
                                domoticz_unit_name=domoticz_unit_name,
                                domoticz_unit_offset=domoticz_unit_offset,
                                domoticz_devices=domoticz_devices,
                            )

                            self.device_dictionary[details.domoticz_unit_name] = details
                else:
                    self.retry_after = datetime.now() + self.retry_delay

                    DomoLog(
                        level=LogLevels.NORMAL,
                        message=f"Connection established with: {self._inverter_address}:{self._inverter_port} Device Address: {self._inverter_device_id}. BUT... inverter returned no devices",
                    )
                    DomoLog(level=LogLevels.NORMAL, message=f"Retrying to communicate with inverter after: {self.retry_after}")
        else:
            DomoLog(level=LogLevels.NORMAL, message=f"Retrying to communicate with inverter after: {self.retry_after}")

        DomoLog(level=LogLevels.DEBUG, message="Leaving connectToInverter()")
