"""
    stdint
    ======

    Although Python has native support for arbitrary-precision integers,
    Javascript by default uses 64-bit floats as the only numeric type,
    signifying they cannot store more than 53 integral bits.

    Therefore, in Javascript, 64-bit integers are stored as an array
    of 2 numbers. Likewise, 128-bit integers are stored as an array of 4
    numbers. These functions the conversion of native Python integers
    to and from a Javascript-like notation, to simplify integration with
    data transfer objects.

    This also provides routines to convert to and from fixed-width
    integers in both catbuffer and data-transfer objects, as well
    as extract high- and low-bit patterns from the types.

    The module is named after <stdint.h>, which describes fixed-width
    (standard) integers in C, even though it has no relationship
    in terms of functionality.
"""

from __future__ import annotations
import typing

__all__ = [
    # DTO Types
    'I8DTOType',
    'U8DTOType',
    'U16DTOType',
    'U32DTOType',
    'U64DTOType',
    'U128DTOType',

    # Byte sizes
    'I8_BYTES',
    'U8_BYTES',
    'U16_BYTES',
    'U32_BYTES',
    'U64_BYTES',
    'U128_BYTES',

    # I8
    # 'i8_high',
    # 'i8_low',
    'i8_iter_from_catbuffer',
    'i8_iter_from_dto',
    'i8_iter_to_catbuffer',
    'i8_iter_to_dto',
    'i8_from_catbuffer',
    'i8_from_dto',
    'i8_to_catbuffer',
    'i8_to_dto',

    # U8
    'u8_high',
    'u8_low',
    'u8_iter_from_catbuffer',
    'u8_iter_from_dto',
    'u8_iter_to_catbuffer',
    'u8_iter_to_dto',
    'u8_from_catbuffer',
    'u8_from_dto',
    'u8_to_catbuffer',
    'u8_to_dto',

    # U16
    'u16_high',
    'u16_low',
    'u16_iter_from_catbuffer',
    'u16_iter_from_dto',
    'u16_iter_to_catbuffer',
    'u16_iter_to_dto',
    'u16_from_catbuffer',
    'u16_from_dto',
    'u16_to_catbuffer',
    'u16_to_dto',

    # U32
    'u32_high',
    'u32_low',
    'u32_iter_from_catbuffer',
    'u32_iter_from_dto',
    'u32_iter_to_catbuffer',
    'u32_iter_to_dto',
    'u32_from_catbuffer',
    'u32_from_dto',
    'u32_to_catbuffer',
    'u32_to_dto',

    # U64
    'u64_high',
    'u64_low',
    'u64_iter_from_catbuffer',
    'u64_iter_from_dto',
    'u64_iter_to_catbuffer',
    'u64_iter_to_dto',
    'u64_from_catbuffer',
    'u64_from_dto',
    'u64_to_catbuffer',
    'u64_to_dto',

    # U128
    'u128_high',
    'u128_low',
    'u128_iter_from_catbuffer',
    'u128_iter_from_dto',
    'u128_iter_to_catbuffer',
    'u128_iter_to_dto',
    'u128_from_catbuffer',
    'u128_from_dto',
    'u128_to_catbuffer',
    'u128_to_dto',
]

U4_BITS = 4
U8_BITS = 8
U16_BITS = 16
U32_BITS = 32
U64_BITS = 64
U128_BITS = 128

U8_BYTES = U8_BITS // 8
U16_BYTES = U16_BITS // 8
U32_BYTES = U32_BITS // 8
U64_BYTES = U64_BITS // 8
U128_BYTES = U128_BITS // 8

U4_MAX = 0xF
U8_MAX = 0xFF
U16_MAX = 0xFFFF
U32_MAX = 0xFFFFFFFF
U64_MAX = 0xFFFFFFFFFFFFFFFF
U128_MAX = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

I8_BITS = 8

I8_BYTES = I8_BITS // 8

I8_MAX = 0x7F

I8_MIN = -0x80

U8DTOType = int
U16DTOType = int
U32DTOType = int
U64DTOType = typing.Sequence[U32DTOType]
U128DTOType = typing.Sequence[U64DTOType]
YieldIntType = typing.Generator[int, None, None]
YieldBytesType = typing.Generator[bytes, None, None]

I8DTOType = int

# HELPERS


def check_overflow(within_range: bool):
    """Raise exception if overflow."""
    if not within_range:
        raise OverflowError


def high(max: int, bits: int, mask: int) -> typing.Callable[[int], int]:
    def wrapper(value: int) -> int:
        check_overflow(0 <= value <= max)
        return (value >> bits) & mask

    wrapper.__name__ = f'u{2*bits}_high'
    wrapper.__qualname__ = wrapper.__name__
    wrapper.__doc__ = f'Get high {bits} from {2*bits}-bit integer.'
    wrapper.__module__ = __name__
    return wrapper


def low(max: int, bits: int, mask: int) -> typing.Callable[[int], int]:
    def wrapper(value: int) -> int:
        check_overflow(0 <= value <= max)
        return value & mask

    wrapper.__name__ = f'u{2*bits}_low'
    wrapper.__qualname__ = wrapper.__name__
    wrapper.__doc__ = f'Get low {bits} from {2*bits}-bit integer.'
    wrapper.__module__ = __name__
    return wrapper


def to_catbuffer_impl(size: int, signed: bool = False) -> typing.Callable[[int], bytes]:
    def wrapper(value: int, signed: bool = False) -> bytes:
        return value.to_bytes(size, 'little', signed=signed)
    return wrapper


def to_catbuffer(bits: int, signed: bool = False) -> typing.Callable[[int], bytes]:
    cb = to_catbuffer_impl(bits // 8, signed=signed)

    def wrapper(value: int, signed: bool = False) -> bytes:
        return cb(value)

    wrapper.__name__ = f'u{bits}_to_catbuffer'
    wrapper.__qualname__ = wrapper.__name__
    wrapper.__doc__ = f'Convert {bits}-bit integer to catbuffer.'
    wrapper.__module__ = __name__
    return wrapper


def iter_to_catbuffer(bits: int, signed: bool = False):
    cb = to_catbuffer_impl(bits // 8, signed=signed)

    def wrapper(iterable, signed: bool = False):
        for value in iterable:
            yield cb(value)

    wrapper.__name__ = f'u{bits}_iter_to_catbuffer'
    wrapper.__qualname__ = wrapper.__name__
    wrapper.__doc__ = f'Iteratively convert {bits}-bit integers to catbuffer.'
    wrapper.__module__ = __name__
    return wrapper


def from_catbuffer_impl(bits: int, signed: bool = False) -> typing.Callable[[bytes], int]:
    def wrapper(catbuffer: bytes, signed: bool = False) -> int:
        return int.from_bytes(catbuffer, 'little', signed=signed)
    return wrapper


def from_catbuffer(bits: int, signed: bool = False) -> typing.Callable[[bytes], int]:
    size = bits // 8
    cb = from_catbuffer_impl(size, signed=signed)

    def wrapper(catbuffer: bytes, signed: bool = False) -> int:
        if len(catbuffer) > size:
            raise OverflowError('bytes too big to convert')
        return cb(catbuffer)

    wrapper.__name__ = f'u{bits}_from_catbuffer'
    wrapper.__qualname__ = wrapper.__name__
    wrapper.__doc__ = f'Convert catbuffer to {bits}-bit integer.'
    wrapper.__module__ = __name__
    return wrapper


def iter_from_catbuffer(bits: int, signed: bool = False) -> typing.Callable[[bytes], YieldIntType]:
    size = bits // 8
    cb = from_catbuffer_impl(size, signed=signed)

    def wrapper(catbuffer: bytes, signed: bool = False) -> YieldIntType:
        length = len(catbuffer)
        if length % size != 0:
            raise ValueError(f'iter from_catbuffer requires multiple of {size}.')

        for i in range(0, length, size):
            start = i
            stop = start + size
            yield cb(catbuffer[start:stop])

    wrapper.__name__ = f'u{bits}_iter_from_catbuffer'
    wrapper.__qualname__ = wrapper.__name__
    wrapper.__doc__ = f'Iteratively convert catbuffer to {bits}-bit integers.'
    wrapper.__module__ = __name__
    return wrapper


def iter_to_dto(bits: int, cb):
    def wrapper(iterable):
        for value in iterable:
            yield cb(value)

    wrapper.__name__ = f'u{bits}_iter_to_dto'
    wrapper.__qualname__ = wrapper.__name__
    wrapper.__doc__ = f'Iteratively convert {bits}-bit integers to DTO.'
    wrapper.__module__ = __name__
    return wrapper


def iter_from_dto(bits: int, cb):
    def wrapper(iterable):
        for value in iterable:
            yield cb(value)

    wrapper.__name__ = f'u{bits}_iter_from_dto'
    wrapper.__qualname__ = wrapper.__name__
    wrapper.__doc__ = f'Iteratively convert DTOs to {bits}-bit integers.'
    wrapper.__module__ = __name__
    return wrapper


# UINT8


def u8_to_dto(value: int) -> U8DTOType:
    """Convert 8-bit int to DTO."""

    check_overflow(0 <= value <= U8_MAX)
    return value


def u8_from_dto(dto: U8DTOType) -> int:
    """Convert DTO to 8-bit int."""

    check_overflow(0 <= dto <= U8_MAX)
    return dto


u8_high = high(U8_MAX, U4_BITS, U4_MAX)
u8_low = low(U8_MAX, U4_BITS, U4_MAX)
u8_to_catbuffer = to_catbuffer(U8_BITS)
u8_from_catbuffer = from_catbuffer(U8_BITS)
u8_iter_to_catbuffer = iter_to_catbuffer(U8_BITS)
u8_iter_from_catbuffer = iter_from_catbuffer(U8_BITS)
u8_iter_to_dto = iter_to_dto(U8_BITS, u8_to_dto)
u8_iter_from_dto = iter_from_dto(U8_BITS, u8_from_dto)


# INT8


def i8_to_dto(value: int) -> I8DTOType:
    """Convert 8-bit int to DTO."""

    check_overflow(I8_MIN <= value <= I8_MAX)
    return value


def i8_from_dto(dto: I8DTOType) -> int:
    """Convert DTO to 8-bit int."""

    check_overflow(I8_MIN <= dto <= I8_MAX)
    return dto


# i8_high = high(I8_MAX, I4_BITS, I4_MAX)
# i8_low = low(I8_MAX, I4_BITS, I4_MAX)
i8_to_catbuffer = to_catbuffer(I8_BITS, signed=True)
i8_from_catbuffer = from_catbuffer(I8_BITS, signed=True)
i8_iter_to_catbuffer = iter_to_catbuffer(I8_BITS, signed=True)
i8_iter_from_catbuffer = iter_from_catbuffer(I8_BITS, signed=True)
i8_iter_to_dto = iter_to_dto(I8_BITS, i8_to_dto)
i8_iter_from_dto = iter_from_dto(I8_BITS, i8_from_dto)


# UINT16


def u16_to_dto(value: int) -> U16DTOType:
    """Convert 16-bit int to DTO."""

    check_overflow(0 <= value <= U16_MAX)
    return value


def u16_from_dto(dto: U16DTOType) -> int:
    """Convert DTO to 16-bit int."""

    check_overflow(0 <= dto <= U16_MAX)
    return dto


u16_high = high(U16_MAX, U8_BITS, U8_MAX)
u16_low = low(U16_MAX, U8_BITS, U8_MAX)
u16_to_catbuffer = to_catbuffer(U16_BITS)
u16_from_catbuffer = from_catbuffer(U16_BITS)
u16_iter_to_catbuffer = iter_to_catbuffer(U16_BITS)
u16_iter_from_catbuffer = iter_from_catbuffer(U16_BITS)
u16_iter_to_dto = iter_to_dto(U16_BITS, u16_to_dto)
u16_iter_from_dto = iter_from_dto(U16_BITS, u16_from_dto)

# UINT32


def u32_to_dto(value: int) -> U32DTOType:
    """Convert 32-bit int to DTO."""

    check_overflow(0 <= value <= U32_MAX)
    return value


def u32_from_dto(dto: U32DTOType) -> int:
    """Convert DTO to 32-bit int."""

    check_overflow(0 <= dto <= U32_MAX)
    return dto


u32_high = high(U32_MAX, U16_BITS, U16_MAX)
u32_low = low(U32_MAX, U16_BITS, U16_MAX)
u32_to_catbuffer = to_catbuffer(U32_BITS)
u32_from_catbuffer = from_catbuffer(U32_BITS)
u32_iter_to_catbuffer = iter_to_catbuffer(U32_BITS)
u32_iter_from_catbuffer = iter_from_catbuffer(U32_BITS)
u32_iter_to_dto = iter_to_dto(U32_BITS, u32_to_dto)
u32_iter_from_dto = iter_from_dto(U32_BITS, u32_from_dto)

# UINT64


def u64_to_dto(value: int) -> U64DTOType:
    """Convert 64-bit int to DTO."""

    check_overflow(0 <= value <= U64_MAX)
    return [u64_low(value), u64_high(value)]


def u64_from_dto(dto: U64DTOType) -> int:
    """Convert DTO to 64-bit int."""

    if not (
        len(dto) == 2
        and dto[0] <= U32_MAX
        and dto[1] <= U32_MAX
    ):
        raise ArithmeticError

    return (dto[0]) | (dto[1] << U32_BITS)


u64_high = high(U64_MAX, U32_BITS, U32_MAX)
u64_low = low(U64_MAX, U32_BITS, U32_MAX)
u64_to_catbuffer = to_catbuffer(U64_BITS)
u64_from_catbuffer = from_catbuffer(U64_BITS)
u64_iter_to_catbuffer = iter_to_catbuffer(U64_BITS)
u64_iter_from_catbuffer = iter_from_catbuffer(U64_BITS)
u64_iter_to_dto = iter_to_dto(U64_BITS, u64_to_dto)
u64_iter_from_dto = iter_from_dto(U64_BITS, u64_from_dto)

# UINT128


def u128_to_dto(value: int) -> U128DTOType:
    """Convert 128-bit int to DTO."""

    check_overflow(0 <= value <= U128_MAX)
    low = u128_low(value)
    high = u128_high(value)
    return [u64_to_dto(low), u64_to_dto(high)]


def u128_from_dto(dto: U128DTOType) -> int:
    """Convert DTO to 128-bit int."""

    if len(dto) != 2:
        raise ArithmeticError

    low = u64_from_dto(dto[0])
    high = u64_from_dto(dto[1])
    return low | (high << U64_BITS)


u128_high = high(U128_MAX, U64_BITS, U64_MAX)
u128_low = low(U128_MAX, U64_BITS, U64_MAX)
u128_to_catbuffer = to_catbuffer(U128_BITS)
u128_from_catbuffer = from_catbuffer(U128_BITS)
u128_iter_to_catbuffer = iter_to_catbuffer(U128_BITS)
u128_iter_from_catbuffer = iter_from_catbuffer(U128_BITS)
u128_iter_to_dto = iter_to_dto(U128_BITS, u128_to_dto)
u128_iter_from_dto = iter_from_dto(U128_BITS, u128_from_dto)
