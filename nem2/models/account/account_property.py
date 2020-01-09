"""
    account_property
    ================

    Property for an account.

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

from .property_type import PropertyType
from .address import Address
from ..blockchain.network_type import OptionalNetworkType
from ..mosaic.mosaic_id import MosaicId
from ..transaction.transaction_type import TransactionType
from ... import util

__all__ = ['AccountProperty']

PropertyValue = typing.Union[
    Address,
    MosaicId,
    TransactionType,
]
PropertyValueList = typing.Sequence[PropertyValue]


def to_base64(
    property_type: int,
    values: typing.Sequence[PropertyValue],
) -> typing.List[str]:
    """Export properties to base64."""

    if property_type & 0x01:
        # We have an address.
        cast = lambda x: typing.cast(Address, x)
        return [util.b64encode(cast(i).encoded) for i in values]
    elif property_type & 0x02:
        # We have a mosaic.
        raise NotImplementedError
    elif property_type & 0x04:
        # We have a transaction.
        raise NotImplementedError
    else:
        raise ValueError('Unknown property type.')


def from_base64(
    property_type: int,
    values: typing.List[str],
) -> typing.Sequence[PropertyValue]:
    """Load properties from base64."""

    if property_type & 0x01:
        # We have an address.
        return [Address.create_from_encoded(util.b64decode(i)) for i in values]
    elif property_type & 0x02:
        # We have a mosaic.
        raise NotImplementedError
    elif property_type & 0x04:
        # We have a transaction.
        raise NotImplementedError
    else:
        raise ValueError('Unknown property type.')


@util.inherit_doc
@util.dataclass(frozen=True)
class AccountProperty(util.DTO):
    """
    Describe account property via type and values.

    :param property_type: Account property type.
    :param values: Property values.

    DTO Format:
        .. code-block:: yaml

            AccountPropertyDTO:
                propertyType: integer
                # Base64(Address), Base64(MosaicID), Base64(Transaction)
                values: string[]
    """

    property_type: PropertyType
    values: typing.Sequence[PropertyValue]

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'propertyType', 'values'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'propertyType': self.property_type.to_dto(network_type),
            'values': to_base64(int(self.property_type), self.values),
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        property_type = data['propertyType']
        values = data['values']
        return cls(
            property_type=PropertyType.create_from_dto(property_type, network_type),
            values=from_base64(property_type, values),
        )
