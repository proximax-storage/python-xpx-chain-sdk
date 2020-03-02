"""
    transaction
    ===========

    Abstract base class for transaction objects.

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

from .aggregate_transaction_info import AggregateTransactionInfo
from .deadline import Deadline
from .format import CatbufferFormat, DTOFormat
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType, OptionalNetworkType
from ... import util


TransactionInfoType = typing.Union[TransactionInfo, AggregateTransactionInfo]
TransactionBaseType = typing.TypeVar('TransactionBaseType', bound='TransactionBase')
TypeMap = typing.Mapping[TransactionType, typing.Type[TransactionBaseType]]


@util.inherit_doc
@util.dataclass(frozen=True)
class TransactionBase(util.Model):
    """
    Abstract, shared transaction base class.

    :param type: Transaction type.
    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param signature: Transaction signature (missing if embedded transaction).
    :param signer: Account of transaction creator.
    :param transaction_info: Transaction metadata.
    """

    # FIELDS

    type: TransactionType
    network_type: NetworkType
    version: TransactionVersion
    deadline: typing.Optional[Deadline]
    max_fee: typing.Optional[int]
    signature: typing.Optional[str]
    signer: typing.Optional[PublicAccount]
    transaction_info: typing.Optional[TransactionInfoType]

    # OVERRIDABLE CLASSVARS
    # The following classvars should be re-implemented for each
    # base transaction type.

    # Registry of transaction types to models. Allows users to
    # register custom models to customize serialization/deserialization
    # logic.
    TYPE_MAP: typing.ClassVar[TypeMap]

    # Data to simplify the serialization/deserialization of
    # transactions of a given type. Stores pre-computed
    # slices for individual fields, using dictionary lookups.
    # Using Python dictionaries is competitive with attribute lookup,
    # so it should be competitive with native performance.
    CATBUFFER: typing.ClassVar[CatbufferFormat]

    # Data to simplify the serialization/deserialization of
    # transactions of a given type. Provides high-level
    # routines, and also maps fields 1:1 to transaction DTO
    # keys.
    DTO: typing.ClassVar[DTOFormat]

    # INFO

    def is_unconfirmed(self) -> bool:
        """Is transaction pending to be included."""
        info = self.transaction_info
        return info is not None and info.is_unconfirmed()

    def is_confirmed(self) -> bool:
        """Is transaction already included."""
        info = self.transaction_info
        return info is not None and info.is_confirmed()

    def has_missing_signatures(self) -> bool:
        """Does the transaction have missing signatures."""
        info = self.transaction_info
        return info is not None and info.has_missing_signatures()

    def is_unannounced(self) -> bool:
        """Is transaction not known by the network."""
        return self.transaction_info is None

    # CATBUFFER

    @classmethod
    def catbuffer_size_shared(cls) -> int:
        """Get the shared size of the entity. Internal use only."""
        return cls.CATBUFFER.size_shared

    def catbuffer_size_specific(self) -> int:
        """Get the transaction-specific size of the entity. Internal use only."""
        raise util.AbstractMethodError

    def catbuffer_size(self) -> int:
        """Get the total size of the entity. Internal use only."""
        shared = self.catbuffer_size_shared()
        specific = self.catbuffer_size_specific()
        return shared + specific

    def to_catbuffer_shared(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export shared transaction data to catbuffer. Internal use only."""
        raise util.AbstractMethodError

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export transaction-specific data to catbuffer. Internal use only."""
        raise util.AbstractMethodError

    def to_catbuffer(
        self,
        network_type: OptionalNetworkType = None,
        fee_strategy: util.FeeCalculationStrategy = util.FeeCalculationStrategy.MEDIUM,
    ) -> bytes:
        # Check network type matches transaction.
        if network_type is not None and network_type != self.network_type:
            raise ValueError('Network type does not match transaction.')

        # Use fee calculation algorithm
        max_fee = util.calculate_fee(fee_strategy, self.max_fee, self.catbuffer_size())
        self._set('max_fee', max_fee)

        # Save shared and specific transaction data.
        shared = self.to_catbuffer_shared(self.network_type)
        specific = self.to_catbuffer_specific(self.network_type)

        return shared + specific

    def load_catbuffer_shared(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load shared transaction data from catbuffer. Internal use only."""
        raise util.AbstractMethodError

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load transaction-specific data from catbuffer. Internal use only."""
        raise util.AbstractMethodError

    @classmethod
    def create_from_catbuffer(
        cls: typing.Type[TransactionBaseType],
        data: typing.AnyStr,
        network_type: OptionalNetworkType = None,
    ) -> TransactionBaseType:
        return cls.create_from_catbuffer_pair(data, network_type)[0]

    @classmethod
    def create_from_catbuffer_pair(
        cls: typing.Type[TransactionBaseType],
        data: typing.AnyStr,
        network_type: OptionalNetworkType = None,
    ) -> typing.Tuple[TransactionBaseType, bytes]:
        """
        Deserialize object from catbuffer interchange format.

        If the cls is a direct subclass of `TransactionBase`,
        determine the transaction type and therefore the correct class.
        If the cls is not a direct subclass of `TransactionBase`
        (and therefore a finalized transaction model), use the
        class directly.

        :param data: Transaction data in catbuffer interchange format.
        :param network_type: Network type.
        """

        # Decode the data and check initial parameters.
        data = util.decode_hex(data, with_prefix=True)
        if len(data) < cls.catbuffer_size_shared():
            raise ValueError('Insufficient data to deserialize transaction.')

        # If we have a base class, find the correct derived class.
        if cls in TransactionBase.__subclasses__():
            cls = cls.CATBUFFER.find_transaction(cls.TYPE_MAP, data)
        inst = typing.cast(TransactionBaseType, cls.__new__(cls))

        # Load the network type and the total size and check transaction data.
        size = cls.CATBUFFER.load_size(data)
        nt = cls.CATBUFFER.load_network_type(data)
        if network_type is not None and network_type != nt:
            raise ValueError('Network type does not match transaction.')
        if len(data) < size:
            raise ValueError('Transaction data shorter than entity size.')

        # Load shared and specific transaction data.
        data = inst.load_catbuffer_shared(data, nt)
        data = inst.load_catbuffer_specific(data, nt)
        return inst, data

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        """Validate transaction-specific fields in data-transfer object."""
        raise util.AbstractMethodError

    @classmethod
    def validate_dto_shared(cls, data: dict) -> bool:
        """Validate shared fields in data-transfer object."""
        raise util.AbstractMethodError

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'transaction'}
        all_keys = required_keys | {'meta'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, all_keys)
            and cls.validate_dto_shared(data['transaction'])
            and cls.validate_dto_specific(data['transaction'])
        )

    def to_dto_shared(
        self,
        network_type: NetworkType,
    ) -> dict:
        """Export shared transaction data to DTO. Internal use only."""
        raise util.AbstractMethodError

    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        """Export transaction-specific data to DTO. Internal use only."""
        raise util.AbstractMethodError

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        # Check network type matches transaction.
        if network_type is not None and network_type != self.network_type:
            raise ValueError('Network type does not match transaction.')

        # Save shared and specific transaction data.
        dto = self.to_dto_shared(self.network_type)
        dto['transaction'].update(self.to_dto_specific(self.network_type))
        return dto

    def load_dto_shared(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        """Load shared transaction data from DTO. Internal use only."""
        raise util.AbstractMethodError

    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        """Load transaction-specific data from DTO. Internal use only."""
        raise util.AbstractMethodError

    @classmethod
    def create_from_dto(
        cls: typing.Type[TransactionBaseType],
        data: dict,
        network_type: OptionalNetworkType = None,
    ) -> TransactionBaseType:
        """
        Deserialize object from DTO interchange format.

        If the cls is a direct subclass of `TransactionBase`,
        determine the transaction type and therefore the correct class.
        If the cls is not a direct subclass of `TransactionBase`
        (and therefore a finalized transaction model), use the
        class directly.

        :param data: Transaction data in DTO interchange format.
        :param network_type: Network type.
        """

        # If we have a base class, find the correct derived class.
        if cls in TransactionBase.__subclasses__():
            cls = cls.DTO.find_transaction(cls.TYPE_MAP, data)
        inst = typing.cast(TransactionBaseType, cls.__new__(cls))

        # Validate after we find the correct subclass.
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        # Load and check the network type.
        nt = cls.DTO.load_network_type(data)
        if network_type is not None and network_type != nt:
            raise ValueError('Network type does not match transaction.')

        # Load shared and specific transaction data.
        inst.load_dto_shared(data, nt)
        inst.load_dto_specific(data['transaction'], nt)
        return inst
