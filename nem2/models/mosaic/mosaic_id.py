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

    def __init__(self, id: int) -> None:
        """
        :param id: Raw identifier for mosaic.
        """
        self._id = id

    @property
    def id(self) -> int:
        """Get raw identifier for mosaic."""
        return self._id

    def __int__(self) -> int:
        return self.id

    def __index__(self) -> int:
        return self.__int__()

    def __repr__(self) -> str:
        return 'MosaicId(id={!r})'.format(self.id)

    def __str__(self) -> str:
        return 'MosaicId(id={!s})'.format(self.id)

    def __eq__(self, other) -> bool:
        if not isinstance(other, MosaicId):
            return False
        return self.id == other.id

    @classmethod
    def from_hex(cls, data: str) -> 'MosaicId':
        """Create instance of class from hex string."""

        return MosaicId(int(data, 16))

    def to_dto(self) -> int:
        return self.id

    to_dto.__doc__ = util.Model.to_dto.__doc__

    @classmethod
    def from_dto(cls, data: int) -> 'MosaicId':
        return cls(data)

    from_dto.__doc__ = util.Model.from_dto.__doc__

    def to_catbuffer(self) -> bytes:
        return struct.pack('<Q', self.id)

    to_catbuffer.__doc__ = util.Model.to_catbuffer.__doc__

    @classmethod
    def from_catbuffer(cls, data: bytes) -> 'MosaicId':
        assert len(data) == 8
        return cls(struct.unpack('<Q', data)[0])

    from_catbuffer.__doc__ = util.Model.from_catbuffer.__doc__
