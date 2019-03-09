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

import typing

from nem2 import util
from nem2.util.signature import ed25519
from .address import Address
from .public_account import PublicAccount

if typing.TYPE_CHECKING:
    from ..blockchain.network_type import NetworkType


@util.inherit_doc
@util.dataclass(frozen=True)
class Account:
    """
    Describe account via private key, public key and account address.

    :param address: Address for the account.
    :param public_key: Hex-encoded public key (with or without '0x' prefix).
    :param private_key: Hex-encoded private key (with or without '0x' prefix).
    """

    address: 'Address'
    public_key: str
    private_key: str

    def __init__(self, address: Address, public_key: str, private_key: str) -> None:
        if len(public_key) != 64:
            raise ValueError("Invalid public key length")
        if len(private_key) != 64:
            raise ValueError("Invalid private key length")
        object.__setattr__(self, 'address', address)
        object.__setattr__(self, 'public_key', public_key)
        object.__setattr__(self, 'private_key', private_key)

    @property
    def network_type(self) -> 'NetworkType':
        """Get network type."""
        return self.address.network_type

    networkType = util.undoc(network_type)

    @property
    def public_account(self) -> PublicAccount:
        """Get public account."""
        return PublicAccount.create_from_public_key(self.public_key, self.network_type)

    publicAccount = util.undoc(public_account)

    @classmethod
    def create_from_private_key(cls, private_key: str, network_type: 'NetworkType') -> 'Account':
        """
        Generate Account object from private_key and network type.

        :param private_key: Hex-encoded private key (with or without '0x' prefix).
        :param network_type: Network type.
        :return: Account object.
        """

        signing_key = ed25519.sha3.SigningKey(util.unhexlify(private_key))
        public_key = util.hexlify(signing_key.get_verifying_key().to_bytes())
        address = Address.create_from_public_key(public_key, network_type)

        return cls(address, public_key, private_key)

    createFromPrivateKey = util.undoc(create_from_private_key)

    @classmethod
    def generate_new_account(cls, network_type: 'NetworkType', entropy=None) -> 'Account':
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

        public_key = util.hexlify(verifying_key.to_bytes())
        private_key = util.hexlify(signing_key.to_seed())
        address = Address.create_from_public_key(public_key, network_type)

        return cls(address, public_key, private_key)

    generateNewAccount = util.undoc(generate_new_account)

    def sign(self, transaction):
        """
        Sign transaction using private key.

        :param transaction: Transaction data to sign.
        :return: Signed transaction data.
        """
        # TODO(ahuszagh) Implement and annotate the function....
        raise NotImplementedError

    def sign_data(self, data: bytes) -> str:
        """
        Sign raw data using private key.

        :param data: Raw data as bytes.
        :return: Hex-encoded signature of data.
        """

        private_key: bytes = util.unhexlify(self.private_key)
        public_key: bytes = util.unhexlify(self.public_key)
        key = ed25519.sha3.SigningKey(private_key + public_key)

        return util.hexlify(key.sign(data))

    signData = util.undoc(sign_data)
