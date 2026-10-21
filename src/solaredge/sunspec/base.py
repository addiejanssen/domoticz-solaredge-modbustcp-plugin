from typing import ClassVar

from pymodbus.client import ModbusTcpClient

from ..base import Device, DeviceDescription, ModbusDataType, ModbusWordOrder, RegisterMap, RegisterMapEntry
from .constants import SunSpecNotImplemented


class SunSpecDevice(Device):
    """
    Every SunSpec Model has an id and a length field.
    This is used as the base class for all SunSpec models
    to prevent that we need to add this to each model class.
    """

    register_count: ClassVar[int] = 2
    register_map: ClassVar[RegisterMap] = {
        **Device.register_map,
        "id": RegisterMapEntry(
            offset=0,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Model identifier",
        ),
        "l": RegisterMapEntry(
            offset=1,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Model length",
        ),
    }

    def get(self, key: str) -> int | float | str | list[bool] | list[int] | list[float] | None:
        """
        This is the SunSpec specific get() function which checks for
        SunSpec not implemented values.
        """
        target_value = None
        not_implemented: bool = False

        if self._registers and key in self.register_map.keys():
            map_entry: RegisterMapEntry = self.register_map[key]

            converted_value = super().get(key)

            if converted_value is not None:
                if isinstance(converted_value, int):
                    if map_entry.register_type == ModbusTcpClient.DATATYPE.INT16 and abs(converted_value) == SunSpecNotImplemented.INT16:
                        not_implemented = True
                    if map_entry.register_type == ModbusTcpClient.DATATYPE.UINT16 and abs(converted_value) == SunSpecNotImplemented.UINT16:
                        not_implemented = True
                    if map_entry.register_type == ModbusTcpClient.DATATYPE.INT32 and abs(converted_value) == SunSpecNotImplemented.INT32:
                        not_implemented = True
                    if map_entry.register_type == ModbusTcpClient.DATATYPE.UINT32 and abs(converted_value) == SunSpecNotImplemented.UINT32:
                        not_implemented = True
                    if map_entry.register_type == ModbusTcpClient.DATATYPE.INT64 and abs(converted_value) == SunSpecNotImplemented.INT64:
                        not_implemented = True
                    if map_entry.register_type == ModbusTcpClient.DATATYPE.UINT64 and abs(converted_value) == SunSpecNotImplemented.UINT64:
                        not_implemented = True
                elif isinstance(converted_value, float):
                    if map_entry.register_type == ModbusTcpClient.DATATYPE.FLOAT32 and abs(converted_value) == SunSpecNotImplemented.FLOAT32:
                        not_implemented = True

            if not not_implemented:
                target_value = converted_value

        return target_value


class SunSpecSupportIdentifier(SunSpecDevice):
    """
    This is a specific class for checking if an inverter supports SunSpec or not
    """

    register_count: ClassVar[int] = 2
    register_map: ClassVar[RegisterMap] = {
        "identifier": RegisterMapEntry(
            offset=0,
            size=2,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.STRING,
            python_type=str,
            scaling_item_id="",
            description="Static SunSpec Identifier",
        ),
    }


class SunSpecDeviceUnknownModel(SunSpecDevice):
    """Not yet implemented SunSpec Model"""

    device_description: ClassVar[DeviceDescription] = DeviceDescription(
        id=0, name="unknown", label="Unknown", description="This SunSpec Model is not included in this software yet."
    )
