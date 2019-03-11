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

import struct
import typing

from nem2 import util
from .transaction import Transaction
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType


@util.inherit_doc
class InnerTransaction(Transaction):
    """
    Transaction with an embedded signer for aggregate transactions.

    Produces embedded transactions.
    """

    __slots__ = ()

    @staticmethod
    def shared_entity_size() -> int:
        return 40

    def to_catbuffer_shared(self, size) -> bytes:
        """
        Serialize shared transaction data to catbuffer interchange format.

        :param size: Entity size.
        """

        # uint32_t size
        # uint8_t[32] signer
        # uint8_t version
        # uint8_t network_type
        # uint16_t type
        buffer = bytearray(self.shared_entity_size())
        buffer[0:4] = struct.pack('<I', size)
        buffer[4:36] = util.unhexlify(self.signer.public_key)
        buffer[36:37] = self.version.to_catbuffer()
        buffer[37:38] = self.network_type.to_catbuffer()
        buffer[38:40] = self.type.to_catbuffer()

        return bytes(buffer)

    def load_catbuffer_shared(self, data: bytes) -> typing.Tuple[int, bytes]:
        """Load shared transaction data from catbuffer."""

        assert len(data) >= self.shared_entity_size()

        # uint32_t size
        # uint8_t[32] signer
        # uint8_t version
        # uint8_t network_type
        # uint16_t type
        total_size = struct.unpack('<I', data[:4])[0]
        public_key = data[4:36]
        version = TransactionVersion.from_catbuffer(data[36:37])[0]
        network_type = NetworkType.from_catbuffer(data[37:38])[0]
        type = TransactionType.from_catbuffer(data[38:40])[0]

        object.__setattr__(self, 'type', type)
        object.__setattr__(self, 'network_type', network_type)
        object.__setattr__(self, 'version', version)
        object.__setattr__(self, 'deadline', None)
        object.__setattr__(self, 'fee', None)
        object.__setattr__(self, 'signature', None)
        if public_key != bytes(32):
            signer = PublicAccount.create_from_public_key(util.hexlify(public_key), network_type)
            object.__setattr__(self, 'signer', signer)
        else:
            object.__setattr__(self, 'signer', None)
        object.__setattr__(self, 'signer', signer)
        object.__setattr__(self, 'transaction_info', signer)

        return total_size, data[self.shared_entity_size():]
