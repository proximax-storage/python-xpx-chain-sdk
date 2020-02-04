"""
    lock_funds_transaction
    ======================

    Lock-funds transaction.

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
from .signed_transaction import SignedTransaction
from .transaction import Transaction
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ..mosaic.mosaic import Mosaic
from ..mosaic.mosaic_id import MosaicId
from ..namespace.namespace_id import NamespaceId
from ... import util

__all__ = [
    'LockFundsTransaction',
    'LockFundsInnerTransaction',
]


@util.inherit_doc
@util.dataclass(frozen=True)
@register_transaction('LOCK')
class LockFundsTransaction(Transaction):
    """
    Lock-funds transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param mosaic: Locked mosaic.
    :param duration: Duration to lock funds.
    :param signed_transaction: Signed transaction for which funds are locked.
    :param signature: (Optional) Transaction signature (missing if embedded transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    mosaic: Mosaic
    duration: int
    signed_transaction: SignedTransaction

    def __init__(
        self,
        network_type: NetworkType,
        version: TransactionVersion,
        deadline: Deadline,
        mosaic: Mosaic,
        duration: int,
        signed_transaction: SignedTransaction,
        max_fee: int = 0,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None,
    ) -> None:
        if signed_transaction.type != TransactionType.AGGREGATE_BONDED:
            raise ValueError('Signed transaction must be aggregated bonded transaction.')
        super().__init__(
            TransactionType.LOCK,
            network_type,
            version,
            deadline,
            max_fee,
            signature,
            signer,
            transaction_info,
        )
        self._set('mosaic', mosaic)
        self._set('duration', duration)
        self._set('signed_transaction', signed_transaction)

    @classmethod
    def create(
        cls,
        deadline: Deadline,
        mosaic: Mosaic,
        duration: int,
        signed_transaction: SignedTransaction,
        network_type: NetworkType,
        max_fee: int = 0,
    ):
        """
        Create new lock funds transaction.

        :param deadline: Deadline to include transaction.
        :param mosaic: Locked mosaic.
        :param duration: Duration to lock funds.
        :param signed_transaction: Signed transaction for which funds are locked.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """
        return cls(
            network_type,
            TransactionVersion.LOCK,
            deadline,
            mosaic,
            duration,
            signed_transaction,
            max_fee,
        )

    @property
    def hash(self) -> str:
        """Get transaction hash from signed transaction."""
        return self.signed_transaction.hash

    @property
    def mosaic_id(self) -> typing.Union[MosaicId, NamespaceId]:
        """Get mosaic ID from mosaic."""
        return self.mosaic.id

    @property
    def amount(self) -> int:
        """Get mosaic amount from mosaic."""
        return self.mosaic.amount

    # CATBUFFER

    def catbuffer_size_specific(self) -> int:
        mosaic_size = Mosaic.CATBUFFER_SIZE
        duration_size = util.U64_BYTES
        hash_size = util.U8_BYTES * 32
        return mosaic_size + duration_size + hash_size

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export lock funds-specific data to catbuffer."""

        # Mosaic mosaic
        # uint64 duration
        # uint8[32] hash
        mosaic = self.mosaic.to_catbuffer(network_type)
        duration = util.u64_to_catbuffer(self.duration)
        hash = util.unhexlify(self.hash)
        return mosaic + duration + hash

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load lock funds-specific data data from catbuffer."""

        # Mosaic mosaic
        # uint64 duration
        # uint8[32] hash
        mosaic, data = Mosaic.create_from_catbuffer_pair(data, network_type)
        duration = util.u64_from_catbuffer(data[:util.U64_BYTES])
        data = data[util.U64_BYTES:]
        hash = data[:util.U8_BYTES * 32]
        data = data[util.U8_BYTES * 32:]
        signed_transaction = SignedTransaction.create_from_announced(
            hash,
            TransactionType.AGGREGATE_BONDED,
            network_type
        )

        self._set('mosaic', mosaic)
        self._set('duration', duration)
        self._set('signed_transaction', signed_transaction)

        return data

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'mosaicId', 'amount', 'duration', 'hash'}
        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        return {
            'mosaicId': util.u64_to_dto(int(self.mosaic_id)),
            'amount': util.u64_to_dto(self.amount),
            'duration': util.u64_to_dto(self.duration),
            'hash': self.hash,
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        mosaic_id = MosaicId(util.u64_from_dto(data['mosaicId']))
        amount = util.u64_from_dto(data['amount'])
        duration = util.u64_from_dto(data['duration'])
        signed_transaction = SignedTransaction.create_from_announced(
            data['hash'],
            TransactionType.AGGREGATE_BONDED,
            network_type
        )
        self._set('mosaic', Mosaic(mosaic_id, amount))
        self._set('duration', duration)
        self._set('signed_transaction', signed_transaction)


@register_transaction('LOCK')
class LockFundsInnerTransaction(InnerTransaction, LockFundsTransaction):
    """Embedded lock funds transaction."""

    __slots__ = ()
