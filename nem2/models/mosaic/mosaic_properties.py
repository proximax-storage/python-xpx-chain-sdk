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

import typing

from nem2 import util

Params = typing.Dict[str, typing.Union[bool, int]]


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


class MosaicProperties:
    """
    NEM mosaic properties.

    Properties of a custom NEM asset.
    """

    def __init__(self, flags: int, divisibility: int, duration: int):
        self._flags = flags
        # TODO(ahuszagh) Implement...

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
        """Get if levy is mutable."""

        return (self._flags & 4) == 4

    levyMutable = util.undoc(levy_mutable)

    @classmethod
    def create(cls, params: Params) -> 'MosaicProperties':
        # TODO(ahuszagh) Document...
        # Are these optional? What are the sensible defaults?
        supply_mutable = typing.cast(bool, params['supply_mutable'])
        transferable = typing.cast(bool, params['transferable'])
        levy_mutable = typing.cast(bool, params['levy_mutable'])
        flags = to_flags(supply_mutable, transferable, levy_mutable)
        return MosaicProperties(flags, params['divisibility'], params['duration'])
