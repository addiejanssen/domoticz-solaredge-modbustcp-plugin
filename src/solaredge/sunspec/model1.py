from typing import ClassVar

from ..base import DeviceDescription, ModbusDataType, ModbusWordOrder, RegisterMap, RegisterMapEntry
from .base import SunSpecDevice


class SunSpecDeviceModel1(SunSpecDevice):
    """Definition for SunSpec Model 1 Common"""

    device_description: ClassVar[DeviceDescription] = DeviceDescription(
        id=1,
        name="common",
        label="Common",
        description="All SunSpec compliant devices must include this as the first model"
    )

    register_count: ClassVar[int] = 67
    register_map: ClassVar[RegisterMap] = {
        **SunSpecDevice.register_map,
        "mn": RegisterMapEntry(
            offset=2,
            size=16,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.STRING,
            python_type=str,
            scaling_item_id="",
            description="Well known value registered with SunSpec for compliance",
        ),
        "md": RegisterMapEntry(
            offset=18,
            size=16,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.STRING,
            python_type=str,
            scaling_item_id="",
            description="Manufacturer specific value (32 chars)",
        ),
        "opt": RegisterMapEntry(
            offset=34,
            size=8,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.STRING,
            python_type=str,
            scaling_item_id="",
            description="Manufacturer specific value (16 chars)",
        ),
        "vr": RegisterMapEntry(
            offset=42,
            size=8,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.STRING,
            python_type=str,
            scaling_item_id="",
            description="Manufacturer specific value (16 chars)",
        ),
        "sn": RegisterMapEntry(
            offset=50,
            size=16,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.STRING,
            python_type=str,
            scaling_item_id="",
            description="Manufacturer specific value (32 chars)",
        ),
        "da": RegisterMapEntry(
            offset=66,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Modbus device address",
        ),
    }
