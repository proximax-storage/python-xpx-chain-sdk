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
from ..transaction.transaction import Transaction
from ... import util

__all__ = ['AccountProperty']

PropertyValue= typing.Union[
    Address,
    MosaicId,
    Transaction,
    # TODO(ahuszagh) Add sentinel
]


@util.inherit_doc
@util.dataclass(frozen=True)
class AccountProperty(util.DTOSerializable):
    """
    Describe account property via type and values.

    :param property_type: Account property type.
    :param values: Property values.

    DTO Format:
        .. code-block:: yaml

            AccountPropertyDTO:
                propertyType: integer
                # Base64(Address), Base64(MosaicID), Base64(Transaction)
                values: string
    """

    property_type: PropertyType
    values: typing.Sequence[PropertyValue]

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        raise NotImplementedError
#        return {
#            # TODO(ahuszagh) Check when stabilized
#            'propertyType': self.property_type.to_dto(network_type),
#            'values': [i.to_base64() for i in self.values],
#        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        raise NotImplementedError
#        return cls(
#            # TODO(ahuszagh) Check when stabilized
#            property_type=PropertyType.from_dto(data['propertyType'], network_type),
#            values=[AccountProperty.from_base64(i) for i in data['values']],
#        )
