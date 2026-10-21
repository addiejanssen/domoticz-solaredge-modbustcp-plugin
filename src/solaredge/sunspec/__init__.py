from ..base import Device, SolarEdge
from .base import SunSpecDevice, SunSpecDeviceUnknownModel, SunSpecSupportIdentifier
from .constants import SUNSPEC_BASE_ADDRESS, SUNSPEC_IDENTIFIER, SunSpecNotImplemented
from .model1 import SunSpecDeviceModel1
from .model101 import SunSpecDeviceModel101
from .model102 import SunSpecDeviceModel102
from .model103 import SunSpecDeviceModel103
from .model201 import SunSpecDeviceModel201
from .model202 import SunSpecDeviceModel202
from .model203 import SunSpecDeviceModel203
from .model204 import SunSpecDeviceModel204

__all__: list[str] = [
    "SunSpecDeviceModel1",
    "SunSpecDeviceModel101",
    "SunSpecDeviceModel102",
    "SunSpecDeviceModel103",
    "SunSpecDeviceModel201",
    "SunSpecDeviceModel202",
    "SunSpecDeviceModel203",
    "SunSpecDeviceModel204",
    "SunSpecNotImplemented",
    "SunSpecDeviceUnknownModel",
    "scan",
]

_all_models: dict[int, type] = {
    1: SunSpecDeviceModel1,
    101: SunSpecDeviceModel101,
    102: SunSpecDeviceModel102,
    103: SunSpecDeviceModel103,
    201: SunSpecDeviceModel201,
    202: SunSpecDeviceModel202,
    203: SunSpecDeviceModel203,
    204: SunSpecDeviceModel204,
}


def scan(inverter: SolarEdge, device_id: int) -> list[Device]:
    """
    Check if the inverter supplies a SunSpec map.
    If so iterate through all the devices and try to match with known/supported SunSpec models.
    If successful, returns a list with Devices.
    """
    devices: list[Device] = []

    identifier = None
    device = SunSpecSupportIdentifier(inverter=inverter, device_id=device_id, address=SUNSPEC_BASE_ADDRESS)
    if device.read():
        identifier = device.get("identifier")

    if identifier and identifier == SUNSPEC_IDENTIFIER:
        address: int = SUNSPEC_BASE_ADDRESS + SunSpecSupportIdentifier.register_count

        while address > 0:
            device = SunSpecDevice(inverter=inverter, device_id=device_id, address=address)
            if device.read():
                id: int = device.get("id")  # type: ignore

                if id:
                    if id in _all_models.keys():
                        d = _all_models[id](inverter=inverter, device_id=device_id, address=address)
                    else:
                        d = SunSpecDeviceUnknownModel(inverter=inverter, device_id=device_id, address=address)

                    devices.append(d)
                    length: int = device.get("l")  # type: ignore
                    address = address + SunSpecDevice.register_count + length
                else:
                    address = -1
            else:
                address = -1

    return devices
