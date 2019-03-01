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

from nem2 import util
from nem2.util.signature import ed25519
from .address import Address
from ..blockchain.network_type import NetworkType


class PublicAccount:
    """
    NEM public account.

    Describe account via the public key and account address.
    """

    def __init__(self, address: Address, public_key: str) -> None:
        """
        :param address: Address for the account.
        :param public_key: Hex-encoded public key (with or without '0x' prefix).
        """
        self._address = address
        self._public_key = public_key

    @property
    def address(self) -> Address:
        """Get address."""
        return self._address

    @property
    def public_key(self) -> str:
        """Get public key."""
        return self._public_key

    publicKey = util.undoc(public_key)

    @property
    def network_type(self) -> NetworkType:
        """Get network type."""
        return self.address.network_type

    networkType = util.undoc(network_type)

    @classmethod
    def create_from_public_key(cls, public_key: str, network_type: NetworkType):
        """
        Create PublicAccount from the public key and network type.

        :param public_key: Hex-encoded public key (with or without '0x' prefix).
        :param network_type: Network type for address.
        :return: PublicAccount object.
        """

        address = Address.create_from_public_key(public_key, network_type)
        return cls(address, public_key)

    createFromPublicKey = util.undoc(create_from_public_key)

    # TODO(ahuszagh)
    # verifyTransaction?

    def verify_signature(self, data: bytes, signature: str) -> bool:
        """
        Verify a signature.

        :param data: Raw data as bytes.
        :param signature: The signature to verify (hex-encoded).
        :return: Boolean representing if the signature was verified.
        """

        if len(signature) != 128:
            raise ValueError("Signature length is incorrect.")

        public_key: bytes = util.unhexlify(self.public_key)
        signature: bytes = util.unhexlify(signature)

        key = ed25519.sha3.VerifyingKey(public_key)
        try:
            key.verify(signature, data)
            return True
        except ed25519.sha3.BadSignatureError:
            return False

    verifySignature = util.undoc(verify_signature)

    def tie(self):
        """Create tuple from fields."""

        return self.address, self.public_key

    def __repr__(self) -> str:
        return 'PublicAccount(address={!r}, public_key={!r})'.format(*self.tie())

    def __str__(self) -> str:
        return 'PublicAccount(address={!s}, public_key={!s})'.format(*self.tie())

    def __eq__(self, other) -> bool:
        if not isinstance(other, PublicAccount):
            return False
        return self.tie() == other.tie()
