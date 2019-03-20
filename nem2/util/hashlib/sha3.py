"""
    sha3
    ====

    Implementation of the SHA3 cryptographic hash functions.

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
import hashlib
import typing

# API


def sha3_224(data: typing.Optional[bytes] = None):
    """Returns a sha3_224 hash object; optionally initialized with a string."""

    if data is None:
        return hashlib.sha3_224()
    return hashlib.sha3_224(data)


def sha3_256(data: typing.Optional[bytes] = None):
    """Returns a sha3_256 hash object; optionally initialized with a string."""

    if data is None:
        return hashlib.sha3_256()
    return hashlib.sha3_256(data)


def sha3_384(data: typing.Optional[bytes] = None):
    """Returns a sha3_384 hash object; optionally initialized with a string."""

    if data is None:
        return hashlib.sha3_384()
    return hashlib.sha3_384(data)


def sha3_512(data: typing.Optional[bytes] = None):
    """Returns a sha3_512 hash object; optionally initialized with a string."""

    if data is None:
        return hashlib.sha3_512()
    return hashlib.sha3_512(data)
