"""
    mosaic_properties
    =================

    Properties of an asset.

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
from ..blockchain.network_type import NetworkType

__all__ = ['MosaicProperties']

OptionalNetworkType = typing.Optional[NetworkType]
DTOType = typing.Sequence[util.U64DTOType]
VERSION = 1
DURATION_ID = 2
PROPERTY_SIZE = 9
PROPERTIES = {
    DURATION_ID: 'duration'
}


def to_flags(
    supply_mutable: bool,
    transferable: bool,
    levy_mutable: bool
) -> int:
    """Convert 3 binary values to sequential bit flags"""

    flags: int = 0
    if supply_mutable:
        flags |= 1
    if transferable:
        flags |= 2
    if levy_mutable:
        flags |= 4

    return flags


def property_to_catbuffer(id: int, value: int) -> bytes:
    """Convert property with ID to catbuffer."""
    return util.u8_to_catbuffer(id) + util.u64_to_catbuffer(value)


def property_from_catbuffer(catbuffer: bytes) -> typing.Tuple[int, int]:
    """Convert catbuffer to property with ID."""

    id = util.u8_from_catbuffer(catbuffer[:1])
    value = util.u64_from_catbuffer(catbuffer[1:])
    return (id, value)


@util.inherit_doc
@util.dataclass(frozen=True, duration=0)
class MosaicProperties(util.Model):
    """
    Properties of an asset.

    :param flags: Flags for the properties of the mosaic.
    :param divisibility: Decimal places mosaic can be divided into [0-6].
    :param duration: Number of blocks the mosaic will be available.
    """

    flags: int
    divisibility: int
    duration: int

    @property
    def supply_mutable(self) -> bool:
        """Mosaic allows a supply change later on. Default false."""
        return (self.flags & 1) == 1

    supplyMutable = util.undoc(supply_mutable)

    @property
    def transferable(self) -> bool:
        """Allow transfer of funds from non-creator accounts. Default true."""
        return (self.flags & 2) == 2

    @property
    def levy_mutable(self) -> bool:
        """Get if levy is mutable. Default false."""
        return (self.flags & 4) == 4

    levyMutable = util.undoc(levy_mutable)

    @classmethod
    def create(cls, **kwds) -> MosaicProperties:
        """
        Create mosaic properties with default parameters.

        :param supply_mutable: Mosaic allows supply change later.
        :param transferable: Allow transfer of funds from accounts other than creator.
        :param levy_mutable: If levy is mutable.
        :param divisibility: Decimal place mosaic can be divided into.
        :param duration: Number of blocks the mosaic will be available.
        """
        supply_mutable = typing.cast(bool, kwds.get('supply_mutable', False))
        transferable = typing.cast(bool, kwds.get('transferable', True))
        levy_mutable = typing.cast(bool, kwds.get('levy_mutable', False))
        divisibility = kwds.get('divisibility', 0)
        duration = kwds.get('duration', 0)
        flags = to_flags(supply_mutable, transferable, levy_mutable)
        return MosaicProperties(flags, divisibility, duration)

    def to_dto(
        self,
        network_type: OptionalNetworkType = None
    ) -> DTOType:
        return [
            util.u64_to_dto(self.flags),
            util.u64_to_dto(self.divisibility),
            util.u64_to_dto(self.duration),
        ]

    @classmethod
    def from_dto(
        cls,
        data: DTOType,
        network_type: OptionalNetworkType = None
    ) -> MosaicProperties:
        flags = util.u64_from_dto(data[0])
        divisibility = util.u64_from_dto(data[1])
        duration = util.u64_from_dto(data[2])
        return cls(flags, divisibility, duration)

    def to_catbuffer(
        self,
        network_type: OptionalNetworkType = None
    ) -> bytes:
        version = util.u8_to_catbuffer(VERSION)
        flags = util.u8_to_catbuffer(self.flags)
        divisibility = util.u8_to_catbuffer(self.divisibility)
        duration = property_to_catbuffer(DURATION_ID, self.duration)
        return version + flags + divisibility + duration

    @classmethod
    def from_catbuffer_pair(
        cls,
        data: bytes,
        network_type: OptionalNetworkType = None
    ) -> typing.Tuple[MosaicProperties, bytes]:
        # Read the array count, property flags and divisibility.
        count = util.u8_from_catbuffer(data[:1])
        flags = util.u8_from_catbuffer(data[1:2])
        divisibility = util.u8_from_catbuffer(data[2:3])

        # Ensure the buffer is long enough for the data, and iteratively
        # read the remaining properties.
        step = PROPERTY_SIZE
        property_size = step * count
        size = 3 + property_size
        kwds = {}
        for i in range(0, property_size, step):
            start = 3 + i
            stop = start + step
            id, value = property_from_catbuffer(data[start:stop])
            kwds[PROPERTIES[id]] = value

        # Instantiate our class and return pair.
        inst = cls(flags, divisibility, **kwds)
        remaining = data[size:]
        return inst, remaining
