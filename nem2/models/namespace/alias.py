"""
    alias
    =====

    Interface for aliases.

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
from .alias_type import AliasType
from ..account.address import Address
from ..blockchain.network_type import OptionalNetworkType
from ..mosaic.mosaic_id import MosaicId

__all__ = ['Alias']

DTOType = typing.Optional[dict]
ValueType = typing.Optional[typing.Union[Address, MosaicId]]


@util.inherit_doc
@util.dataclass(frozen=True)
class Alias(util.DTO):
    """
    Alias for type definitions.

    :param value: Address or mosaic ID for alias.
    """

    type: AliasType
    value: ValueType

    def __init__(self, value: ValueType = None) -> None:
        self._set("value", value)
        if isinstance(value, Address):
            self._set("type", AliasType.ADDRESS)
        elif isinstance(value, MosaicId):
            self._set("type", AliasType.MOSAIC_ID)
        elif value is None:
            self._set("type", AliasType.NONE)
        else:
            raise TypeError("Got invalid value type for Alias.")

    @property
    def address(self) -> Address:
        if self.type != AliasType.ADDRESS:
            raise ValueError("Alias does not store address.")
        return self.value

    @property
    def mosaic_id(self) -> MosaicId:
        if self.type != AliasType.MOSAIC_ID:
            raise ValueError("Alias does not store mosaic ID.")
        return self.value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Alias):
            return False
        return self.astuple(recurse=False) == other.astuple(recurse=False)

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> DTOType:
        if self.type == AliasType.NONE:
            return None

        type = self.type.to_dto(network_type)
        value = self.value.to_dto(network_type)
        if self.type == AliasType.ADDRESS:
            return {'type': type, 'address': value}
        elif self.type == AliasType.MOSAIC_ID:
            return {'type': type, 'mosaicId': value}
        raise ValueError("Invalid data for Alias.to_dto.")

    @classmethod
    def from_dto(
        cls,
        data: DTOType,
        network_type: OptionalNetworkType = None,
    ):
        if data is None:
            return cls()

        type = AliasType.from_dto(data['type'], network_type)
        if type == AliasType.ADDRESS:
            return cls(Address.from_dto(data['address'], network_type))
        elif type == AliasType.MOSAIC_ID:
            return cls(MosaicId.from_dto(data['mosaicId'], network_type))
        raise ValueError("Invalid data for Alias.from_dto.")
