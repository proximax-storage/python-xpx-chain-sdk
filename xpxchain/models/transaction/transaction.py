"""
    transaction
    ===========

    Abstract base class for transactions.

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
import bidict
import typing

from .base import TransactionBase, TypeMap
from .format import CatbufferFormat, DTOFormat
from .inner_transaction import InnerTransaction
from .signed_transaction import SignedTransaction
from ..account.account import Account
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ... import util

__all__ = ['Transaction']


@util.inherit_doc
class Transaction(TransactionBase):
    """Abstract, non-embedded transaction base class."""

    __slots__ = ()
    # Overridable classvars.
    TYPE_MAP: typing.ClassVar[TypeMap] = bidict.bidict()
    CATBUFFER: typing.ClassVar[CatbufferFormat] = CatbufferFormat(
        # Layout
        #   uint32_t size
        #   uint8_t[64] signature
        #   uint8_t[32] signer
        #   uint8_t[3] version
        #   uint8_t network_type
        #   uint16_t type
        #   uint64_t max_fee
        #   uint64_t deadline
        slices={
            # Main fields.
            'size': slice(0, 4),
            'signature': slice(4, 68),
            'signer': slice(68, 100),
            'version': slice(100, 103),
            'network_type': slice(103, 104),
            'type': slice(104, 106),
            'max_fee': slice(106, 114),
            'deadline': slice(114, 122),
            # Helpers.
            'signature_half': slice(4, 36),
            'signing_bytes': slice(100, None),
        },
        size_shared=122,
    )
    DTO: typing.ClassVar[DTOFormat] = DTOFormat(
        names={
            'signature': 'signature',
            'signer': 'signer',
            'version': 'version',
            'network_type': 'version',
            'type': 'type',
            'max_fee': 'maxFee',
            'deadline': 'deadline',
            'transaction_info': 'meta',
        },
    )

    # SIGNING

    def sign_with(
        self,
        account: Account,
        gen_hash: typing.AnyStr,
        fee_strategy: util.FeeCalculationStrategy = util.FeeCalculationStrategy.MEDIUM,
    ) -> SignedTransaction:
        """
        Serialize and sign transaction.

        :param account: Account to sign transaction.
        :param gen_hash: Nemesis generation hash.
        :return: Signed transaction data,
        """

        # Serialize transaction data, sign, and generate a hash.
        transaction = self.to_catbuffer(fee_strategy=fee_strategy)
        payload = account.sign(transaction, gen_hash)  # type: ignore

        hash = self.transaction_hash(payload, gen_hash)  # type: ignore
        return SignedTransaction(  # type: ignore
            payload,
            hash,
            account.public_key,
            self.type,
            self.network_type
        )

    @staticmethod
    def transaction_hash(transaction: typing.AnyStr, gen_hash: typing.AnyStr) -> str:
        """Generate transaction hash from signed transaction payload."""

        # Decode the data.
        transaction = util.decode_hex(transaction, with_prefix=True)

        # Extract the first half of the signature, the signer, and the
        # remaining signing bytes, sign them, and get the hash.
        slices = Transaction.CATBUFFER.slices

        signature_half = transaction[slices['signature_half']]
        signer = transaction[slices['signer']]
        rest = transaction[slices['signing_bytes']]

        data = signature_half + signer + util.decode_hex(gen_hash, with_prefix=True) + rest
        hash = util.hashlib.sha3_256(data).hexdigest()

        return typing.cast(str, hash)

    # AGGREGATE

    def aggregate_transaction(
        self,
        signer: typing.Optional[PublicAccount] = None,
    ) -> bytes:
        """Build aggregate transaction."""

        if signer is None:
            signer = self.signer
        if signer is None:
            raise ValueError('Cannot create aggregate transaction without signer.')

        transaction = self.to_aggregate(signer).to_catbuffer()
        return typing.cast(bytes, transaction)

    def to_aggregate(self, signer: PublicAccount) -> InnerTransaction:
        """Convert transaction to inner transaction."""
        return InnerTransaction.create_from_transaction(self, signer)

    # CATBUFFER

    def catbuffer_size_specific(self) -> int:
        raise util.AbstractMethodError

    def to_catbuffer_shared(
        self,
        network_type: NetworkType,
    ) -> bytes:
        # Shared data and callbacks.
        data = bytearray(self.catbuffer_size_shared())
        cb = lambda k, v: self.CATBUFFER.save(k, data, v, network_type)
        cb_get = lambda k: cb(k, getattr(self, k))

        # Save shared data.
        cb('size', self.catbuffer_size())
        cb_get('signature')
        cb_get('signer')
        cb_get('version')
        cb_get('network_type')
        cb_get('type')
        cb_get('max_fee')
        cb_get('deadline')

        return bytes(data)

    def load_catbuffer_shared(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        # Shared data and callbacks.
        cb = lambda k: self.CATBUFFER.load(k, data, network_type)
        cb_set = lambda k: self._set(k, cb(k))

        # Load shared data.
        cb_set('signature')
        cb_set('signer')
        cb_set('version')
        self._set('network_type', network_type)
        cb_set('type')
        cb_set('max_fee')
        cb_set('deadline')
        self._set('transaction_info', None)

        return data[self.catbuffer_size_shared():]

    # DTO

    @classmethod
    def validate_dto_shared(cls, data: dict) -> bool:
        required_keys = {
            'version',
            'type',
        }
        return cls.validate_dto_required(data, required_keys)

    def to_dto_shared(
        self,
        network_type: NetworkType,
    ) -> dict:
        # Shared data and callbacks.
        data: dict = {}
        cb = lambda k, v: self.DTO.save(k, data, v, network_type)
        cb_get = lambda k: cb(k, getattr(self, k))

        # Save shared data.
        # Do not export `network_type`, already exported
        # with version.
        cb_get('signature')
        cb_get('signer')
        cb_get('version')
        cb_get('type')
        cb_get('max_fee')
        cb_get('deadline')
        cb_get('transaction_info')

        return data

    def load_dto_shared(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        # Shared data and callbacks.
        cb = lambda k: self.DTO.load(k, data, network_type)
        cb_set = lambda k: self._set(k, cb(k))

        # Load shared data.
        cb_set('signature')
        cb_set('signer')
        cb_set('version')
        self._set('network_type', network_type)
        cb_set('type')
        cb_set('max_fee')
        cb_set('deadline')
        cb_set('transaction_info')
