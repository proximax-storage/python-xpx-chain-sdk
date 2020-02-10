"""
    blockchain_upgrade_transaction
    ====================

    Transfer transaction.

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

from .deadline import Deadline
from .inner_transaction import InnerTransaction
from .registry import register_transaction
from .transaction import Transaction
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ... import util

__all__ = [
    'BlockchainUpgradeTransaction',
    'BlockchainUpgradeInnerTransaction',
]


@util.inherit_doc
@util.dataclass(frozen=True)
@register_transaction('BLOCKCHAIN_UPGRADE')
class BlockchainUpgradeTransaction(Transaction):
    """
    Blockchain upgrade transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param new_blockchain_version: New blockchain version
    :param upgrade_period: Upgrade period
    :param signature: (Optional) Transaction signature (missing if embedded transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    new_blockchain_version: int
    upgrade_period: int

    def __init__(
        self,
        network_type: NetworkType,
        version: TransactionVersion,
        deadline: Deadline,
        new_blockchain_version: int,
        upgrade_period: int,
        max_fee: int = 0,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None
    ) -> None:
        super().__init__(
            TransactionType.TRANSFER,
            network_type,
            version,
            deadline,
            max_fee,
            signature,
            signer,
            transaction_info
        )
        self._set('new_blockchain_version', new_blockchain_version)
        self._set('upgrade_period', new_blockchain_version)

    @classmethod
    def create(
        cls,
        deadline: Deadline,
        network_type: NetworkType,
        new_blockchain_version: int,
        upgrade_period: int,
        max_fee: int = 0,
    ):
        """
        Create new network configuration transaction.

        :param deadline: Deadline to include transaction.
        :param network_type: Network type.
        :param new_blockchain_version: New blockchain version
        :param upgrade_period: Upgrade period
        :param max_fee: (Optional) Max fee defined by sender.
        """
        return cls(
            network_type,
            TransactionVersion.TRANSFER,
            deadline,
            new_blockchain_version,
            upgrade_period,
            max_fee,
        )

    # CATBUFFER

    def catbuffer_size_specific(self) -> int:
        new_blockchain_version_size = util.U64_BYTES
        upgrade_period_size = util.U64_BYTES

        return new_blockchain_version_size + upgrade_period_size

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export transfer-specific data to catbuffer."""

        # uint64_t upgrade_period
        # uint64_t new_blockchain_version
        upgrade_period = util.u64_to_catbuffer(self.upgrade_period)
        new_blockchain_version = util.u64_to_catbuffer(self.new_blockchain_version)

        return upgrade_period + new_blockchain_version

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load transfer-specific data from catbuffer."""

        # uint64_t upgrade_period
        # uint64_t new_blockchain_version
        upgrade_period = util.u64_from_catbuffer(data[:util.U64_BYTES])
        data = data[util.U64_BYTES:]
        new_blockchain_version = util.u64_from_catbuffer(data[:util.U64_BYTES])
        data = data[util.U64_BYTES:]

        self._set('upgrade_period', upgrade_period)
        self._set('new_blockchain_version', new_blockchain_version)

        return data

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'newBlockchainVersion', 'upgradePeriod'}

        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        return {
            'newBlockchainVersion': util.u64_to_dto(self.new_blockchain_version),
            'upgradePeriod': util.u64_to_dto(self.upgrade_period),
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        new_blockchain_version = util.u64_from_dto(data['newBlockchainVersion'])
        upgrade_period = util.u64_from_dto(data['upgradePeriod'])

        self._set('new_blockchain_version', new_blockchain_version)
        self._set('upgrade_period', upgrade_period)


@register_transaction('BLOCKCHAIN_UPGRADE')
class BlockchainUpgradeInnerTransaction(InnerTransaction, BlockchainUpgradeTransaction):
    """Embedded blockchain upgrade transaction."""

    __slots__ = ()
