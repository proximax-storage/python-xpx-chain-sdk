"""
    crypto
    ======

    Wrappers for PyCryptodome keccak hash functions.

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

# Disable warnings for importing Keccak, PyCryptoDome is spuriously
# flagged for using legacy hashes, but we need to use those hashes
# for compatibility.
from __future__ import annotations
from Crypto.Hash import keccak      # nosec
import typing

# API


def keccak_224(data: typing.Optional[bytes] = None) -> keccak:
    """Returns a 224-bit keccak hash object; optionally initialized with a string."""

    return keccak.new(digest_bits=224, data=data)


def keccak_256(data: typing.Optional[bytes] = None) -> keccak:
    """Returns a 256-bit keccak hash object; optionally initialized with a string."""

    return keccak.new(digest_bits=256, data=data)


def keccak_384(data: typing.Optional[bytes] = None) -> keccak:
    """Returns a 384-bit keccak hash object; optionally initialized with a string."""

    return keccak.new(digest_bits=384, data=data)


def keccak_512(data: typing.Optional[bytes] = None) -> keccak:
    """Returns a 512-bit keccak hash object; optionally initialized with a string."""

    return keccak.new(digest_bits=512, data=data)
