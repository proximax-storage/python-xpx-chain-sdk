"""
    account
    =======

    Account private key, public key and address.

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
from .public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ... import util
from ...util.signature import ed25519

__all__ = ['Account']


@util.inherit_doc
@util.dataclass(frozen=True)
class Account(util.Object):
    """
    Describe account via private key, public key and account address.

    :param address: Address for the account.
    :param public_key: Hex-encoded or raw bytes for public key.
    :param private_key: Hex-encoded or raw bytes for private key.
    """

    address: Address
    public_key: str
    private_key: str

    def __init__(
        self,
        address: Address,
        public_key: typing.AnyStr,
        private_key: typing.AnyStr,
    ) -> None:
        public_key = util.encode_hex(public_key)
        private_key = util.encode_hex(private_key)
        if len(public_key) != 64:
            raise ValueError("Invalid public key length")
        if len(private_key) != 64:
            raise ValueError("Invalid private key length")
        self._set('address', address)
        self._set('public_key', public_key)
        self._set('private_key', private_key)

    @property
    def network_type(self) -> NetworkType:
        """Get network type."""
        return self.address.network_type

    @property
    def public_account(self) -> PublicAccount:
        """Get public account."""
        return PublicAccount(self.address, self.public_key)

    @classmethod
    def create_from_private_key(
        cls,
        private_key: typing.AnyStr,
        network_type: NetworkType,
    ):
        """
        Generate Account object from private_key and network type.

        :param private_key: Hex-encoded or raw bytes for private key.
        :param network_type: Network type.
        :return: Account object.
        """

        private_key = util.decode_hex(private_key)
        signing_key = ed25519.sha3.SigningKey(private_key)
        public_key = signing_key.get_verifying_key().to_bytes()
        address = Address.create_from_public_key(public_key, network_type)

        return cls(address, public_key, private_key)  # type: ignore

    @classmethod
    def generate_new_account(
        cls,
        network_type: NetworkType,
        entropy=None
    ):
        """
        Generate new NEM account from network type and random bytes.

        :param network_type: Network type.
        :param entropy: (Optional) callable to generate random bytes for secret key.
        :return: Account object.
        """

        if entropy is not None:
            signing_key, verifying_key = ed25519.sha3.create_keypair(entropy)
        else:
            signing_key, verifying_key = ed25519.sha3.create_keypair()

        public_key = verifying_key.to_bytes()
        private_key = signing_key.to_seed()
        address = Address.create_from_public_key(public_key, network_type)

        return cls(address, public_key, private_key)

    def sign(self, transaction: typing.AnyStr, gen_hash: typing.AnyStr) -> bytes:
        """
        Sign transaction using private key.

        :param private_key: Hex-encoded or raw bytes for transaction data.
        :param gen_hash: Nemesis generation hash.
        :return: Signed transaction data.
        """

        transaction = util.decode_hex(transaction, with_prefix=True)

        # Skip first 100 bytes.
        # uint32_t size
        # uint8_t[64] signature
        # uint8_t[32] signer

        signing_bytes = util.unhexlify(gen_hash) + transaction[100:]

        signature = self.sign_data(signing_bytes)
        public_key = util.unhexlify(self.public_key)
        size = transaction[:4]

        return size + signature + public_key + transaction[100:]

    def sign_data(self, data: typing.AnyStr) -> bytes:
        """
        Sign raw data using private key.

        :param private_key: Hex-encoded or raw bytes to sign.
        :return: Raw data signature.
        """

        data = util.decode_hex(data, with_prefix=True)
        private_key = util.unhexlify(self.private_key)
        public_key = util.unhexlify(self.public_key)
        key = ed25519.sha3.SigningKey(private_key + public_key)

        return typing.cast(bytes, key.sign(data))

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
        return self.public_account.verify_signature(data, signature)

    def verify_transaction(
        self,
        transaction: typing.AnyStr
    ) -> bool:
        """
        Verify signed transaction data.

        :param transaction: Hex-encoded or raw bytes for transaction data.
        :return: Boolean representing if the transaction signature was verified.
        """
        return self.public_account.verify_transaction(transaction)
