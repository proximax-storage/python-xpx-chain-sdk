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

import struct
import typing

from nem2 import util

if typing.TYPE_CHECKING:
    from .aggregate_transaction_info import AggregateTransactionInfo
    from .deadline import Deadline
    from .inner_transaction import InnerTransaction
    from .transaction_info import TransactionInfo
    from .transaction_type import TransactionType
    from .transaction_version import TransactionVersion
    from ..account.public_account import PublicAccount
    from ..blockchain.network_type import NetworkType

TransactionInfoType = typing.Union['TransactionInfo', 'AggregateTransactionInfo']


# TODO(ahuszagh) Model??
@util.inherit_doc
@util.dataclass(frozen=True)
class Transaction(util.Model):
    """
    Abstract transaction base class.

    :param type: Transaction type.
    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param fee: Fee for the transaction. Higher fees increase transaction priority.
    :param signature: Transaction signature (missing if aggregate transaction).
    :param signer: Account of transaction creator.
    :param transaction_info: Transaction metadata.
    """

    type: 'TransactionType'
    network_type: 'NetworkType'
    version: 'TransactionVersion'
    deadline: 'Deadline'
    fee: int
    signature: typing.Optional[str]
    signer: typing.Optional['PublicAccount']
    transaction_info: typing.Optional[TransactionInfoType]

    def sign_with(self, account: 'Account') -> 'SignedTransaction':
        """
        Serialize and sign transaction.

        :param account: Account to sign transaction.
        """
        catbuf = self.to_catbuffer()
        # signTransaction
        # SignedTransaction
        raise NotImplementedError

    signWith = util.undoc(sign_with)

    @staticmethod
    def shared_entity_size(embedded=False) -> int:
        """Get the base size of the transaction entity."""
        return 40 if embedded else 120

    sharedEntitySize = util.undoc(shared_entity_size)

    def entity_size(self, embedded=False) -> int:
        """Get the total size of the transaction entity."""
        raise NotImplementedError

    entitySize = util.undoc(entity_size)

    def to_catbuffer(self, embedded=False) -> bytes:
        """
        Serialize object to catbuffer interchange format.

        :param embedded: Is embedded transaction.
        """

        total_size = self.entity_size(embedded)
        shared = self.to_catbuffer_shared(total_size, embedded)
        specific = self.to_catbuffer_specific()

        return shared + specific

    def toCatbuffer(self, embedded=False) -> bytes:
        return self.to_catbuffer(embedded)

    def to_catbuffer_shared(self, size, embedded=False) -> bytes:
        """
        Serialize shared transaction data to catbuffer interchange format.

        :param size: Entity size.
        :param embedded: Is embedded transaction.
        """

        buffer = bytearray(self.base_entity_size())
        if embedded:
            # uint32_t size
            # uint8_t[32] signer
            # uint16_t version
            # uint16_t type
            buffer[0:4] = struct.pack('<I', size)
            buffer[4:36] = util.unhexlify(self.signer.public_key)
            buffer[36:38] = self.version.to_catbuffer()
            buffer[38:40] = self.type.to_catbuffer()
        else:
            # uint32_t size
            # uint8_t[64] signature
            # uint8_t[32] signer
            # uint16_t version
            # uint16_t type
            # uint64_t fee
            # uint64_t deadline
            buffer[0:4] = struct.pack('<I', size)
            buffer[4:68] = util.unhexlify(self.signature)
            buffer[68:100] = util.unhexlify(self.signer.public_key)
            buffer[100:102] = self.version.to_catbuffer()
            buffer[102:104] = self.type.to_catbuffer()
            buffer[104:112] = struct.pack('<Q', self.fee)
            buffer[112:120] = self.deadline.to_catbuffer()

        return bytes(buffer)

    toCatbufferShared = util.undoc(to_catbuffer_shared)

    def to_catbuffer_specific(self) -> bytes:
        """Serialize transaction-specific data to catbuffer interchange format."""
        raise NotImplementedError

    toCatbufferSpecific = util.undoc(to_catbuffer_specific)

    @classmethod
    def from_catbuffer(cls, data: bytes, embedded=False) -> 'Transaction':
        """
        Deserialize object from catbuffer interchange format.

        :param data: Transaction data in catbuffer interchange format.
        :param embedded: Is embedded transaction.
        """
        raise NotImplementedError

    @classmethod
    def fromCatbuffer(cls, data: bytes, embedded=False) -> 'Transaction':
        return cls.from_catbuffer(data, embedded)

    # TODO(ahuszagh) Need some sort of loader...

    def aggregate_transaction(self) -> bytes:
        """Build aggregate transaction."""
        raise NotImplementedError

    aggregateTransaction = util.undoc(aggregate_transaction)

    def to_aggregate(self, signer: 'PublicAccount') -> 'InnerTransaction':
        """Convert transaction to inner transaction."""
        import pdb; pdb.set_trace()
        # TODO(ahuszagh) How do I do this??
        # Need to copy over methods.
        # Metaclass??? Lols fun...
        raise NotImplementedError

    toAggregate = util.undoc(to_aggregate)

    def is_unconfirmed(self) -> bool:
        """Is transaction pending to be included."""
        info = self.transaction_info
        return info is not None and info.is_unconfirmed()

    isUnconfirmed = util.undoc(is_unconfirmed)

    def is_confirmed(self) -> bool:
        """Is transaction already included."""
        info = self.transaction_info
        return info is not None and info.is_confirmed()

    isConfirmed = util.undoc(is_confirmed)

    def has_missing_signatures(self) -> bool:
        """Does the transaction have missing signatures."""
        info = self.transaction_info
        return info is not None and info.has_missing_signatures()

    hasMissingSignatures = util.undoc(has_missing_signatures)

    def is_unannounced(self) -> bool:
        """Is transaction not known by the network."""
        return self.transaction_info is None

    isUnannounced = util.undoc(is_unannounced)

    # TODO(ahuszagh) Finish the implementation...
    # hasMissingSignatures
    # reapplyGiven

    # TODO(ahuszagh) Implement
    # from_dto
    # to_dto
