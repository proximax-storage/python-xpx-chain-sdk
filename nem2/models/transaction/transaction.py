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
import typing

from nem2 import util
from .aggregate_transaction_info import AggregateTransactionInfo
from .deadline import Deadline
from .signed_transaction import SignedTransaction
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.account import Account
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType

OptionalNetworkType = typing.Optional[NetworkType]
TransactionInfoType = typing.Union[TransactionInfo, AggregateTransactionInfo]

# Callback types to register hooks to determine if
LoadCatbuffer = typing.Callable[[bytes, OptionalNetworkType], typing.Tuple['Transaction', bytes]]
LoadDto = typing.Callable[[dict, OptionalNetworkType], 'Transaction']
Hooks = typing.Dict[TransactionType, typing.Tuple[LoadCatbuffer, LoadDto]]


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

    type: TransactionType
    network_type: NetworkType
    version: TransactionVersion
    deadline: typing.Optional[Deadline]
    fee: typing.Optional[int]
    signature: typing.Optional[str]
    signer: typing.Optional[PublicAccount]
    transaction_info: typing.Optional[TransactionInfoType]
    HOOKS: typing.ClassVar[Hooks] = {}

    def sign_with(self, account: Account) -> SignedTransaction:
        """
        Serialize and sign transaction.

        :param account: Account to sign transaction.
        """

        transaction = self.to_catbuffer()
        payload = account.sign(transaction)
        hash = self.transaction_hash(payload)
        return SignedTransaction(
            payload,
            hash,
            account.public_key,
            self.type,
            self.network_type
        )

    signWith = util.undoc(sign_with)

    @staticmethod
    def transaction_hash(transaction: typing.AnyStr) -> str:
        """Generate transaction hash from signed transaction payload."""

        transaction = util.decode_hex(transaction, with_prefix=True)

        signature_half = transaction[4:36]
        signer = transaction[68:100]
        rest = transaction[100:]
        data = signature_half + signer + rest
        hash = util.hashlib.sha3_256(data).hexdigest()
        return typing.cast(str, hash)

    @staticmethod
    def catbuffer_size_shared() -> int:
        """Get the shared size of the entity."""
        return 120

    sharedEntitySize = util.undoc(catbuffer_size_shared)

    def catbuffer_size_specific(self) -> int:
        """Get the transaction-specific size of the entity."""
        raise NotImplementedError

    def catbuffer_size(self) -> int:
        """Get the total size of the entity."""
        shared = self.catbuffer_size_shared()
        specific = self.catbuffer_size_specific()
        return shared + specific

    entitySize = util.undoc(catbuffer_size)

    def to_catbuffer_shared(
        self,
        size: int,
        network_type: OptionalNetworkType = None
    ) -> bytes:
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
        buffer = bytearray(self.catbuffer_size_shared())
        buffer[0:4] = util.u32_to_catbuffer(size)
        if self.signer is not None and self.signature is not None:
            # Transaction is signed.
            buffer[4:68] = util.unhexlify(self.signature)
            buffer[68:100] = util.unhexlify(self.signer.public_key)
        else:
            # Transaction is not signed, write 0 bytes.
            buffer[4:68] = bytes(64)
            buffer[68:100] = bytes(32)
        buffer[100:101] = self.version.to_catbuffer()
        buffer[101:102] = self.network_type.to_catbuffer()
        buffer[102:104] = self.type.to_catbuffer()
        buffer[104:112] = util.u64_to_catbuffer(self.fee)
        buffer[112:120] = self.deadline.to_catbuffer()

        return bytes(buffer)

    toCatbufferShared = util.undoc(to_catbuffer_shared)

    def to_catbuffer_specific(
        self,
        network_type: OptionalNetworkType = None
    ) -> bytes:
        """Serialize transaction-specific data to catbuffer interchange format."""
        raise NotImplementedError

    toCatbufferSpecific = util.undoc(to_catbuffer_specific)

    def to_catbuffer(
        self,
        network_type: OptionalNetworkType = None
    ) -> bytes:
        """
        Serialize object to catbuffer interchange format.

        :param embedded: Is embedded transaction.
        """

        total_size = self.catbuffer_size()
        shared = self.to_catbuffer_shared(total_size, network_type)
        specific = self.to_catbuffer_specific(network_type)

        return shared + specific

    def load_catbuffer_shared(
        self,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ) -> typing.Tuple[int, bytes]:
        """Load shared transaction data from catbuffer."""

        assert len(data) >= self.catbuffer_size_shared()

        # uint32_t size
        # uint8_t[64] signature
        # uint8_t[32] signer
        # uint8_t version
        # uint8_t network_type
        # uint16_t type
        # uint64_t fee
        # uint64_t deadline
        total_size = util.u32_from_catbuffer(data[:4])
        signature = data[4:68]
        public_key = data[68:100]
        version = TransactionVersion.from_catbuffer(data[100:101])
        network_type = NetworkType.from_catbuffer(data[101:102])
        type = TransactionType.from_catbuffer(data[102:104])
        fee = util.u64_from_catbuffer(data[104:112])
        deadline = Deadline.from_catbuffer(data[112:])

        self._set('type', type)
        self._set('network_type', network_type)
        self._set('version', version)
        self._set('deadline', deadline)
        self._set('fee', fee)
        if signature != bytes(64) and public_key != bytes(32):
            # Transaction is signed.
            self._set('signature', util.hexlify(signature))
            signer = PublicAccount.create_from_public_key(util.hexlify(public_key), network_type)
            self._set('signer', signer)
        else:
            # Transaction is not signed.
            # All zero bytes for public key and hash, impossible, must be
            # dummy data.
            self._set('signature', None)
            self._set('signer', None)
        self._set('transaction_info', None)

        return total_size, data[self.catbuffer_size_shared():]

    loadCatbufferShared = util.undoc(load_catbuffer_shared)

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ) -> bytes:
        """Load transaction-specific data data from catbuffer."""
        raise NotImplementedError

    loadCatbufferSpecific = util.undoc(load_catbuffer_specific)

    @classmethod
    def from_catbuffer(
        cls,
        data: typing.AnyStr,
        network_type: OptionalNetworkType = None,
    ) -> Transaction:
        return cls.from_catbuffer_pair(data, network_type)[0]

    @classmethod
    def from_catbuffer_pair(
        cls,
        data: typing.AnyStr,
        network_type: OptionalNetworkType = None,
    ) -> typing.Tuple[Transaction, bytes]:
        """
        Deserialize object from catbuffer interchange format.
        If the cls is a subclass of `Transaction`, use the dedicated loader.
        If the cls is `Transaction`, determine the transaction type
        and load that.

        :param data: Transaction data in catbuffer interchange format.
        """

        data = util.decode_hex(data, with_prefix=True)
        if cls is not Transaction:
            # Have a subclass, use a dedicated loader.
            inst = cls.__new__(cls)
            total_size, data = inst.load_catbuffer_shared(data, network_type)
            data = inst.load_catbuffer_specific(data, network_type)
            return inst, data
        else:
            # Directly calling Transaction.from_catbuffer, detect the proper
            # loader and call that.
            type = TransactionType.from_catbuffer(data[102:104])[0]
            return cls.HOOKS[type][0](data, network_type)

    def to_dto(
        self,
        network_type: OptionalNetworkType = None
    ) -> dict:
        """Serialize object data to data transfer object."""
        raise NotImplementedError

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ) -> Transaction:
        """
        Deserialize object from data transfer object.
        If the cls is a subclass of `Transaction`, use the dedicated loader.
        If the cls is `Transaction`, determine the transaction type
        and load that.

        :param data: Transaction data in data transfer object.
        """
        raise NotImplementedError

    def aggregate_transaction(self) -> bytes:
        """Build aggregate transaction."""
        raise NotImplementedError

    aggregateTransaction = util.undoc(aggregate_transaction)

    def to_aggregate(self, signer: PublicAccount):
        """Convert transaction to inner transaction."""
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
