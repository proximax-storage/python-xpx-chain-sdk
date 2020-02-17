"""
    address
    =======

    A public identifier for an account and network type.

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
import typing

from ..blockchain.network_type import NetworkType
from ... import util

__all__ = ['Address']

T = typing.TypeVar('T')
U = typing.Sequence[T]


def chunks(collection: U, n: int) -> typing.Generator[U, None, None]:
    """Generate n-sized chunks from collection."""

    for i in range(0, len(collection), n):
        yield collection[i:i + n]


def calculate_checksum(address: bytes) -> bytes:
    """Calculate the checksum for the address."""

    checksum = util.hashlib.sha3_256(address[:21]).digest()[:4]
    return typing.cast(bytes, checksum)


def public_key_to_address(
    public_key: bytes,
    network_type: NetworkType
) -> bytes:
    """
    Convert public key to address.

    :param public_key: Raw bytes of public key.
    :param network_type: Network type.
    :return: Address bytes.
    """

    # step 1: keccak256 hash of the public key
    public_key_hash: bytes = util.hashlib.sha3_256(public_key).digest()

    # step 2: ripemd160 hash of (1)
    ripemd_hash: bytes = util.hashlib.ripemd160(public_key_hash).digest()

    # step 3: add network identifier byte in front of (2)
    address = bytearray(25)
    address[0] = int(network_type)
    address[1:21] = ripemd_hash

    # step 4: concatenate (3) and the checksum of (3)
    address[21:] = calculate_checksum(address)

    return address


def is_valid_address(address: bytes) -> bool:
    """Check if address is valid."""

    return typing.cast(bool, calculate_checksum(address) == address[21:])


@util.inherit_doc
@util.dataclass(frozen=True)
class Address(util.Object):
    """
    Account address for network type.

    An address is derived from the public key and network type, and
    uniquely identifies a NEM account.

    :param address: Base32-encoded, human-readable address.
    """

    address: str
    network_type: NetworkType

    def __init__(self, address: str) -> None:
        plain = address.strip().upper().replace('-', '')
        if len(plain) != 40:
            raise ValueError(f"{address} is not a valid raw address")
        network_type = NetworkType.create_from_raw_address(plain)
        self._set('address', plain)
        self._set('network_type', network_type)

    @property
    def encoded(self) -> bytes:
        """Get encoded address."""
        return util.b32decode(self.address)

    @property
    def hex(self) -> str:
        """Get hex address."""
        return util.encode_hex(self.encoded).upper()

    @classmethod
    def create_from_raw_address(cls, address: str) -> Address:
        """
        Create Address from human-readable, raw address.

        :param address: Base32-encoded, human-readable address.
        :return: Address object.
        """
        return cls(address)

    @classmethod
    def create_from_encoded(cls, address: typing.AnyStr) -> Address:
        """
        Create Address from encoded address.

        :param address: Base32-decoded address bytes or hex-encoded bytes.
        :return: Address object.
        """

        address = util.decode_hex(address, with_prefix=True)
        if len(address) != 25:
            raise ValueError(f"{address!r} is not a valid encoded address")
        raw_address = util.b32encode(address)
        return cls.create_from_raw_address(raw_address)

    @classmethod
    def create_from_public_key(
        cls,
        public_key: typing.AnyStr,
        network_type: NetworkType
    ):
        """
        Create Address from the public key and network type.

        :param public_key: Hex-encoded public key (with or without '0x' prefix).
        :param network_type: Network type for address.
        :return: Address object.
        """

        key = util.decode_hex(public_key, with_prefix=True)
        if len(key) != 32:
            raise ValueError(f"{public_key!r} is not a valid public key")
        address: bytes = public_key_to_address(key, network_type)

        return cls.create_from_encoded(address)

    def plain(self) -> str:
        """Get plain representation of address as base32-decoded string."""
        return self.address

    def pretty(self) -> str:
        """Get pretty representation of address as base32-decoded string."""
        return u'-'.join(chunks(self.address, 6))

    def is_valid(self) -> bool:
        """Check if address is valid."""
        return is_valid_address(self.encoded)
