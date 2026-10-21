from typing import ClassVar

from ..base import Device, RegisterMap


class VendorDevice(Device):
    """This is the base class for Vendor specific, read non-SunSpec devices."""

    register_map: ClassVar[RegisterMap] = {
        **Device.register_map,
    }
