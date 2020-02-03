"""
    receipt_base
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

from .format import DTOFormat
from .receipt_type import ReceiptType
from .receipt_version import ReceiptVersion
from ..blockchain.network_type import OptionalNetworkType
from ... import util


ReceiptBaseType = typing.TypeVar('ReceiptBaseType', bound='ReceiptBase')
TypeMap = typing.Mapping[ReceiptType, typing.Type[ReceiptBaseType]]


@util.inherit_doc
@util.dataclass(frozen=True)
class ReceiptBase(util.Model):
    """
    Abstract, shared transaction base class.

    :param type: Transaction type.
    :param network_type: Network type.
    :param version: Transaction version.
    """

    # FIELDS

    type: ReceiptType
    version: ReceiptVersion
    network_type: OptionalNetworkType

    # OVERRIDABLE CLASSVARS
    # The following classvars should be re-implemented for each
    # base transaction type.

    # Registry of transaction types to models. Allows users to
    # register custom models to customize serialization/deserialization
    # logic.
    TYPE_MAP: typing.ClassVar[TypeMap]

    # Data to simplify the serialization/deserialization of
    # transactions of a given type. Provides high-level
    # routines, and also maps fields 1:1 to transaction DTO
    # keys.
    DTO: typing.ClassVar[DTOFormat]

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        """Validate receipt-specific fields in data-transfer object."""
        raise util.AbstractMethodError

    @classmethod
    def validate_dto_shared(cls, data: dict) -> bool:
        """Validate shared fields in data-transfer object."""
        raise util.AbstractMethodError

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        return (
            cls.validate_dto_shared(data)
            and cls.validate_dto_specific(data)
        )

    def to_dto_shared(
        self,
        network_type: OptionalNetworkType,
    ) -> dict:
        """Export shared receipt data to DTO. Internal use only."""
        raise util.AbstractMethodError

    def to_dto_specific(
        self,
        network_type: OptionalNetworkType,
    ) -> dict:
        """Export receipt-specific data to DTO. Internal use only."""
        raise util.AbstractMethodError

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        # Check network type matches transaction.
        if network_type is not None and network_type != self.network_type:
            raise ValueError('Network type does not match receipt.')

        # Save shared and specific receipt data.
        dto = self.to_dto_shared(self.network_type)
        dto.update(self.to_dto_specific(self.network_type))
        return dto

    def load_dto_shared(
        self,
        data: dict,
        network_type: OptionalNetworkType,
    ) -> None:
        """Load shared receipt data from DTO. Internal use only."""
        raise util.AbstractMethodError

    def load_dto_specific(
        self,
        data: dict,
        network_type: OptionalNetworkType,
    ) -> None:
        """Load receipt-specific data from DTO. Internal use only."""
        raise util.AbstractMethodError

    @classmethod
    def create_from_dto(
        cls: typing.Type[ReceiptBaseType],
        data: dict,
        network_type: OptionalNetworkType = None,
    ) -> ReceiptBaseType:
        """
        Deserialize object from DTO interchange format.

        If the cls is a direct subclass of `ReceiptBase`,
        determine the receipt type and therefore the correct class.
        If the cls is not a direct subclass of `TransactionBase`
        (and therefore a finalized receipt model), use the
        class directly.

        :param data: Receipt data in DTO interchange format.
        :param network_type: Network type.
        """

        # If we have a base class, find the correct derived class.
        if cls in ReceiptBase.__subclasses__():
            cls = cls.DTO.find_receipt(cls.TYPE_MAP, data)
        inst = typing.cast(ReceiptBaseType, cls.__new__(cls))

        # Validate after we find the correct subclass.
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        # Load and check the network type.
        # nt = cls.DTO.load_network_type(data)
        # if network_type is not None and network_type != nt:
        #    raise ValueError('Network type does not match receipt.')

        # Load shared and specific receipt data.
        inst.load_dto_shared(data, network_type)
        inst.load_dto_specific(data, network_type)
        return inst
