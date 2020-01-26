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
    'decode_base32',
    'decode_base64',
    'encode_base32',
    'encode_base64',
]


def b32encode(data: bytes, with_suffix=True) -> str:
    """Encode bytes data to a base32-encoded string."""

    encoded = base64.b32encode(data).decode('ascii')
    return remove_suffix(encoded, with_suffix=with_suffix)


def encode_base32(data: typing.AnyStr, with_suffix=True) -> str:
    """Encodes raw bytes to base32."""

    if isinstance(data, str):
        return remove_suffix(data, with_suffix=with_suffix)
    return b32encode(data, with_suffix=with_suffix)


def b32decode(data: typing.AnyStr, with_suffix=True) -> bytes:
    """Decode bytes data from a base32-encoded string."""

    if not with_suffix:
        data = add_suffix(data, 8)
    return base64.b32decode(data)


def decode_base32(data: typing.AnyStr, with_suffix=True) -> bytes:
    """Decode base32 data to raw bytes."""

    if isinstance(data, (bytes, bytearray)):
        return data
    return b32decode(data, with_suffix=with_suffix)


def b64encode(data: bytes, altchars=None, with_suffix=True) -> str:
    """Encode bytes data to a base64-encoded string."""

    encoded = base64.b64encode(data, altchars=altchars).decode('ascii')
    return remove_suffix(encoded, with_suffix=with_suffix)


def encode_base64(data: typing.AnyStr, altchars=None, with_suffix=True) -> str:
    """Encodes raw bytes to base64."""

    if isinstance(data, str):
        return remove_suffix(data, with_suffix=with_suffix)
    return b64encode(data, altchars=altchars, with_suffix=with_suffix)


def b64decode(data: typing.AnyStr, altchars=None, with_suffix=True) -> bytes:
    """Decode bytes data from a base64-encoded string."""

    if not with_suffix:
        data = add_suffix(data, 4)
    return base64.b64decode(data, altchars=altchars)


def decode_base64(data: typing.AnyStr, altchars=None, with_suffix=True) -> bytes:
    """Decode base64 data to raw bytes."""

    if isinstance(data, (bytes, bytearray)):
        return data
    return b64decode(data, altchars=altchars, with_suffix=with_suffix)


@typing.no_type_check
def add_suffix(data: typing.AnyStr, width: int) -> typing.AnyStr:
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


def remove_suffix(data: str, with_suffix=True) -> str:
    """Remove '=' suffix from encoded str."""

    if not with_suffix:
        return data.rstrip('=')
    return data
