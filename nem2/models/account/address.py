"""
    address
    =======

    A public identifier for a NEM account and network type.

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

import typing

from nem2 import util
from ..blockchain.network_type import NetworkType

BytesType = typing.Union[bytes, bytearray]


def chunks(collection, n):
    """Generate n-sized chunks from collection."""

    for i in range(0, len(collection), n):
        yield collection[i:i + n]


def calculate_checksum(address: BytesType) -> bytes:
    """Calculate the checksum for the address."""

    return util.hashlib.sha3_256(address[:21]).digest()[:4]


def public_key_to_address(public_key: bytes, network_type: NetworkType) -> bytes:
    """
    Convert public key to address.

    :param public_key: Raw bytes of public key.
    :param network_type: Network type.
    :return: Address bytes.
    """

    # step 1: keccak256 hash of the public key
    public_key_hash: bytes = util.hashlib.sha3_256(public_key).digest();

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

    return calculate_checksum(address) == address[21:]


class Address(util.Model):
    """
    NEM address.

    An address is derived from the public key and network type, and
    uniquely identifies a NEM account.
    """

    def __init__(self, address: str) -> None:
        """
        :param address: Base32-encoded, human-readable address.
        """
        plain = address.strip().upper().replace('-', '')
        if len(plain) != 40:
            raise ValueError("{} does not represent a valid raw address".format(address))
        self._address = plain
        self._network_type = NetworkType.create_from_raw_address(plain)

    @property
    def address(self) -> str:
        """Get human readable (raw) address."""
        return self._address

    @property
    def encoded(self) -> bytes:
        """Get encoded address."""
        return util.b32decode(self.address)

    @property
    def network_type(self) -> 'NetworkType':
        """Get network type."""
        return self._network_type

    networkType = util.undoc(network_type)

    @classmethod
    def create_from_raw_address(cls, address: str) -> 'Address':
        """
        Create Address from human-readable, raw address.

        :param address: Base32-encoded, human-readable address.
        :return: Address object.
        """

        return Address(address)

    createFromRawAddress = util.undoc(create_from_raw_address)

    @classmethod
    def create_from_encoded(cls, address: bytes) -> 'Address':
        """
        Create Address from encoded address.

        :param address: Base32-decoded address bytes.
        :return: Address object.
        """

        if len(address) != 25:
            raise ValueError("{} does not represent a valid encoded address".format(address))
        raw_address = util.b32encode(address)
        return Address.create_from_raw_address(raw_address)

    createFromEncoded = util.undoc(create_from_encoded)

    @classmethod
    def create_from_public_key(cls, public_key: str, network_type: NetworkType) -> 'Address':
        """
        Create Address from the public key and network type.

        :param public_key: Hex-encoded public key (with or without '0x' prefix).
        :param network_type: Network type for address.
        :return: Address object.
        """

        key: bytes = util.unhexlify(public_key, with_prefix=True)
        if len(key) != 32:
            raise ValueError("{} is not a valid public key".format(public_key))
        address: bytes = public_key_to_address(key, network_type)

        return Address.create_from_encoded(address)

    createFromPublicKey = util.undoc(create_from_public_key)

    def plain(self) -> str:
        """Get plain representation of address as base32-decoded string."""

        return self.address

    def pretty(self) -> str:
        """Get pretty representation of address as base32-decoded string."""

        return u'-'.join(chunks(self.address, 6))

    def is_valid(self) -> bool:
        """Check if address is valid."""

        return is_valid_address(self.encoded)

    isValid = util.undoc(is_valid)

    def tie(self):
        """Create tuple from fields."""

        return self.address, self.network_type

    def __repr__(self) -> str:
        return 'Address(address={!r}, network_type={!r})'.format(*self.tie())

    def __str__(self) -> str:
        return 'Address(address={!s}, network_type={!s})'.format(*self.tie())

    def __eq__(self, other) -> bool:
        if not isinstance(other, Address):
            return False
        return self.tie() == other.tie()

    def to_dto(self) -> str:
        return self.address

    to_dto.__doc__ = util.Model.to_dto.__doc__

    @classmethod
    def from_dto(cls, data: str) -> 'Address':
        return cls.create_from_raw_address(data)

    from_dto.__doc__ = util.Model.from_dto.__doc__

    def to_catbuffer(self) -> bytes:
        return self.encoded

    to_catbuffer.__doc__ = util.Model.to_catbuffer.__doc__

    @classmethod
    def from_catbuffer(cls, data: bytes) -> 'Address':
        assert len(data) == 25
        return cls.create_from_encoded(data)

    from_catbuffer.__doc__ = util.Model.from_catbuffer.__doc__
