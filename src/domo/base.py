from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import IntEnum
from typing import ClassVar

import Domoticz
from solaredge import Device as SolarEdgeDevice

from .logging import DomoLog, LogLevels


class DeviceType(IntEnum):
    """The main device types used"""

    GENERAL = 243  # 0xF3
    USAGE = 248  # 0xF8


class DeviceSubtype(IntEnum):
    """The subtypes used"""

    NOT_APPLICABLE = -1
    # Applies to GENERAL
    TEMPERATURE = 5
    PERCENTAGE = 6
    VOLTAGE = 8
    TEXT_STATUS = 19
    CURRENT = 23
    ENERGY = 29
    CUSTOM = 31
    MANAGED_COUNTER = 33
    # Applies to USAGE
    ELECTRIC = 1


class DeviceSwitchType(IntEnum):
    """The switch types used"""

    NOT_APPLICABLE = 0
    # Applies to GENERAL - ENERGY
    IMPORTING = 0
    EXPORTING = 4
    # Applies to GENERAL - MANAGED_COUNTER
    ENERGY = 0
    GAS = 1
    WATER = 2
    COUNTER = 3
    ENERGY_GENERATED = 4
    TIME = 5


@dataclass(frozen=True)
class DeviceStaticConfiguration:
    """The Domoticz configuration for a Device"""

    type_id: DeviceType
    subtype_id: DeviceSubtype
    switch_type_id: DeviceSwitchType
    options: dict[str, str]
    format: str
    calculator: type | None


class Device:
    """A Domoticz Device"""

    configuration: ClassVar[DeviceStaticConfiguration]

    id: int
    name: str
    _solaredge_device:SolarEdgeDevice
    _solaredge_primary_register: str
    _solaredge_secondary_register: str|None

    def __init__(self, id:int, name:str, device:SolarEdgeDevice, registers:list[str]) -> None:
        self.id = id
        self.name = name
        self._solaredge_device = device

        self._solaredge_primary_register = registers[0]
        self._solaredge_secondary_register = None
        if len(registers) == 2:
            self._solaredge_secondary_register = registers[1]

        if self.configuration.calculator:
            self._calculator = self.configuration.calculator()
        else:
            self._calculator = None

    def update(self) -> str:

        result:str = ""

        primary = self._solaredge_device.get(self._solaredge_primary_register)
        if self._calculator:
            primary = self._calculator.update(primary)

        secondary = None
        if self._solaredge_secondary_register:
            secondary = self._solaredge_device.get(self._solaredge_secondary_register)
            result = self.configuration.format.format(primary, secondary)
        else: 
            result = self.configuration.format.format(primary)

        return result


    def updateDomoticzValue(self, domoticz_devices: dict[int, Domoticz.Device], now:datetime) -> bool:

        DomoLog(level=LogLevels.DEBUG, message=f"Entered {self.__class__.__name__}.updateDomoticzValue()")
        did_update: bool = False

        if self.id in domoticz_devices:
            sValue: str = self.update()
            last_update: datetime = datetime.strptime(domoticz_devices[self.id].LastUpdate, "%Y-%m-%d %H:%M:%S")
            if sValue != domoticz_devices[self.id].sValue or (now - last_update) >= timedelta(minutes=5):
                DomoLog(level=LogLevels.INFO, message=f" [{self.name}] updating value to [{sValue}]")
                domoticz_devices[self.id].Update(nValue=0, sValue=sValue)
                did_update = True
            else:
                DomoLog(level=LogLevels.INFO, message=f" [{self.name}] value has not changed and last update is too fresh")

        DomoLog(level=LogLevels.DEBUG, message=f"Leaving {self.__class__.__name__}.updateDomoticzValue()")
        return did_update


    def updateDomoticzDevice(self, add_missing_device: bool, domoticz_devices: dict[int, Domoticz.Device]) -> None:

        DomoLog(level=LogLevels.DEBUG, message=f"Entered {self.__class__.__name__}.createDomoticzDevice()")
        DomoLog(level=LogLevels.DEBUG, message=f" For device id [{self.id}] name [{self.name}]")

        if self.id in domoticz_devices:
            domoticz_device: Domoticz.Device = domoticz_devices[self.id]

            DomoLog(level=LogLevels.INFO, message=f"[{self.__class__.__name__}]  Check if device [{domoticz_device.Name}] needs updating")

            if (domoticz_device.Type != self.configuration.type_id or
                domoticz_device.SubType != self.configuration.subtype_id or
                domoticz_device.SwitchType != self.configuration.switch_type_id or
                domoticz_device.Options != self.configuration.options):

                DomoLog(level=LogLevels.INFO, message=f"[{self.__class__.__name__}]   Updating device [{domoticz_device.Name}]")

                nValue = domoticz_device.nValue
                sValue = domoticz_device.sValue

                domoticz_device.Update(
                        Type=self.configuration.type_id,
                        Subtype=self.configuration.subtype_id,
                        Switchtype=self.configuration.switch_type_id,
                        Options=self.configuration.options,
                        nValue=nValue,
                        sValue=sValue
                )
            else:
                DomoLog(level=LogLevels.INFO, message=f"[{self.__class__.__name__}]   No Update needed")

        elif add_missing_device:
            DomoLog(level=LogLevels.INFO, message=f"[{self.__class__.__name__}]  Adding new domoticz device id [{self.id}] name [{self.name}]")

            Domoticz.Device(
                Unit=self.id,
                Name=self.name,
                Type=self.configuration.type_id,
                Subtype=self.configuration.subtype_id,
                Switchtype=self.configuration.switch_type_id,
                Options=self.configuration.options,
                Used=1,
            ).Create()
        else:
            DomoLog(level=LogLevels.INFO, message=f"[{self.__class__.__name__}]  Add missing devices is turned off - skipping device")

        DomoLog(level=LogLevels.DEBUG, message=f"Leaving {self.__class__.__name__}.createDomoticzDevice()")
