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
import typing

from nem2 import util
from .transaction import Hooks, Transaction
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType

__all__ = ['InnerTransaction']

OptionalNetworkType = typing.Optional[NetworkType]


@util.inherit_doc
class InnerTransaction(Transaction):
    """
    Transaction with an embedded signer for aggregate transactions.

    Produces embedded transactions.
    """

    __slots__ = ()
    # Override the base-implementation, so any classmethods
    # inheriting from (InnerTransaction, cls) use the derived hooks.
    HOOKS: typing.ClassVar[Hooks] = {}

    @staticmethod
    def catbuffer_size_shared() -> int:
        return 40

    def to_catbuffer_shared(
        self,
        size: int,
        network_type: OptionalNetworkType = None,
    ) -> bytes:
        """
        Serialize shared transaction data to catbuffer interchange format.

        :param size: Entity size.
        """

        network_type = self.network_type

        # uint32_t size
        # uint8_t[32] signer
        # uint8_t version
        # uint8_t network_type
        # uint16_t type
        buffer = bytearray(self.catbuffer_size_shared())
        buffer[0:4] = util.u32_to_catbuffer(size)
        buffer[4:36] = self.signer.to_catbuffer(network_type)
        buffer[36:37] = self.version.to_catbuffer(network_type)
        buffer[37:38] = self.network_type.to_catbuffer(network_type)
        buffer[38:40] = self.type.to_catbuffer(network_type)

        return bytes(buffer)

    def load_catbuffer_shared(
        self,
        data: typing.AnyStr,
        network_type: OptionalNetworkType = None,
    ) -> typing.Tuple[int, bytes]:
        """Load shared transaction data from catbuffer."""

        data = util.decode_hex(data, with_prefix=True)
        assert len(data) >= self.catbuffer_size_shared()
        network_type = NetworkType.from_catbuffer(data[37:38])

        # uint32_t size
        # uint8_t[32] signer
        # uint8_t version
        # uint8_t network_type
        # uint16_t type
        total_size = util.u32_from_catbuffer(data[:4])
        public_key = data[4:36]
        signer = PublicAccount.from_catbuffer(public_key, network_type)
        version = TransactionVersion.from_catbuffer(data[36:37])
        type = TransactionType.from_catbuffer(data[38:40])

        self._set('type', type)
        self._set('network_type', network_type)
        self._set('version', version)
        self._set('deadline', None)
        self._set('fee', None)
        self._set('signature', None)
        if public_key != bytes(32):
            self._set('signer', signer)
        else:
            self._set('signer', None)
        self._set('transaction_info', None)

        return total_size, data[self.catbuffer_size_shared():]

    @classmethod
    def from_transaction(
        cls,
        transaction: Transaction,
        signer: PublicAccount
    ) -> InnerTransaction:
        """
        Generate aggregate transaction from regular transaction.

        :param transaction: Non-aggregate transaction.
        :param signer: Account of transaction signer.
        """

        data = transaction.asdict()
        data['signer'] = signer
        data.pop('type')
        return cls(**data)
