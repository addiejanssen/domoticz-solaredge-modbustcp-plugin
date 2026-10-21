from enum import IntEnum
from typing import ClassVar

from ..base import DeviceDescription, ModbusDataType, ModbusWordOrder, RegisterMap, RegisterMapEntry
from .base import VendorDevice


class VendorBattery(VendorDevice):
    """Vendor Specific device for batteries"""

    class Status(IntEnum):
        """States used by this Device"""

        OFF = 0
        STANDBY = 1
        INIT = 2
        CHARGE = 3
        DISCHARGE = 4
        FAULT = 5
        IDLE = 7
        POWER_SAVING = 10  # According to https://github.com/WillCodeForCats/solaredge-modbus-multi

    device_description: ClassVar[DeviceDescription] = DeviceDescription(id=0, name="battery", label="Battery", description="Battery Information")

    register_count: ClassVar[int] = 139
    register_map: ClassVar[RegisterMap] = {
        **VendorDevice.register_map,
        "mn": RegisterMapEntry(
            offset=0,
            size=16,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.STRING,
            python_type=str,
            scaling_item_id="",
            description="Manufacturer Name",
        ),
        "md": RegisterMapEntry(
            offset=16,
            size=16,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.STRING,
            python_type=str,
            scaling_item_id="",
            description="Model",
        ),
        "vr": RegisterMapEntry(
            offset=32,
            size=16,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.STRING,
            python_type=str,
            scaling_item_id="",
            description="Firmware Version",
        ),
        "sn": RegisterMapEntry(
            offset=48,
            size=16,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.STRING,
            python_type=str,
            scaling_item_id="",
            description="Serial Number",
        ),
        "da": RegisterMapEntry(
            offset=64,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Device ID",
        ),
        "re": RegisterMapEntry(
            offset=66,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.FLOAT32,
            python_type=float,
            scaling_item_id="",
            description="Rated Energy",
        ),
        "mccp": RegisterMapEntry(
            offset=68,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.FLOAT32,
            python_type=float,
            scaling_item_id="",
            description="Max Charge Continues Power",
        ),
        "mdcp": RegisterMapEntry(
            offset=70,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.FLOAT32,
            python_type=float,
            scaling_item_id="",
            description="Max Discharge Continues Power",
        ),
        "mcpp": RegisterMapEntry(
            offset=72,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.FLOAT32,
            python_type=float,
            scaling_item_id="",
            description="Max Charge PeakPower",
        ),
        "mdpp": RegisterMapEntry(
            offset=74,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.FLOAT32,
            python_type=float,
            scaling_item_id="",
            description="Max Discharge PeakPower",
        ),
        "at": RegisterMapEntry(
            offset=108,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.FLOAT32,
            python_type=float,
            scaling_item_id="",
            description="Average Temperature",
        ),
        "mt": RegisterMapEntry(
            offset=110,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.FLOAT32,
            python_type=float,
            scaling_item_id="",
            description="Max Temperature",
        ),
        "iv": RegisterMapEntry(
            offset=112,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.FLOAT32,
            python_type=float,
            scaling_item_id="",
            description="Instantaneous Voltage",
        ),
        "ic": RegisterMapEntry(
            offset=114,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.FLOAT32,
            python_type=float,
            scaling_item_id="",
            description="Instantaneous Current",
        ),
        "ip": RegisterMapEntry(
            offset=116,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.FLOAT32,
            python_type=float,
            scaling_item_id="",
            description="Instantaneous Power",
        ),
        "leec": RegisterMapEntry(
            offset=118,
            size=4,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="",
            description="Lifetime Export Energy Counter",
        ),
        "liec": RegisterMapEntry(
            offset=122,
            size=4,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.UINT64,
            python_type=int,
            scaling_item_id="",
            description="Lifetime Import EnergyCounter",
        ),
        "me": RegisterMapEntry(
            offset=126,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.FLOAT32,
            python_type=float,
            scaling_item_id="",
            description="Max Energy",
        ),
        "ae": RegisterMapEntry(
            offset=128,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.FLOAT32,
            python_type=float,
            scaling_item_id="",
            description="Available Energy",
        ),
        "soh": RegisterMapEntry(
            offset=130,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.FLOAT32,
            python_type=float,
            scaling_item_id="",
            description="State of Health",
        ),
        "soe": RegisterMapEntry(
            offset=132,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.FLOAT32,
            python_type=float,
            scaling_item_id="",
            description="State of Energy",
        ),
        "st": RegisterMapEntry(
            offset=134,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.UINT32,
            python_type=Status,
            scaling_item_id="",
            description="Status",
        ),
        "sti": RegisterMapEntry(
            offset=136,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.UINT32,
            python_type=Status,
            scaling_item_id="",
            description="Status Internal",
        ),
        "el": RegisterMapEntry(
            offset=138,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Events Log",
        ),
    }
