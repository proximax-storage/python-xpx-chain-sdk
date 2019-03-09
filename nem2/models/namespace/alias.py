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

import typing

from nem2 import util
from .alias_type import AliasType
from ..account.address import Address
from ..mosaic.mosaic_id import MosaicId

ValueType = typing.Optional[typing.Union['Address', 'MosaicId']]


@util.inherit_doc
@util.dataclass(frozen=True)
class Alias(util.Dto):
    """
    Alias for type definitions.

    :param value: Address or mosaic ID for alias.
    """

    type: 'AliasType'
    value: ValueType

    def __init__(self, value: ValueType = None) -> None:
        object.__setattr__(self, "value", value)
        if isinstance(value, Address):
            object.__setattr__(self, "type", AliasType.ADDRESS)
        elif isinstance(value, MosaicId):
            object.__setattr__(self, "type", AliasType.MOSAIC_ID)
        elif value is None:
            object.__setattr__(self, "type", AliasType.NONE)
        else:
            raise TypeError("Got invalid value type for Alias.")

    @property
    def address(self) -> 'Address':
        if self.type != AliasType.ADDRESS:
            raise ValueError("Alias does not store address.")
        return self.value

    @property
    def mosaic_id(self) -> 'MosaicId':
        if self.type != AliasType.MOSAIC_ID:
            raise ValueError("Alias does not store mosaic ID.")
        return self.value

    mosaicId = util.undoc(mosaic_id)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Alias):
            return False
        return self.astuple() == other.astuple()

    def to_dto(self) -> typing.Optional[dict]:
        if self.type == AliasType.NONE:
            return None
        elif self.type == AliasType.ADDRESS:
            return {'type': self.type.to_dto(), 'address': self.value.to_dto()}
        elif self.type == AliasType.MOSAIC_ID:
            return {'type': self.type.to_dto(), 'mosaicId': self.value.to_dto()}
        raise ValueError("Invalid data for Alias.to_dto.")

    @classmethod
    def from_dto(cls, data: typing.Optional[dict]) -> 'Alias':
        if data is None:
            return cls()

        type = AliasType.from_dto(data['type'])
        if type == AliasType.ADDRESS:
            return cls(Address.from_dto(data['address']))
        elif type == AliasType.MOSAIC_ID:
            return cls(MosaicId.from_dto(data['mosaicId']))
        raise ValueError("Invalid data for Alias.from_dto.")
