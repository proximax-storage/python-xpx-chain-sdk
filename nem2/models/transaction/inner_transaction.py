"""
    inner_transaction
    =================

    Transaction with an embedded signer for aggregate transactions.

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
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ... import util

__all__ = ['InnerTransaction']

# We need 3 different transaction base types for `create_from_transaction`.
T1 = typing.TypeVar('T1', bound='TransactionBase')
T2 = typing.TypeVar('T2', bound='TransactionBase')
T3 = typing.TypeVar('T3', bound='TransactionBase')


@util.inherit_doc
class InnerTransaction(TransactionBase):
    """Abstract, embedded transaction base class."""

    __slots__ = ()
    # Overridable classvars.
    TYPE_MAP: typing.ClassVar[TypeMap] = bidict.bidict()
    CATBUFFER: typing.ClassVar[CatbufferFormat] = CatbufferFormat(
        # Layout
        #   uint32_t size
        #   uint8_t[32] signer
        #   uint8_t version
        #   uint8_t network_type
        #   uint16_t type
        slices={
            'size': slice(0, 4),
            'signer': slice(4, 36),
            'version': slice(36, 39),
            'network_type': slice(39, 40),
            'type': slice(40, 42),
        },
        size_shared=42,
    )
    DTO: typing.ClassVar[DTOFormat] = DTOFormat(
        names={
            'signer': 'signer',
            'version': 'version',
            'network_type': 'version',
            'type': 'type',
            'transaction_info': 'meta'
        },
    )

    # AGGREGATE

    @classmethod
    def create_from_transaction(
        cls: typing.Type[T1],
        transaction: T2,
        signer: PublicAccount,
    ) -> T3:
        """
        Generate embedded transaction from non-embedded transaction.

        :param transaction: Non-embedded transaction.
        :param signer: Account of transaction signer.
        """

        data = transaction.asdict(recurse=False)
        data['signer'] = signer
        aggregate_cls: typing.Type[T3] = cls.TYPE_MAP[data.pop('type')]
        return aggregate_cls(**data)

    # CATBUFFER

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
        cb_get('signer')
        cb_get('version')
        cb_get('network_type')
        cb_get('type')

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
        self._set('signature', None)
        cb_set('signer')
        cb_set('version')
        self._set('network_type', network_type)
        cb_set('type')
        self._set('max_fee', None)
        self._set('deadline', None)
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
        cb_get('signer')
        cb_get('version')
        cb_get('network_type')
        cb_get('type')
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
        self._set('signature', None)
        cb_set('signer')
        cb_set('version')
        self._set('network_type', network_type)
        cb_set('type')
        self._set('max_fee', None)
        self._set('deadline', None)
        self._set('transaction_info', None)


InnerTransactionList = typing.Sequence[InnerTransaction]
