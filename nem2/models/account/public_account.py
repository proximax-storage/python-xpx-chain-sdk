"""
    public_account
    ==============

    Account public key and address.

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

from .address import Address
from ..blockchain.network_type import NetworkType, OptionalNetworkType
from ... import util
from ...util.signature import ed25519

__all__ = ['PublicAccount']


# TODO(ahuszagh) Change to an object, not an actual Model.
@util.inherit_doc
@util.dataclass(frozen=True)
class PublicAccount(util.Serializable):
    """
    Describe public account information via public key and account address.

    :param address: Address for the account.
    :param public_key: Hex-encoded public key (with or without '0x' prefix).
    """

    address: Address
    public_key: str
    CATBUFFER_SIZE: typing.ClassVar[int] = 32 * util.U8_BYTES

    def __init__(
        self,
        address: Address,
        public_key: typing.AnyStr,
    ) -> None:
        public_key = util.encode_hex(public_key)
        if len(public_key) != 64:
            raise ValueError("Invalid public key length")
        self._set('address', address)
        self._set('public_key', public_key)

    @property
    def network_type(self) -> NetworkType:
        """Get network type."""
        return self.address.network_type

    @classmethod
    def create_from_public_key(
        cls,
        public_key: typing.AnyStr,
        network_type: NetworkType,
    ):
        """
        Create PublicAccount from the public key and network type.

        :param public_key: Hex-encoded or raw bytes for public key.
        :param network_type: Network type for address.
        :return: PublicAccount object.
        """

        public_key = util.encode_hex(public_key)
        address = Address.create_from_public_key(public_key, network_type)

        return cls(address, public_key)

    def verify_signature(
        self,
        data: typing.AnyStr,
        signature: typing.AnyStr
    ) -> bool:
        """
        Verify a signature.

        :param data: Hex-encoded or raw bytes used to generate signature.
        :param public_key: Hex-encoded or raw bytes for signature.
        :return: Boolean representing if the signature was verified.
        """

        data = util.decode_hex(data, with_prefix=True)
        signature = util.decode_hex(signature, with_prefix=True)
        if len(signature) != 64:
            raise ValueError("Signature length is incorrect.")

        public_key = util.unhexlify(self.public_key)
        key = ed25519.sha3.VerifyingKey(public_key)
        try:
            key.verify(signature, data)
            return True
        except ed25519.sha3.BadSignatureError:
            return False

    def verify_transaction(
        self,
        transaction: typing.AnyStr
    ) -> bool:
        """
        Verify signed transaction data.

        :param transaction: Hex-encoded or raw bytes for transaction data.
        :return: Boolean representing if the transaction signature was verified.
        """

        transaction = util.decode_hex(transaction, with_prefix=True)

        # Skip first 100 bytes.
        # uint32_t size
        # uint8_t[64] signature
        # uint8_t[32] signer
        data = transaction[100:]
        signature = transaction[4:68]
        return self.verify_signature(data, signature)

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> str:
        return self.public_key

    @classmethod
    def from_dto(
        cls,
        data: str,
        network_type: OptionalNetworkType = None,
    ):
        assert network_type is not None
        return cls.create_from_public_key(data, network_type)

    def to_catbuffer(
        self,
        network_type: OptionalNetworkType = None,
    ) -> bytes:
        # uint8_t[32] public_key
        return util.unhexlify(self.public_key)

    @classmethod
    def from_catbuffer(
        cls,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ):
        assert network_type is not None
        # uint8_t[32] public_key
        public_key = data[:32]
        return cls.create_from_public_key(public_key, network_type)


PublicAccountList = typing.Sequence[PublicAccount]
