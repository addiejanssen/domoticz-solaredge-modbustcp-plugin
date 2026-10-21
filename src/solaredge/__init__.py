__all__: list[str] = [
    "Device",
    "SolarEdge",
    "scan",
]

from .base import Device, SolarEdge


def scan(hostname: str, port_number: int, device_id: int) -> list[Device]:
    """Scan for all devices in/attached to a SolarEdge inverter"""
    inverter: SolarEdge = SolarEdge(hostname=hostname, port_number=port_number)
    return inverter.scan(device_id=device_id)
