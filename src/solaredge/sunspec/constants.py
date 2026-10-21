from enum import IntEnum


class SunSpecNotImplemented(IntEnum):
    """SunSpec NOT IMPLEMENTED values for the various types"""

    INT16 = 0x8000
    UINT16 = 0xFFFF
    INT32 = 0x80000000
    UINT32 = 0xFFFFFFFF
    INT64 = 0x8000000000000000
    UINT64 = 0xFFFFFFFFFFFFFFFF
    FLOAT32 = 0x7FC00000


SUNSPEC_IDENTIFIER: str = "SunS"
SUNSPEC_BASE_ADDRESS: int = 40000  # 0x9c40 - this is where the SunSpec map should start
