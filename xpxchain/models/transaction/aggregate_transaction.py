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
from .inner_transaction import InnerTransaction, InnerTransactionList
from .registry import register_transaction
from .signed_transaction import SignedTransaction
from .transaction import Transaction
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.account import Account
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from .recipient import Recipient
from ..mosaic.mosaic import Mosaic
from ... import util

__all__ = ['AggregateTransaction', 'AggregateBondedTransaction', 'AggregateCompleteTransaction']

import logging
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

Cosignature = AggregateTransactionCosignature
Cosignatures = typing.Sequence[Cosignature]
TYPES = (
    TransactionType.AGGREGATE_BONDED,
    TransactionType.AGGREGATE_COMPLETE,
)


@util.inherit_doc
@util.dataclass(frozen=True)
class AggregateTransaction(Transaction):
    """
    Transaction containing multiple inner transactions.

    :param network_type: Network type.
    :param type: Transaction type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param inner_transactions: Inner transactions to be included.
    :param cosignatures: Transaction cosigner signatures.
    :param signature: (Optional) Transaction signature.
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    inner_transactions: InnerTransactionList
    cosignatures: Cosignatures

    def __init__(
        self,
        network_type: NetworkType,
        type: TransactionType,
        version: TransactionVersion,
        deadline: Deadline,
        max_fee: int = 0,
        ####fee_strategy: typing.Optional[util.FeeCalculationStrategy] = util.FeeCalculationStrategy.ZERO,
        inner_transactions: typing.Optional[InnerTransactionList] = None,
        #cosignatures: typing.Optional[Cosignatures] = None,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None,
    ) -> None:
        if type not in TYPES:
            raise ValueError('Invalid transaction type.')
        super().__init__(
            type,
            network_type,
            version,
            deadline,
            max_fee,
            ####fee_strategy,
            signature,
            signer,
            transaction_info,
        )
        self._set('inner_transactions', inner_transactions or [])
        #self._set('cosignatures', cosignatures or [])

    @classmethod
    def create_complete(
        cls,
        deadline: Deadline,
        inner_transactions: typing.Optional[InnerTransactionList],
        network_type: NetworkType,
        cosignatures: typing.Optional[Cosignatures] = None,
        max_fee: int = 0,
        ####fee_strategy: typing.Optional[util.FeeCalculationStrategy] = util.FeeCalculationStrategy.ZERO
    ):
        """
        Create aggregate complete transaction object.

        :param deadline: Deadline to include transaction.
        :param inner_transactions: Inner transactions to be included.
        :param cosignatures: Transaction cosigner signatures.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """

        return cls(
            network_type,
            TransactionType.AGGREGATE_COMPLETE,
            TransactionVersion.AGGREGATE_COMPLETE,
            deadline,
            max_fee,
            ####fee_strategy,
            inner_transactions,
            cosignatures,
        )

    @classmethod
    def create_bonded(
        cls,
        deadline: Deadline,
        inner_transactions: typing.Optional[InnerTransactionList],
        network_type: NetworkType,
        cosignatures: typing.Optional[Cosignatures] = None,
        max_fee: int = 0,
        ####fee_strategy: typing.Optional[util.FeeCalculationStrategy] = util.FeeCalculationStrategy.ZERO
    ):
        """
        Create aggregate bonded transaction object.

        :param deadline: Deadline to include transaction.
        :param inner_transactions: Inner transactions to be included.
        :param cosignatures: Transaction cosigner signatures.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """

        return cls(
            network_type,
            TransactionType.AGGREGATE_BONDED,
            TransactionVersion.AGGREGATE_BONDED,
            deadline,
            max_fee,
            ####fee_strategy,
            inner_transactions,
            cosignatures,
        )

    # SIGNING

#    def sign_with(
#        self, 
#        account: Account,
#        gen_hash: typing.AnyStr
#    ) -> SignedTransaction:
#        """
#        Sign transaction.
#
#        :param account: Escrow account.
#        :param gen_hash: Generation hash
#        """
#
#        transaction = self.to_catbuffer()
#        payload = account.sign(transaction, gen_hash)
#        hash = self.transaction_hash(payload, gen_hash)
#
#        return SignedTransaction(
#            payload,
#            hash,
#            account.public_key,
#            self.type,
#            self.network_type
#        )

    def sign_transaction_with_cosignatories(
        self,
        initiator: Account,
        gen_hash: typing.AnyStr,
        cosignatories: typing.Optional[typing.Sequence[Account]] = None,
        fee_strategy: util.FeeCalculationStrategy = util.FeeCalculationStrategy.ZERO,
    ) -> SignedTransaction:
        """
        Sign transaction with cosignatories.

        :param initiator_account: Initiator account.
        :param gen_hash: Generation hash
        :param cosignatories: Sequence of accounts cosigning transaction.
        """

        transaction = self.to_catbuffer(fee_strategy=fee_strategy)
      
        if (cosignatories):
            COSIGNATURE_SIZE = 96
            new_fee = util.calculate_fee(fee_strategy, self.max_fee, self.catbuffer_size() + COSIGNATURE_SIZE * len(cosignatories))
            
            if (self.max_fee != new_fee):
                transaction = transaction[0:106] + new_fee.to_bytes(8, 'little') + transaction[114:]
                
        payload = initiator.sign(transaction, gen_hash) #type: ignore
        hash = self.transaction_hash(payload, gen_hash) #type: ignore

        if (cosignatories):
            for cosignatory in cosignatories:
                payload += util.decode_hex(cosignatory.public_key)
                payload += cosignatory.sign_data(hash)

            new_size = len(payload)
            payload = new_size.to_bytes(4, 'little') + payload[4:]

        return SignedTransaction( #type: ignore
            payload,
            hash,
            initiator.public_key,
            self.type,
            self.network_type
        )

#    def signed_by_account(self, public_account: PublicAccount) -> bool:
#        """
#        Check if account has signed transaction.
#
#        :param public_account: Signer public account.
#        """
#        return (
#            public_account == self.signer
#            or any(i.signer == public_account for i in self.cosignatures)
#        )

    # AGGREGATE

    def to_aggregate(self, signer: PublicAccount):
        raise TypeError('Aggregate transaction cannot be embedded.')

    # CATBUFFER

    def inner_transactions_size(self) -> int:
        """Get payload size, the size in bytes of all sub-transactions."""
        return sum(i.catbuffer_size() for i in self.inner_transactions)

    def cosignatures_size(self) -> int:
        """Get the size in bytes of all cosignatures."""
        return sum(i.CATBUFFER_SIZE for i in self.cosignatures)

    def catbuffer_size_specific(self) -> int:
        # 4 extra bytes for the payload size.
        # The payload size is the size from all inner transactions.
        extra_size = util.U32_BYTES
        payload_size = self.inner_transactions_size()
        #cosignatures_size = self.cosignatures_size()
        #return extra_size + payload_size + cosignatures_size
        return extra_size + payload_size

    def to_inner_transactions_bytes(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Get the serialized byte array of all sub-transactions."""

        return util.Model.sequence_to_catbuffer(
            self.inner_transactions,
            network_type
        )

    def to_cosignatures_bytes(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Get the serialized byte array of all cosignatures."""

        return util.Model.sequence_to_catbuffer(
            self.cosignatures,
            network_type
        )

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export transfer-specific data to catbuffer."""

        # uint32_t payload_size
        # uint8_t[payload_size] transactions
        # uint8_t[size - payload_size] cosignatures
        payload_size = util.u32_to_catbuffer(self.inner_transactions_size())
        transactions = self.to_inner_transactions_bytes(network_type)
        #cosignatures = self.to_cosignatures_bytes(network_type)
        #return payload_size + transactions + cosignatures
        return payload_size + transactions

    def load_inner_transactions_bytes(
        self,
        data: bytes,
        size: int,
        network_type: NetworkType,
    ) -> bytes:
        """Load inner transactions data from catbuffer."""

        transactions = []
        subdata = data[:size]
        while subdata:
            # This will hard-error if the transaction is invalid,
            # or cut-off, since every deserializer checks the input
            # is valid.
            value, subdata = InnerTransaction.create_from_catbuffer_pair(
                subdata,
                network_type
            )
            transactions.append(value)
        return data[size:]

    def load_cosignatures_bytes(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load cosignatures data from catbuffer."""

        count = len(data) // Cosignature.CATBUFFER_SIZE
        value, data = Cosignature.sequence_from_catbuffer_pair(data, count, network_type)
        self._set('cosignatures', value)
        return data

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load transfer-specific data data from catbuffer."""

        raise NotImplementedError

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'transactions'}
        return cls.validate_dto_required(data, required_keys)

	
    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        raise NotImplementedError

    
    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        inner_transactions = [InnerTransaction.create_from_dto(x, network_type) for x in data['transactions']]

        self._set('inner_transactions', inner_transactions)


@util.inherit_doc
@register_transaction('AGGREGATE_BONDED')
class AggregateBondedTransaction(AggregateTransaction):

    @classmethod
    def create(
        cls,
        deadline: Deadline,
        inner_transactions: typing.Optional[InnerTransactionList],
        cosignatures: Cosignatures,
        network_type: NetworkType,
        max_fee: int = 0,
        ####fee_strategy: typing.Optional[util.FeeCalculationStrategy] = util.FeeCalculationStrategy.ZERO,
    ):
        """
        Create aggregate bonded transaction object.

        :param deadline: Deadline to include transaction.
        :param inner_transactions: Inner transactions to be included.
        :param cosignatures: Transaction cosigner signatures.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """
        return cls.create_bonded(
            deadline,
            inner_transactions,
            network_type,
            cosignatures,
            max_fee,
            ####fee_strategy,
        )


@util.inherit_doc
@register_transaction('AGGREGATE_COMPLETE')
class AggregateCompleteTransaction(AggregateTransaction):

    @classmethod
    def create(
        cls,
        deadline: Deadline,
        inner_transactions: typing.Optional[InnerTransactionList],
        cosignatures: typing.Optional[Cosignatures],
        network_type: NetworkType,
        max_fee: int = 0,
        ####fee_strategy: typing.Optional[util.FeeCalculationStrategy] = util.FeeCalculationStrategy.ZERO,
    ):
        """
        Create aggregate complete transaction object.

        :param deadline: Deadline to include transaction.
        :param inner_transactions: Inner transactions to be included.
        :param cosignatures: Transaction cosigner signatures.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """
        return cls.create_complete(
            deadline,
            inner_transactions,
            cosignatures,
            network_type,
            max_fee,
            ####fee_strategy,
        )
