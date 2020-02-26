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

from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['MosaicProperties']


DTO2Type = typing.Sequence[dict]
FLAGS_ID = 0
DIVISIBILITY_ID = 1
DURATION_ID = 2
PROPERTY_SIZE = 9
PROPERTIES = {
    FLAGS_ID: 'flags',
    DIVISIBILITY_ID: 'divisibility',
    DURATION_ID: 'duration',
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
@util.dataclass(frozen=True)
class MosaicProperties(util.DTO):
    """
    Properties of an asset.

    Note: The `MosaicDefinitionTransaction` uses a different DTO
    format for `MosaicProperties` than specified here.

    :param flags: Flags for the properties of the mosaic.
    :param divisibility: Decimal places mosaic can be divided into [0-6].
    :param duration: Number of blocks the mosaic will be available.

    DTO Format:
        .. code-block:: yaml

            MosaicPropertiesDTO: UInt64DTO[]
    """

    flags: int
    divisibility: int
    duration: int

    def __init__(
        self,
        flags: int,
        divisibility: int = 0,
        duration: int = 0,
    ):
        if flags < 0 or flags > 7:
            raise ValueError('Invalid flags, not in range [0-7].')
        if divisibility < 0 or divisibility > 6:
            raise ValueError('Invalid divisibility, not in range [0-6].')
        self._set('flags', flags)
        self._set('divisibility', divisibility)
        self._set('duration', duration)

    @property
    def supply_mutable(self) -> bool:
        """Mosaic allows a supply change later on. Default false."""
        return (self.flags & 1) == 1

    @property
    def transferable(self) -> bool:
        """Allow transfer of funds from non-creator accounts. Default true."""
        return (self.flags & 2) == 2

    @property
    def levy_mutable(self) -> bool:
        """Get if levy is mutable. Default false."""
        return (self.flags & 4) == 4

    @classmethod
    def create(cls, **kwds):
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
        return cls(flags, divisibility, duration)

    @classmethod
    def validate_dto(cls, data: typing.Sequence[dict]) -> bool:
        """Validate the data-transfer object."""

        return (
            len(data) in {2, 3}
            and all(len(i) == 2 for i in data)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> typing.Sequence[dict]:
        # For indefinite mosaics, the duration is optional (default 0).
        return [
            {'id': 0, 'value': util.u64_to_dto(self.flags)},
            {'id': 1, 'value': util.u64_to_dto(self.divisibility)},
            {'id': 2, 'value': util.u64_to_dto(self.duration)},
        ]

    @classmethod
    def create_from_dto(
        cls,
        data: typing.Sequence[dict],
        network_type: OptionalNetworkType = None,
    ) -> MosaicProperties:
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        # For indefinite mosaics, the duration is optional (default 0).
        duration = 0

        for prop in data[0:3]:
            prop_id = util.u8_from_dto(prop["id"])

            if (prop_id == 0):
                flags = util.u64_from_dto(prop["value"])
            elif (prop_id == 1):
                divisibility = util.u64_from_dto(prop["value"])
            elif (prop_id == 2):
                duration = util.u64_from_dto(prop["value"])
            else:
                raise ValueError('Invalid data-transfer object.')

        return cls(flags, divisibility, duration)

    # TESTING
    # Private, internal helper for testing only.

    def _permute_(self, cb) -> MosaicProperties:
        """Permute data inside self."""

        flags = 0x7 - self.flags
        divisibility = 6 - self.divisibility
        duration = cb(self.duration)
        return MosaicProperties(flags, divisibility, duration)


@util.inherit_doc
@util.dataclass(frozen=True)
class MosaicDefinitionProperties(util.Model):
    """Internal class to provide transaction support for mosaic properties."""

    model: MosaicProperties

    def catbuffer_size(self) -> int:
        """Get the mosaic properties size as catbuffer."""

        # Get the number of optional properties.
        count = 0
        if self.model.duration != 0:
            count += 1

        # uint8_t count
        # uint8_t flags
        # uint8_t divisibility
        # typedef MosaicProperty { id: uint8_t, value: uint64_t }
        # MosaicProperty[count] properties
        count_size = util.U8_BYTES
        flags_size = util.U8_BYTES
        divisibility_size = util.U8_BYTES
        property_size = util.U64_BYTES + util.U8_BYTES
        return count_size + flags_size + divisibility_size + count * property_size

    @classmethod
    def validate_dto(cls, data: DTO2Type) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'id', 'value'}
        return (
            len(data) >= 2
            and all((
                cls.validate_dto_required(entry, required_keys)
                and cls.validate_dto_all(entry, required_keys)
            ) for entry in data)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ):
        # A newer version of DTO, which is used in MosaicDefinitionTransactions.
        # We need to keep the two versions separate.
        data = [
            {'id': FLAGS_ID, 'value': util.u64_to_dto(self.model.flags)},
            {'id': DIVISIBILITY_ID, 'value': util.u64_to_dto(self.model.divisibility)},
        ]
        if self.model.duration != 0:
            data.append({
                'id': DURATION_ID,
                'value': util.u64_to_dto(self.model.duration)
            })

        return data

    @classmethod
    def create_from_dto(
        cls,
        data: DTO2Type,
        network_type: OptionalNetworkType = None,
    ):
        # There's a data inconsistnecy in reply from node
        # /mosaic routes contains 'id' field
        # MosaciDefinition transactions replies with 'key' field
        for item in data:
            if (('key' in item) and ('id' not in item)):
                item['id'] = item.pop('key')

        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        # A newer version of DTO, which is used in MosaicDefinitionTransactions.
        # We need to keep the two versions separate.
        kwds = {}
        for item in data:
            kwds[PROPERTIES[item['id']]] = util.u64_from_dto(item['value'])
        return cls(MosaicProperties(**kwds))

    def to_catbuffer(
        self,
        network_type: OptionalNetworkType = None,
        fee_strategy: typing.Optional[util.FeeCalculationStrategy] = util.FeeCalculationStrategy.MEDIUM,
    ) -> bytes:
        # Serialize the required properties.
        flags = util.u8_to_catbuffer(self.model.flags)
        divisibility = util.u8_to_catbuffer(self.model.divisibility)

        # Serialize the optional properties.
        counter = 0
        optional = b''
        if self.model.duration != 0:
            counter += 1
            optional += property_to_catbuffer(DURATION_ID, self.model.duration)

        count = util.u8_to_catbuffer(counter)
        return count + flags + divisibility + optional

    @classmethod
    def create_from_catbuffer_pair(
        cls,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ):
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
        inst = cls(MosaicProperties(flags, divisibility, **kwds))
        remaining = data[size:]
        return inst, remaining
