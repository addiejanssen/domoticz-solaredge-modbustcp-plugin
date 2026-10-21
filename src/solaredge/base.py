from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum
from typing import Any, ClassVar, TypeAlias

from pymodbus import ModbusException
from pymodbus.client import ModbusTcpClient
from pymodbus.pdu import ModbusPDU

ModbusDataType: TypeAlias = ModbusTcpClient.DATATYPE


class ModbusWordOrder(StrEnum):
    """Some registers use Big Endian other Little Endian"""

    BIG = "big"
    LITTLE = "little"


@dataclass(frozen=True)
class RegisterMapEntry:
    """
    A Device can have multiple properties.
    The DeviceProperties class describes a single property.
    """

    offset: int  # Required: Offset within the Modbus registers where the property is stored
    size: int  # Required: The size (in terms of Modbus registers) of the property
    word_order: ModbusWordOrder  # Required: If the value consists of multiple words, this defines the order of the individual words
    register_type: ModbusDataType  # Required: Defines the type of the value (in the Modbus registers)
    python_type: type  # Required: The Python type the value will be translated into
    scaling_item_id: str  # Optional: Defines id of the property to use as a scaling factor for the value of this property
    description: str  # Optional: A description of the property


RegisterMap: TypeAlias = dict[str, RegisterMapEntry]


@dataclass(frozen=True)
class DeviceDescription:
    """Human readable description of the device"""

    id: int
    name: str
    label: str
    description: str


class Device:
    """
    The Device class represents an actual device.
    This can be a SunSpec device (like an inverter or meter) or a Vendor device (like a battery).
    """

    device_description: ClassVar[DeviceDescription] = DeviceDescription(id=-1, name="", label="", description="")

    register_count: ClassVar[int] = 0
    register_map: ClassVar[RegisterMap] = {}

    def __init__(self, inverter: SolarEdge, device_id: int, address: int) -> None:
        self._inverter: SolarEdge = inverter
        self._device_id: int = device_id
        self._address: int = address
        self._registers: list[int] = []

    def read(self) -> list[int]:
        """Read one or more holding registers from a Modbus server"""
        self._registers = self._inverter.read(address=self._address, count=self.register_count, device_id=self._device_id)
        return self._registers

    def get(self, key: str) -> int | float | str | list[bool] | list[int] | list[float] | None:
        """Extracts a value from a list of Modbus registers"""
        target_value = None

        if self._registers and key in self.register_map.keys():
            map_entry: RegisterMapEntry = self.register_map[key]
            registers: list[int] = self._registers[map_entry.offset : map_entry.offset + map_entry.size]

            try:
                converted_value = ModbusTcpClient.convert_from_registers(
                    registers=registers, data_type=map_entry.register_type, word_order=map_entry.word_order.value
                )

            # Based on testing and feedback, we found that inverters may return invalid
            # strings which will result in a UnicodeDecodeError during the conversion.

            except UnicodeDecodeError:
                converted_value = ""

            target_value = converted_value
            if map_entry.python_type:
                target_value = map_entry.python_type(converted_value)
                if isinstance(target_value, IntEnum):
                    target_value = target_value.name

            if target_value is not None and map_entry.scaling_item_id:
                scale_factor = self.get(map_entry.scaling_item_id)

                if scale_factor is not None and isinstance(scale_factor, int):
                    target_value *= 10**scale_factor
                else:
                    target_value = None

        return target_value

    def dump(self)-> dict[str, Any]:
        """Export all the information of the Device to json"""
        result: dict[str, Any] = {}

        result["type"] = self.__class__.__name__

        if self.device_description.id >= 0:
            result["description"] = self.device_description

        self.read()
        key_value: dict[str, Any] = {}
        for key in self.register_map.keys():
            key_value[key] = {
                "description": self.register_map[key].description,
                "value": self.get(key)
            }
        result["data"] = key_value

        return result        


class SolarEdge:
    """
    This class contains the SolarEdge specific functionality.
    """

    #
    # We found that reading too many modbus registers in one go could result in issues.
    # The current implementation has a static maximum of registers.
    #
    # TODO:
    # Consider an approach where we make sure that we don't do a partial read of a register.
    # This can be done by looking at the register_map.
    # However, the register_map lives in Device, not in SolarEdge.
    #
    _modbus_chunk_size: ClassVar[int] = 64

    def __init__(self, hostname: str, port_number: int, timeout: int = 5) -> None:

        self._modbus_hostname: str = hostname
        self._modbus_port_number: int = port_number
        self._modbus_timeout: int = timeout

        self._modbus_device_id: int = -1

        self._modbus_client: ModbusTcpClient = ModbusTcpClient(
            host=self._modbus_hostname, port=self._modbus_port_number, timeout=self._modbus_timeout
        )

    def connect(self) -> bool:
        """Connect to the inverter and return if successful"""
        return self._modbus_client.connect()

    def disconnect(self) -> None:
        """Close the connection with the inverter"""
        self._modbus_client.close()

    def read(self, address: int, count: int, device_id: int) -> list[int]:
        """Read one or more holding registers from a Modbus server"""
        result: list[int] = []
        start: int = address
        end: int = address + count
        read_now: int

        # read_holding_registers only allows 125 registers in one go
        # we need to loop if we have more to read than that

        while start < end:
            if end - start > self._modbus_chunk_size:
                read_now = self._modbus_chunk_size
            else:
                read_now = end - start

            try:
                self._modbus_client.connect()
                rr: ModbusPDU = self._modbus_client.read_holding_registers(address=start, count=read_now, device_id=device_id)
            except ModbusException as exc:
                print(f"Received ModbusException({exc}) from library")
                return []
            if rr.isError():
                print(f"Received exception from device ({rr})")
                return []

            if len(rr.registers) != read_now:
                print(f"expected [{read_now}] got [{len(rr.registers)}]")

            start += read_now
            result.extend(rr.registers)

        return result

    def scan(self, device_id: int) -> list[Device]:
        """This is where the actual scanning happens"""
        from .sunspec import scan as sunspec_scan
        from .vendor import scan as vendor_scan

        devices: list[Device] = []

        devices.extend(sunspec_scan(inverter=self, device_id=device_id))
        devices.extend(vendor_scan(inverter=self, device_id=device_id))

        return devices
