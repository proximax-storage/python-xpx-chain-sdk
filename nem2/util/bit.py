"""
    bit
    ===

    Utilities to modify individual bits from bytes.

    License
    -------

    Copyright 2019 NEM

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from __future__ import annotations


def set(byte: int, index: int) -> int:
    """Set bit at index to 1."""

    assert 0 <= byte <= 255
    assert 0 <= index <= 7

    return byte | (1 << index)


def clear(byte: int, index: int) -> int:
    """Set bit at index to 0."""

    assert 0 <= byte <= 255
    assert 0 <= index <= 7

    # Python guarantees the ~ operator will return the 2s complement
    # signed integer with the same bit pattern, AKA, ~128 is -129, not 127.
    # However, the & operator with the resulting value will use the sign bit,
    # so `255 & 127 == 255 & -129`, for example.
    return byte & ~(1 << index)


def assign(byte: int, index: int, value: bool) -> int:
    """Assign bit at index depending on value."""

    if value:
        return set(byte, index)
    else:
        return clear(byte, index)


def toggle(byte: int, index: int) -> int:
    """Toggle bit at index."""

    assert 0 <= byte <= 255
    assert 0 <= index <= 7

    return byte ^ (1 << index)


def get(byte: int, index: int) -> int:
    """Get bit at index."""

    assert 0 <= byte <= 255
    assert 0 <= index <= 7

    return (byte >> index) & 1
