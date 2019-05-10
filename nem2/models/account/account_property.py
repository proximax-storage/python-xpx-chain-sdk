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
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['AccountProperty']


@util.inherit_doc
@util.dataclass(frozen=True)
class AccountProperty(util.DTO):
    """
    Describe account property via type and values.

    :param property_type: Account property type.
    :param values: Property values.
    """

    property_type: PropertyType
    values: typing.Sequence

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            # TODO(ahuszagh) Check when stabilized
            'propertyType': self.property_type.to_dto(network_type),
            'values': self.values,
        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        return cls(
            # TODO(ahuszagh) Check when stabilized
            property_type=PropertyType.from_dto(data['propertyType'], network_type),
            values=data['values'],
        )
