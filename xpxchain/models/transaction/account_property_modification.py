"""
    account_property_modification
    =============================

    Account property modification type and value.

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

from ..account.account_property import PropertyValue
from ..account.address import Address
from ..account.property_modification_type import PropertyModificationType
from ..blockchain.network_type import OptionalNetworkType
from ..mosaic.mosaic_id import MosaicId
from ..transaction.transaction_type import TransactionType
from ... import util

__all__ = ['AccountPropertyModification']

DTOType = typing.Union[
    str,
    typing.Sequence[int],
    int
]


def to_dto(value: PropertyValue) -> DTOType:
    """Serialize property modification value to DTO."""

    if isinstance(value, Address):
        return value.address
    elif isinstance(value, MosaicId):
        return util.u64_to_dto(int(value.id))
    elif isinstance(value, TransactionType):
        return value.to_dto()
    else:
        raise NotImplementedError


def from_dto(data: DTOType) -> PropertyValue:
    """Load property modification value from DTO."""

    if (isinstance(data, str) and (len(data) == 50)):
        return Address.create_from_encoded(data)
    elif (isinstance(data, str) and (len(data) == 40)):
        return Address.create_from_raw_address(data)
    elif isinstance(data, list):
        return MosaicId(util.u64_from_dto(data))
    elif isinstance(data, int):
        return TransactionType.create_from_dto(data)
    else:
        raise NotImplementedError


@util.inherit_doc
@util.dataclass(frozen=True)
class AccountPropertyModification(util.DTO):
    """
    Account property modification type and value.

    :param modification_type: Property modification type.
    :param value: Modification value.
    """

    modification_type: PropertyModificationType
    value: PropertyValue

    def is_address(self) -> bool:
        """Determine if the modification value type is an address."""
        return isinstance(self.value, Address)

    def is_mosaic(self) -> bool:
        """Determine if the modification value type is a mosaic ID."""
        return isinstance(self.value, MosaicId)

    def is_entity_type(self) -> bool:
        """Determine if the modification value type is an entity type."""
        return isinstance(self.value, TransactionType)

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'type', 'value'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'type': self.modification_type.to_dto(network_type),
            'value': to_dto(self.value),
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        type = data['type']
        return cls(
            modification_type=PropertyModificationType.create_from_dto(type),
            value=from_dto(data['value']),
        )
