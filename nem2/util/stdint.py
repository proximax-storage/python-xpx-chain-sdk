"""
    uint64
    ======

    Although Python has native support for arbitrary-precision integers,
    Javascript by default uses 64-bit floats as the only numeric type,
    signifying they cannot store more than 53 integral bits.

    Therefore, in Javascript, 64-bit integers are stored as an array
    of 2 numbers. Likewise, 128-bit integers are stored as an array of 4
    numbers. These functions the conversion of native Python integers
    to and from a Javascript-like notation, to simplify integration with
    data transfer objects.

    The module is named after <stdint.h>, which describes fixed-width
    (standard) integers in C, even though it has no relationship
    in terms of functionality.
"""

import typing

__all__ = [
    # Typing
    'Uint32DtoType',
    'Uint64DtoType',
    'Uint128DtoType',

    # Helpers
    'uint64_high',
    'uint64_low',
    'uint64_to_dto',
    'dto_to_uint64',
    'uint128_high',
    'uint128_low',
    'uint128_to_dto',
    'dto_to_uint128',
]

UINT32_MAX = 0xFFFFFFFF
UINT64_MAX = 0xFFFFFFFFFFFFFFFF
UINT128_MAX = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

Uint32DtoType = int
Uint64DtoType = typing.Sequence[Uint32DtoType]
Uint128DtoType = typing.Sequence[Uint64DtoType]


def uint64_high(value: int) -> int:
    """Get high 32 bits from 64-bit integer."""

    assert value <= UINT64_MAX
    return (value >> 32) & UINT32_MAX


def uint64_low(value: int) -> int:
    """Get low 32 bits from 64-bit integer."""

    assert value <= UINT64_MAX
    return value & UINT32_MAX


def uint64_to_dto(value: int) -> Uint64DtoType:
    """Convert 64-bit int to DTO."""

    assert value <= UINT64_MAX
    return [uint64_low(value), uint64_high(value)]


def dto_to_uint64(dto: Uint64DtoType) -> int:
    """Convert DTO to 64-bit int."""

    assert len(dto) == 2
    low = dto[0]
    high = dto[1] << 32
    value = low | high
    assert value <= UINT64_MAX
    return value


def uint128_high(value: int) -> int:
    """Get high 64 bits from 128-bit integer."""

    assert value <= UINT128_MAX
    return (value >> 64) & UINT64_MAX


def uint128_low(value: int) -> int:
    """Get low 64 bits from 128-bit integer."""

    assert value <= UINT128_MAX
    return value & UINT64_MAX


def uint128_to_dto(value: int) -> Uint128DtoType:
    """Convert 128-bit int to DTO."""

    assert value <= UINT128_MAX
    low = uint64_to_dto(uint128_low(value))
    high = uint64_to_dto(uint128_high(value))
    return [low, high]


def dto_to_uint128(dto: Uint128DtoType) -> int:
    """Convert DTO to 128-bit int."""

    assert len(dto) == 2
    low = dto_to_uint64(dto[0])
    high = dto_to_uint64(dto[1]) << 64
    value = low | high
    assert value <= UINT128_MAX
    return value
