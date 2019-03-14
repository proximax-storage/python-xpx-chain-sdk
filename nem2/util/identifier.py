"""
    id_generator
    ============

    Generate integral identifiers from names.

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

import itertools
import re
import struct
import typing

from . import hashlib
from . import stdint

FQN = re.compile(r'\A[a-z0-9][a-z0-9-_]*\Z')
NAMESPACE_MAX_DEPTH = 3


def unpack_uint32(data: bytes) -> typing.Generator[int, None, None]:
    """Unpack array of 32-bit integers from a byte array."""

    for value in struct.iter_unpack('<I', data):
        yield value[0]


def generate_mosaic_id(nonce: bytes, public_key: bytes) -> int:
    """
    Generate mosaic ID from nonce and public key.

    :param nonce: Mosaic nonce.
    :param owner: Account of mosaic owner.

    Example:
        .. code-block:: python

            >>> nonce = b'\x00\x00\x00\x00'
            >>> public_key = binascii.unhexlify(
            ...     '7D08373CFFE4154E129E04F0827E5F3D'
            ...     '6907587E348757B0F87D2F839BF88246'
            ... )
            >>> generate_mosaic_id(nonce, public_key)
            3456466875032780966
    """

    assert len(nonce) == 4
    assert len(public_key) == 32

    hasher = hashlib.sha3_256()
    hasher.update(nonce)
    hasher.update(public_key)
    result = list(itertools.islice(unpack_uint32(hasher.digest()), 2))

    return stdint.dto_to_uint64((result[0], result[1] & 0x7FFFFFFF))


def generate_namespace_id(*names: str) -> typing.Sequence[int]:
    """
    Generate namespace ID from names.

    :param *names: Component names for a namespace.

    Example:
        .. code-block:: python

           >>> generate_namespace_id("sample")
           >>> generate_namespace_id("sample", "subpath")
           >>> generate_namespace_id("sample.subpath")
    """

    name = '.'.join(names)
    names = name.split('.')
    if name == '':
        return []
    elif len(names) > NAMESPACE_MAX_DEPTH:
        raise ValueError(f"Namespace '{name}' has too many parts.")
    elif not all(FQN.match(i) for i in names):
        raise ValueError(f"Invalid part name for namespace '{name}'.")

    ids = []
    parent_id = 0
    for name in names:
        hasher = hashlib.sha3_256()
        hasher.update(struct.pack('<Q', parent_id))
        hasher.update(name.encode('ascii'))
        result = list(itertools.islice(unpack_uint32(hasher.digest()), 2))
        parent_id = stdint.dto_to_uint64((result[0], result[1] | 0x80000000))
        ids.append(parent_id)

    return ids
