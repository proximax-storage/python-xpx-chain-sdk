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

from .account_meta import AccountMeta
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

    DTO Format:
        .. code-block:: yaml

            AccountDTO:
                # Hex(Address) (50-bytes)
                address: string
                addressHeight: UInt64DTO
                # Hex(PublicKey) (64-bytes)
                publicKey: string
                publicKeyHeight: UInt64DTO
                accountType: UInt64DTO
                linkedAccountType: string
                mosaics: MosaicDTO[]

            AccountInfoDTO:
                meta: AccountMetaDTO
                account: AccountDTO
    """

    meta: AccountMeta
    address: Address
    address_height: int
    public_key: str
    public_key_height: int
    account_type: int
    linked_account_key: str
    mosaics: MosaicList
    snapshots: dict

    @property
    def public_account(self) -> PublicAccount:
        """Get public account."""
        return PublicAccount(self.address, self.public_key)

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'meta', 'account'}
        required_l2 = {
            'address',
            'addressHeight',
            'publicKey',
            'publicKeyHeight',
            'accountType',
            'linkedAccountKey',
            'mosaics',
            'snapshots'
        }
        return (
            # Level 1
            cls.validate_dto_required(data, required_l1)
            and cls.validate_dto_all(data, required_l1)
            # Level 2
            and cls.validate_dto_required(data['account'], required_l2)
            and cls.validate_dto_all(data['account'], required_l2)
        )

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
            'accountType': self.account_type,
            'linkedAccountKey': self.linked_account_key,
            'mosaics': Mosaic.sequence_to_dto(self.mosaics, network_type),
            'snapshots': self.snapshots
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
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        meta = data['meta']
        account = data['account']
        return cls(
            meta=AccountMeta.create_from_dto(meta, network_type),
            address=Address.create_from_encoded(account['address']),
            address_height=util.u64_from_dto(account.get('addressHeight', [0, 0])),
            public_key=account['publicKey'],
            public_key_height=util.u64_from_dto(account.get('publicKeyHeight', [0, 0])),
            account_type=account['accountType'],
            linked_account_key=account['linkedAccountKey'],
            mosaics=Mosaic.sequence_from_dto(account.get('mosaics', []), network_type),
            snapshots=account.get('snapshots', [])
        )
