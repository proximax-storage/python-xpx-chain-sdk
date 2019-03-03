"""
    uint64
    ======

    Although Python has native support for arbitrary-precision integers,
    Javascript by default uses 64-bit floats as the only numeric type,
    signifying they cannot store more than 53 integral bits.

    Therefore, in Javascript, these integers are stored as an array
    of 2 numbers. These support the conversion of native Python integers
    to and from a Javascript-like notation, to simplify integration with
    data transfer objects.
"""

from typing import Sequence


def uint64_to_dto(value: int) -> Sequence[int]:
    """Convert 64-bit int to DTO."""

    assert value <= 0xFFFFFFFFFFFFFFFF
    lower = value & 0xFFFFFFFF
    upper = (value >> 32) & 0xFFFFFFFF
    return [lower, upper]


def dto_to_uint64(l: Sequence[int]) -> int:
    """Convert DTO to 64-bit int."""

    assert len(l) == 2
    lower = l[0]
    upper = l[1] << 32
    value = lower | upper
    assert value <= 0xFFFFFFFFFFFFFFFF
    return value
