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

from .alias_type import AliasType
from ..account.address import Address
from ..blockchain.network_type import OptionalNetworkType
from ..mosaic.mosaic_id import MosaicId
from ... import util

__all__ = ['Alias']

ValueType = typing.Optional[typing.Union[Address, MosaicId]]


def dto_to_kwds(
    data: dict,
    network_type: OptionalNetworkType = None,
) -> dict:
    """Convert data transfer object to keywords for initializer."""

    kwds: dict = {'type': AliasType.create_from_dto(data['type'], network_type)}
    if data['type'] == AliasType.NONE:
        kwds['value'] = None
    elif data['type'] == AliasType.ADDRESS:
        kwds['value'] = Address.create_from_encoded(data['address'])
    elif data['type'] == AliasType.MOSAIC_ID:
        kwds['value'] = MosaicId(util.u64_from_dto(data['mosaicId']))
    else:       # pragma: unreachable
        raise ValueError("Invalid data for Alias.create_from_dto.")

    return kwds


@util.inherit_doc
@util.dataclass(frozen=True, type=AliasType.NONE, value=None)
class Alias(util.DTO):
    """
    Alias for type definitions.

    :param value: Address or mosaic ID for alias.

    DTO Format:
        .. code-block:: yaml

            AliasDTO:
                type: integer
                mosaicId?: UInt64DTO
                # Hex(Address) (50-bytes)
                address?: string
    """

    type: AliasType
    value: ValueType

    def __post_init__(self):
        if self.type == AliasType.ADDRESS:
            same_type = isinstance(self.value, Address)
        elif self.type == AliasType.MOSAIC_ID:
            same_type = isinstance(self.value, MosaicId)
        elif self.type == AliasType.NONE:
            same_type = self.value is None
        else:       # pragma: unreachable
            same_type = False
        if not same_type:
            raise TypeError("Alias value and type do not match.")

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
    ) -> dict:
        data: dict = {'type': self.type.to_dto(network_type)}
        if self.type == AliasType.NONE:
            pass
        elif self.type == AliasType.ADDRESS:
            address = typing.cast(Address, self.value)
            data['address'] = util.hexlify(address.encoded)
        elif self.type == AliasType.MOSAIC_ID:
            mosaic_id = typing.cast(MosaicId, self.value)
            data['mosaicId'] = util.u64_to_dto(int(mosaic_id))
        else:       # pragma: unreachable
            raise ValueError("Invalid data for Alias.to_dto.")

        return data

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        return cls(**dto_to_kwds(data, network_type))
