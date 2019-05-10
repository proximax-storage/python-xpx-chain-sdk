"""
    cosignature_transaction
    =======================

    Aggregate transaction to cosign.

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

from .aggregate_transaction import AggregateTransaction
from .cosignature_signed_transaction import CosignatureSignedTransaction
from .transaction_info import TransactionInfo
from ..account.account import Account
from ... import util

__all__ = [
    'CosignatureTransaction',
]


@util.inherit_doc
@util.dataclass(frozen=True)
class CosignatureTransaction(util.Object):
    """Cosignature transaction is used to sign aggregate transactions."""

    transaction: AggregateTransaction

    def __init__(
        self,
        transaction: AggregateTransaction
    ) -> None:
        if transaction.is_unannounced():
            raise ValueError('Transaction to cosign must be announced first.')
        self._set('transaction', transaction)

    @classmethod
    def create(
        cls,
        transaction: AggregateTransaction
    ):
        """
        Create cosignature transaction.

        :param account: Account to sign with.
        """
        return cls(transaction)

    def sign_with(self, account: Account) -> CosignatureSignedTransaction:
        """
        Serialize and sign transaction.

        :param account: Account to sign with.
        """

        transaction_info = self.transaction.transaction_info
        if transaction_info is None:
            raise ValueError('Transaction info not present.')
        parent_hash = typing.cast(TransactionInfo, transaction_info).hash
        if parent_hash is None:
            raise ValueError('Transaction info to cosign has no hash.')

        signature = util.hexlify(account.sign_data(parent_hash))
        signer = account.public_key
        return CosignatureSignedTransaction(parent_hash, signature, signer)
