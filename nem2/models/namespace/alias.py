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


class Alias(util.Tie):
    """Alias for type definitions."""

    __slots__ = (
        '_type',
        '_value',
    )

    def __init__(self, value: ValueType = None):
        """
        :param value: Address or mosaic ID for alias.
        """
        self._value = value
        if isinstance(value, Address):
            self._type = AliasType.ADDRESS
        elif isinstance(value, MosaicId):
            self._type = AliasType.MOSAIC_ID
        elif value is None:
            self._type = AliasType.NONE
        else:
            raise TypeError("Got invalid value type for Alias.")

    @property
    def type(self) -> AliasType:
        """Get the value type."""
        return self._type

    @property
    def value(self) -> ValueType:
        """Get the value."""
        return self._value

    @property
    def address(self) -> 'Address':
        if self.type != AliasType.ADDRESS:
            raise TypeError("Alias does not store address.")
        return self.value

    @property
    def mosaic_id(self) -> 'MosaicId':
        if self.type != AliasType.MOSAIC_ID:
            raise TypeError("Alias does not store mosaic ID.")
        return self.value

    mosaicId = util.undoc(mosaic_id)

    @util.doc(util.Tie.tie)
    def tie(self) -> tuple:
        return super().tie()
