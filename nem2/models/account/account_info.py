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
import typing

from nem2 import util
from .account_metadata import AccountMetadata
from .address import Address
from .public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ..mosaic.mosaic import Mosaic

__all__ = ['AccountInfo']

MosaicListType = typing.Sequence[Mosaic]
OptionalNetworkType = typing.Optional[NetworkType]


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
    """

    meta: typing.Optional[AccountMetadata]
    address: Address
    address_height: int
    public_key: str
    public_key_height: int
    mosaics: MosaicListType
    importance: int
    importance_height: int

    @property
    def public_account(self) -> PublicAccount:
        """Get public account."""
        return PublicAccount(self.address, self.public_key)

    publicAccount = util.undoc(public_account)

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'meta': {},
            'account': {
                'address': util.hexlify(self.address.encoded),
                'addressHeight': util.u64_to_dto(self.address_height),
                'publicKey': self.public_key,
                'publicKeyHeight': util.u64_to_dto(self.public_key_height),
                'mosaics': [i.to_dto(network_type) for i in self.mosaics],
                'importance': util.u64_to_dto(self.importance),
                'importanceHeight': util.u64_to_dto(self.importance_height),
            }
        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ) -> AccountInfo:
        assert data['meta'] == {}
        account = data['account']
        mosaics = account.get('mosaics', [])
        return cls(
            meta=None,
            address=Address.create_from_encoded(util.unhexlify(account['address'])),
            address_height=util.u64_from_dto(account.get('addressHeight', [0, 0])),
            public_key=account['publicKey'],
            public_key_height=util.u64_from_dto(account.get('publicKeyHeight', [0, 0])),
            mosaics=[Mosaic.from_dto(i, network_type) for i in mosaics],
            importance=util.u64_from_dto(account.get('importance', [0, 0])),
            importance_height=util.u64_from_dto(account.get('importanceHeight', [0, 0])),
        )
