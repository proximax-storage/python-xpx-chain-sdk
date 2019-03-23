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

from __future__ import annotations
import itertools
import re
import typing

from . import hashlib
from . import stdint

__all__ = [
    'generate_mosaic_id',
    'generate_sub_namespace_id',
    'generate_namespace_id',
]

FQN = re.compile(r'\A[a-z0-9][a-z0-9-_]*\Z')
NAMESPACE_MAX_DEPTH = 3
pack_u64 = stdint.u64_to_catbuffer
unpack_u32 = stdint.u32_iter_from_catbuffer
unpack_u64_dto = lambda x: list(itertools.islice(unpack_u32(x), 2))


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
    result = unpack_u64_dto(hasher.digest())

    return stdint.u64_from_dto((result[0], result[1] & 0x7FFFFFFF))


def generate_sub_namespace_id(parent_id: int, name: str) -> int:
    """
    Generate namespace ID from child namespace name and parent ID.

    :param parent_id: Identifier for parent namespace.
    :param name: Child namespace name.

    Example:
        .. code-block:: python

           >>> generate_sub_namespace_id(0x84b3552d375ffa4b, "sample")
    """

    hasher = hashlib.sha3_256()
    hasher.update(pack_u64(parent_id))
    hasher.update(name.encode('ascii'))
    result = unpack_u64_dto(hasher.digest())
    child_id = stdint.u64_from_dto((result[0], result[1] | 0x80000000))

    return child_id


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
        parent_id = generate_sub_namespace_id(parent_id, name)
        ids.append(parent_id)

    return ids
