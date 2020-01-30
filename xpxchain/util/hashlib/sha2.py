"""
    sha2
    ====

    Implementation of the SHA2 cryptographic hash functions.

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


def sha224(data: typing.Optional[bytes] = None):
    """Returns a sha224 hash object; optionally initialized with a string."""

    if data is None:
        return hashlib.sha224()
    return hashlib.sha224(data)


def sha256(data: typing.Optional[bytes] = None):
    """Returns a sha256 hash object; optionally initialized with a string."""

    if data is None:
        return hashlib.sha256()
    return hashlib.sha256(data)


def sha384(data: typing.Optional[bytes] = None):
    """Returns a sha384 hash object; optionally initialized with a string."""

    if data is None:
        return hashlib.sha384()
    return hashlib.sha384(data)


def sha512(data: typing.Optional[bytes] = None):
    """Returns a sha512 hash object; optionally initialized with a string."""

    if data is None:
        return hashlib.sha512()
    return hashlib.sha512(data)
