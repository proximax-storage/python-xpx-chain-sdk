"""
    mosaic_supply_type
    ==================

    Constants for the mosaic supply type.

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

import enum
import struct

from nem2 import util


class MosaicSupplyType(util.enum_catbuffer(enum.IntEnum)):
    """Identifier for the mosaic supply type."""

    DECREASE = 0
    INCREASE = 1

    def description(self) -> str:
        """Describe enumerated values in detail."""

        return DESCRIPTION[self]

    @util.doc(util.Catbuffer.to_catbuffer.__doc__)
    def to_catbuffer(self) -> bytes:
        return struct.pack('<B', int(self))

    @util.doc(util.Catbuffer.from_catbuffer.__doc__)
    @classmethod
    def from_catbuffer(cls, data: bytes) -> ('MosaicSupplyType', bytes):
        assert len(data) >= 1
        inst = cls(struct.unpack('<B', data[:1])[0])
        return inst, data[1:]

DESCRIPTION = {
    MosaicSupplyType.DECREASE: "Decrease mosaic supply.",
    MosaicSupplyType.INCREASE: "Increase mosaic supply.",
}
