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
from .deadline import Deadline
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType

if typing.TYPE_CHECKING:
    from .aggregate_transaction_info import AggregateTransactionInfo
    from .inner_transaction import InnerTransaction
    from .signed_transaction import SignedTransaction
    from .transaction_info import TransactionInfo
    from ..account.account import Account

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
    deadline: typing.Optional['Deadline']
    fee: typing.Optional[int]
    signature: typing.Optional[str]
    signer: typing.Optional['PublicAccount']
    transaction_info: typing.Optional[TransactionInfoType]

    def sign_with(self, account: 'Account') -> 'SignedTransaction':
        """
        Serialize and sign transaction.

        :param account: Account to sign transaction.
        """
        # buffer = self.to_catbuffer()
        # signTransaction
        # SignedTransaction
        raise NotImplementedError

    signWith = util.undoc(sign_with)

    @staticmethod
    def shared_entity_size() -> int:
        """Get the base size of the transaction entity."""
        return 120

    sharedEntitySize = util.undoc(shared_entity_size)

    def entity_size(self) -> int:
        """Get the total size of the transaction entity."""
        raise NotImplementedError

    entitySize = util.undoc(entity_size)

    def to_catbuffer(self) -> bytes:
        """
        Serialize object to catbuffer interchange format.

        :param embedded: Is embedded transaction.
        """

        total_size = self.entity_size()
        shared = self.to_catbuffer_shared(total_size)
        specific = self.to_catbuffer_specific()

        return shared + specific

    def to_catbuffer_shared(self, size) -> bytes:
        """
        Serialize shared transaction data to catbuffer interchange format.

        :param size: Entity size.
        """

        # uint32_t size
        # uint8_t[64] signature
        # uint8_t[32] signer
        # uint8_t version
        # uint8_t network_type
        # uint16_t type
        # uint64_t fee
        # uint64_t deadline
        buffer = bytearray(self.shared_entity_size())
        buffer[0:4] = struct.pack('<I', size)
        buffer[4:68] = util.unhexlify(self.signature)
        buffer[68:100] = util.unhexlify(self.signer.public_key)
        buffer[100:101] = self.version.to_catbuffer()
        buffer[101:102] = self.network_type.to_catbuffer()
        buffer[102:104] = self.type.to_catbuffer()
        buffer[104:112] = struct.pack('<Q', self.fee)
        buffer[112:120] = self.deadline.to_catbuffer()

        return bytes(buffer)

    toCatbufferShared = util.undoc(to_catbuffer_shared)

    def to_catbuffer_specific(self) -> bytes:
        """Serialize transaction-specific data to catbuffer interchange format."""
        raise NotImplementedError

    toCatbufferSpecific = util.undoc(to_catbuffer_specific)

    def load_catbuffer_shared(self, data: bytes) -> typing.Tuple[int, bytes]:
        """Load shared transaction data from catbuffer."""

        assert len(data) >= self.shared_entity_size()

        # uint32_t size
        # uint8_t[64] signature
        # uint8_t[32] signer
        # uint8_t version
        # uint8_t network_type
        # uint16_t type
        # uint64_t fee
        # uint64_t deadline
        total_size = struct.unpack('<I', data[:4])[0]
        signature = util.hexlify(data[4:68])
        public_key = util.hexlify(data[68:100])
        version = TransactionVersion.from_catbuffer(data[100:101])[0]
        network_type = NetworkType.from_catbuffer(data[101:102])[0]
        type = TransactionType.from_catbuffer(data[102:104])[0]
        fee = struct.unpack('<Q', data[104:112])[0]
        deadline = Deadline.from_catbuffer(data[112:])[0]
        signer = PublicAccount.create_from_public_key(public_key, network_type)

        object.__setattr__(self, 'type', type)
        object.__setattr__(self, 'network_type', network_type)
        object.__setattr__(self, 'version', version)
        object.__setattr__(self, 'deadline', deadline)
        object.__setattr__(self, 'fee', fee)
        object.__setattr__(self, 'signature', signature)
        object.__setattr__(self, 'signer', signer)
        object.__setattr__(self, 'transaction_info', None)

        return total_size, data[self.shared_entity_size():]

    loadCatbufferShared = util.undoc(load_catbuffer_shared)

    def load_catbuffer_specific(self, data: bytes) -> bytes:
        """Load transaction-specific data data from catbuffer."""
        raise NotImplementedError

    loadCatbufferSpecific = util.undoc(load_catbuffer_specific)

    @classmethod
    def from_catbuffer(cls, data: bytes) -> typing.Tuple['Transaction', bytes]:
        """
        Deserialize object from catbuffer interchange format.

        :param data: Transaction data in catbuffer interchange format.
        :param embedded: Is embedded transaction.
        """
        inst = cls.__new__(cls)
        total_size, data = inst.load_catbuffer_shared(data)
        data = inst.load_catbuffer_specific(data)
        return inst, data

    def aggregate_transaction(self) -> bytes:
        """Build aggregate transaction."""
        raise NotImplementedError

    aggregateTransaction = util.undoc(aggregate_transaction)

    def to_aggregate(self, signer: 'PublicAccount') -> 'InnerTransaction':
        """Convert transaction to inner transaction."""
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
