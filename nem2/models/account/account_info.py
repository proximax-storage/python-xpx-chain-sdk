"""
    account_info
    ============

    Account data and metadata pair.

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

from .account_metadata import AccountMetadata
from .address import Address
from .public_account import PublicAccount
from ..blockchain.network_type import OptionalNetworkType
from ..mosaic.mosaic import Mosaic, MosaicList
from ... import util

__all__ = ['AccountInfo']


@util.inherit_doc
@util.dataclass(frozen=True)
class AccountInfo(util.DTO):
    """
    Basic information describing an account.

    :param meta: Account metadata.
    :param address: Account address.
    :param address_height: Chain height when address was published.
    :param public_key: Account public key.
    :param public_key_height: Chain height when public key was published.
    :param mosaics: List of mosaics owned by account.
    :param importance: Importance of the account.
    :param importance_height: Importance height of the account.

    DTO Format:
        .. code-block:: yaml

            AccountDTO:
                # Hex(Address) (50-bytes)
                address: string
                addressHeight: UInt64DTO
                # Hex(PublicKey) (64-bytes)
                publicKey: string
                publicKeyHeight: UInt64DTO
                mosaics: MosaicDTO[]
                importance: UInt64DTO
                importanceHeight: UInt64DTO

            AccountInfoDTO:
                meta: AccountMetaDTO
                account: AccountDTO
    """

    meta: AccountMetadata
    address: Address
    address_height: int
    public_key: str
    public_key_height: int
    mosaics: MosaicList
    importance: int
    importance_height: int

    @property
    def public_account(self) -> PublicAccount:
        """Get public account."""
        return PublicAccount(self.address, self.public_key)

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        meta = self.meta.to_dto(network_type)
        account = {
            'address': util.hexlify(self.address.encoded),
            'addressHeight': util.u64_to_dto(self.address_height),
            'publicKey': self.public_key,
            'publicKeyHeight': util.u64_to_dto(self.public_key_height),
            'mosaics': Mosaic.sequence_to_dto(self.mosaics, network_type),
            'importance': util.u64_to_dto(self.importance),
            'importanceHeight': util.u64_to_dto(self.importance_height),
        }

        return {
            'meta': meta,
            'account': account,
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        account = data['account']
        return cls(
            meta=AccountMetadata.create_from_dto(data['meta'], network_type),
            address=Address.create_from_encoded(account['address']),
            address_height=util.u64_from_dto(account.get('addressHeight', [0, 0])),
            public_key=account['publicKey'],
            public_key_height=util.u64_from_dto(account.get('publicKeyHeight', [0, 0])),
            mosaics=Mosaic.sequence_from_dto(account.get('mosaics', []), network_type),
            importance=util.u64_from_dto(account.get('importance', [0, 0])),
            importance_height=util.u64_from_dto(account.get('importanceHeight', [0, 0])),
        )
