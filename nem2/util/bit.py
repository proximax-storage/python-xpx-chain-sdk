"""
    bit
    ===

    Utilities to modify individual bits from bytes.
"""


def set(byte: int, index: int):
    """Set bit at index to 1."""

    assert 0 <= byte <= 255
    assert 0 <= index <= 7

    return byte | (1 << index)


def clear(byte: int, index: int):
    """Set bit at index to 0."""

    assert 0 <= byte <= 255
    assert 0 <= index <= 7

    # Python guarantees the ~ operator will return the 2s complement
    # signed integer with the same bit pattern, AKA, ~128 is -129, not 127.
    # However, the & operator with the resulting value will use the sign bit,
    # so `255 & 127 == 255 & -129`, for example.
    return byte & ~(1 << index)


def assign(byte: int, index: int, value: bool):
    """Assign bit at index depending on value."""

    if value:
        return set(byte, index)
    else:
        return clear(byte, index)


def toggle(byte: int, index: int):
    """Toggle bit at index."""

    assert 0 <= byte <= 255
    assert 0 <= index <= 7

    return byte ^ (1 << index)


def get(byte: int, index: int):
    """Get bit at index."""

    assert 0 <= byte <= 255
    assert 0 <= index <= 7

    return (byte >> index) & 1
