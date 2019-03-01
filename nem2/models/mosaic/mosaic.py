"""
    mosaic_id
    =========

    Description of a NEM asset.

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
from .mosaic_id import MosaicId


class Mosaic(util.Model):
    """
    NEM mosaic.

    Describes an instance of a custom NEM asset.
    """

    def __init__(self, id: MosaicId, amount: int) -> None:
        self._id = id
        self._amount = amount

    @property
    def id(self) -> MosaicId:
        return self._id

    @property
    def amount(self) -> int:
        return self._amount

    def __repr__(self) -> str:
        return 'Mosaic(id={!r}, amount={!r})'.format(self.id, self.amount)

    def __str__(self) -> str:
        return 'Mosaic(id={!s}, amount={!s})'.format(self.id, self.amount)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Mosaic):
            return False
        return (self.id, self.amount) == (other.id, other.amount)

    def to_dto(self) -> dict:
        return {'amount': self.amount, 'id': self.id.to_dto()}

    to_dto.__doc__ = util.Model.to_dto.__doc__

    @classmethod
    def from_dto(cls, data: dict) -> 'Mosaic':
        return cls(MosaicId.from_dto(data['id']), data['amount'])

    from_dto.__doc__ = util.Model.from_dto.__doc__

    def to_catbuffer(self) -> bytes:
        return self.id.to_catbuffer() + struct.pack('<Q', self.amount)

    to_catbuffer.__doc__ = util.Model.to_catbuffer.__doc__

    @classmethod
    def from_catbuffer(cls, data: bytes) -> 'Mosaic':
        assert len(data) == 16
        id = MosaicId.from_catbuffer(data[:8])
        amount = struct.unpack('<Q', data[8:])[0]
        return cls(id, amount)

    from_catbuffer.__doc__ = util.Model.from_catbuffer.__doc__
