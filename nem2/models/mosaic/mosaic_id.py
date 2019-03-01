"""
    mosaic_id
    =========

    Identifier for a NEM asset.

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

from nem2 import util


class MosaicId(util.Model):
    """
    NEM mosaic identifier.

    Unique identifier for a custom NEM asset.
    """

    def __init__(self, id: int):
        self._id = id

    @property
    def id(self) -> int:
        return self._id

    def __int__(self):
        return self.id

    def __index__(self):
        return self.__int__()

    def __repr__(self):
        return 'MosaicId(id={!r})'.format(self.id)

    def __str__(self):
        return 'MosaicId(id={!s})'.format(self.id)

    def __eq__(self, other):
        if not isinstance(other, MosaicId):
            return False
        return self.id == other.id

    @classmethod
    def from_hex(cls, data: str) -> 'MosaicId':
        """Create instance of class from hex string."""

        return MosaicId(int(data, 16))

    def to_dto(self):
        return self.id

    @classmethod
    def from_dto(cls, data: int):
        return cls(data)

    def to_catbuffer(self):
        return struct.pack('<Q', self.id)

    @classmethod
    def from_catbuffer(cls, data: bytes):
        assert len(data) == 8
        return cls(struct.unpack('<Q', data)[0])

