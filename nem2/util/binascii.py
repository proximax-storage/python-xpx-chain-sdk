"""
    binascii
    ========

    Utilities for converting between binary and ascii data.

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

import binascii
import typing

HexType = typing.Union[str, bytes, bytearray]
BytesType = typing.Union[bytes, bytearray]


def hexlify(data: BytesType, with_prefix=False) -> str:
    """Convert bytes data to hexadecimal string."""

    encoded = binascii.hexlify(data).decode('ascii')
    if with_prefix:
        return '0x' + encoded
    return encoded


def unhexlify(data: HexType, with_prefix=False) -> bytes:
    """Convert hexadecimal string to raw bytes."""

    if with_prefix:
        data = remove_prefix(data)
    return binascii.unhexlify(data)


@typing.no_type_check
def remove_prefix(data: HexType) -> HexType:
    """Remove hexadecimal prefix from string ('0x', '0X')"""

    if isinstance(data, str):
        prefix = ('0x', '0X')
    else:
        prefix = (b'0x', b'0X')

    if data.startswith(prefix):
        return data[2:]
    return data
