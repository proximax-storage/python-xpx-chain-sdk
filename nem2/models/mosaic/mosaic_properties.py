"""
    mosaic_properties
    =================

    Properties of a NEM asset.

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

import struct
import typing

from nem2 import util


def to_flags(supply_mutable: bool, transferable: bool, levy_mutable: bool) -> int:
    """Convert 3 binary values to sequential bit flags"""

    flags: int = 0
    if supply_mutable:
        flags |= 1
    if transferable:
        flags |= 2
    if levy_mutable:
        flags |= 4

    return flags


DURATION_ID = 2

PROPERTIES = {
    DURATION_ID: 'duration'
}

class MosaicProperties(util.Model):
    """
    NEM mosaic properties.

    Properties of a custom NEM asset.
    """

    __slots__ = (
        '_flags',
        '_divisibility',
        '_duration',
    )

    def __init__(self, flags: int, divisibility: int, duration: int = 0):
        """
        :param flags: Flags for the properties of the mosaic.
        :param divisibility: Determines the decimal place mosaic can be divided into (from 0-6).
        :param duration: Number of blocks the mosaic will be available.
        """
        self._flags = flags
        self._divisibility = divisibility
        self._duration = duration

    @property
    def flags(self):
        """Get raw flags for mosaic."""
        return self._flags

    @property
    def supply_mutable(self) -> bool:
        """Mosaic allows a supply change later on. Defaults to false."""
        return (self._flags & 1) == 1

    supplyMutable = util.undoc(supply_mutable)

    @property
    def transferable(self) -> bool:
        """Allow transfer of funds from accounts other than the creator. Defaults to true."""
        return (self._flags & 2) == 2

    @property
    def levy_mutable(self) -> bool:
        """Get if levy is mutable. Defaults to false."""
        return (self._flags & 4) == 4

    levyMutable = util.undoc(levy_mutable)

    @property
    def divisibility(self) -> int:
        """Get the decimal place mosaic can be divided into."""
        return self._divisibility

    @property
    def duration(self) -> int:
        """Get the number of blocks the mosaic will be available."""
        return self._duration

    @classmethod
    def create(cls, **kwds) -> 'MosaicProperties':
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

    @util.doc(util.Model.tie.__doc__)
    def tie(self) -> tuple:
        return super().tie()

    @util.doc(util.Model.to_dto.__doc__)
    def to_dto(self) -> typing.Sequence[util.Uint64DtoType]:
        return [
            util.uint64_to_dto(self.flags),
            util.uint64_to_dto(self.divisibility),
            util.uint64_to_dto(self.duration),
        ]

    @util.doc(util.Model.from_dto.__doc__)
    @classmethod
    def from_dto(cls, data: typing.Sequence[util.Uint64DtoType]) -> 'MosaicProperties':
        flags = util.dto_to_uint64(data[0])
        divisibility = util.dto_to_uint64(data[1])
        duration = util.dto_to_uint64(data[2])
        return cls(flags, divisibility, duration)

    @util.doc(util.Model.to_catbuffer.__doc__)
    def to_catbuffer(self) -> bytes:
        data = struct.pack('<BBB', 1, self.flags, self.divisibility)
        properties = struct.pack('<BQ', DURATION_ID, self.duration)
        return data + properties

    @util.doc(util.Model.from_catbuffer.__doc__)
    @classmethod
    def from_catbuffer(cls, data: bytes) -> ('MosaicProperties', bytes):
        # Read the array count, property flags and divisibility.
        assert len(data) >= 3
        count, flags, divisibility = struct.unpack('<BBB', data[:3])

        # Ensure the buffer is long enough for the data, and iteratively
        # read the remaining properties.
        buffer_length = 3 + 9 * count
        assert len(data) >= buffer_length
        properties = struct.iter_unpack('<BQ', data[3:])
        kwds = {}
        for _ in range(count):
            prop_id, prop_value = next(properties)
            kwds[PROPERTIES[prop_id]] = prop_value

        inst = cls(flags, divisibility, **kwds)
        return inst, data[buffer_length:]
