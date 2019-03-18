"""
    aggregate_transaction
    =====================

    Transaction containing multiple inner transactions that may be
    initiated by different accounts.

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

from .aggregate_transaction_cosignature import AggregateTransactionCosignature
from .deadline import Deadline
from .inner_transaction import InnerTransaction
from .transaction import Transaction
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType

__all__ = ['AggregateTransaction']

Cosignatures = typing.Sequence[AggregateTransactionCosignature]
InnerTransactions = typing.Sequence[InnerTransaction]
OptionalNetworkType = typing.Optional[NetworkType]


class AggregateTransaction(Transaction):
    """Transaction containing multiple inner transactions."""

    inner_transactions: InnerTransactions
    cosignatures: Cosignatures

    def __init__(
        self,
        network_type: NetworkType,
        type: TransactionType,
        version: TransactionVersion,
        deadline: Deadline,
        fee: int,
        inner_transactions: typing.Optional[InnerTransactions] = None,
        cosignatures: Cosignatures = None,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None,
    ):
        super().__init__(
            type,
            network_type,
            version,
            deadline,
            fee,
            signature,
            signer,
            transaction_info,
        )
        self._set('inner_transactions', inner_transactions or [])
        self._set('cosignatures', cosignatures or [])

    # TODO(ahuszagh)
    # create_complete
    # create_bonded
    # sign_transaction_with_cosignatories
    # signed_by_account

    def catbuffer_size_specific(self) -> int:
        raise NotImplementedError

    def to_catbuffer_specific(
        self,
        network_type: OptionalNetworkType = None,
    ) -> bytes:
        """Export transfer-specific data to catbuffer."""
        # TODO(ahuszagh) Implement...
        raise NotImplementedError

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ) -> bytes:
        """Load transfer-specific data data from catbuffer."""
        # TODO(ahuszagh) Implement...
        raise NotImplementedError


Transaction.HOOKS[TransactionType.AGGREGATE_COMPLETE] = (
    AggregateTransaction.from_catbuffer_pair,
    AggregateTransaction.from_dto,
)

Transaction.HOOKS[TransactionType.AGGREGATE_BONDED] = (
    AggregateTransaction.from_catbuffer_pair,
    AggregateTransaction.from_dto,
)
