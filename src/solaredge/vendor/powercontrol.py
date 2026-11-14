from enum import IntFlag
from typing import ClassVar

from ..base import DeviceDescription, ModbusDataType, ModbusWordOrder, RegisterMap, RegisterMapEntry
from .base import VendorDevice


class VendorPowerControl(VendorDevice):
    """
    Vendor Specific device for Power Control
    
    This class is based on the SolarEdge Application Note "Power Reduction Control in SolarEdge Inverters"
    which documents two options for power reduction control in SolarEdge inverters:
    - Hardware Power Reduction: The inverter can be connected to a RRCR (Radio Ripple Control Receiver) in order to dynamically limit the output power of all the inverters in the installation.
    - Software Configurable Power Limitation: A fixed power limit as a percentage [%].
    """

    class RRCRFlag(IntFlag):
        """Radio Ripple Control Receiver flags"""

        L1 = 1
        L2 = 2
        L3 = 4
        L4 = 8

    device_description: ClassVar[DeviceDescription] = DeviceDescription(id=0, name="power_control", label="Power Control", description="Power Control")

    register_count: ClassVar[int] = 4
    register_map: ClassVar[RegisterMap] = {
        **VendorDevice.register_map,
        "rrcr": RegisterMapEntry(
            offset=0,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=RRCRFlag,
            scaling_item_id="",
            description="RRCR State",
        ),
        "apl": RegisterMapEntry(
            offset=1,
            size=1,
            word_order=ModbusWordOrder.BIG,
            register_type=ModbusDataType.UINT16,
            python_type=int,
            scaling_item_id="",
            description="Active Power Limit",
        ),
        "pf": RegisterMapEntry(
            offset=2,
            size=2,
            word_order=ModbusWordOrder.LITTLE,
            register_type=ModbusDataType.FLOAT32,
            python_type=float,
            scaling_item_id="",
            description="Cosine phi",
        ),
    }
