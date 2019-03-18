"""
    base64
    ======

    Utilities for converting to and from base32 and base64 encodings.

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
import base64
import typing

__all__ = [
    'b32encode',
    'b32decode',
    'b64encode',
    'b64decode',
]

BasenType = typing.Union[str, bytes, bytearray]
BytesType = typing.Union[bytes, bytearray]


def b32encode(data: BytesType, with_suffix=True) -> str:
    """Encode bytes data to a base32-encoded string."""

    encoded = base64.b32encode(data).decode('ascii')
    if not with_suffix:
        encoded = encoded.rstrip('=')
    return encoded


def b32decode(data: BasenType, with_suffix=True) -> bytes:
    """Decode bytes data from a base32-encoded string."""

    if not with_suffix:
        data = add_suffix(data, 8)
    return base64.b32decode(data)


def b64encode(data: BytesType, altchars=None, with_suffix=True) -> str:
    """Encode bytes data to a base64-encoded string."""

    encoded = base64.b64encode(data, altchars=altchars).decode('ascii')
    if not with_suffix:
        encoded = encoded.rstrip('=')
    return encoded


def b64decode(data: BasenType, altchars=None, with_suffix=True) -> bytes:
    """Decode bytes data from a base64-encoded string."""

    if not with_suffix:
        data = add_suffix(data, 4)
    return base64.b64decode(data, altchars=altchars)


@typing.no_type_check
def add_suffix(data: BasenType, width: int) -> BasenType:
    """Add basen suffix to string ('=')."""

    if isinstance(data, str):
        padchar = '='
    else:
        padchar = b'='

    trailing = len(data) % width
    if trailing != 0:
        pad = width - trailing
        data = data + padchar * pad

    return data
