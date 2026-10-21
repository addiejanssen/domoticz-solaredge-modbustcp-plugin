from ..base import Device, SolarEdge
from .battery import VendorBattery

__all__: list[str] = [
    "VendorBattery",
    "scan",
]

VENDOR_BATTERY_BASE_ADDRESS = 57600
VENDOR_BATTERY_BLOCK_LENGTH = 256
VENDOR_BATTERY_COUNT = 2


def scan(inverter: SolarEdge, device_id: int) -> list[Device]:
    """
    Check if the inverter supplies Vendor specific devices.
    If successful, returns a list with Devices.
    """
    devices: list[Device] = []
    index = 0
    while index < VENDOR_BATTERY_COUNT:
        address: int = VENDOR_BATTERY_BASE_ADDRESS + (index * VENDOR_BATTERY_BLOCK_LENGTH)

        device = VendorBattery(inverter=inverter, device_id=device_id, address=address)
        if device.read():
            da: int = device.get("da")  # type: ignore
            if da and da > 0 and da != 255:
                # 255 should indicate "no battery", however, some inverters
                # return valid values, although there's no battery attached.
                # So, we check if there's a manufacturer name as well.

                mn: str = device.get("mn")  # type: ignore
                if mn:
                    # We have a valid device address and a manufacturer name.
                    devices.append(device)
            index += 1

    return devices
