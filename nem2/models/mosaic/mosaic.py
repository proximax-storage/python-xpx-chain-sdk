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

    __slots__ = (
        '_id',
        '_amount',
    )

    def __init__(self, id: MosaicId, amount: int) -> None:
        """
        :param id: Identifier for mosaic.
        :param amount: Mosaic quantity in the smallest unit possible.
        """
        self._id = id
        self._amount = amount

    @property
    def id(self) -> MosaicId:
        """Get identifier for mosaic."""
        return self._id

    @property
    def amount(self) -> int:
        """Get mosaic quantity in the smallest unit possible."""
        return self._amount

    @util.doc(util.Tie.tie.__doc__)
    def tie(self) -> tuple:
        return super().tie()

    @util.doc(util.Model.to_dto.__doc__)
    def to_dto(self) -> dict:
        return {
            'amount': util.uint64_to_dto(self.amount),
            'id': self.id.to_dto(),
        }

    @util.doc(util.Model.from_dto.__doc__)
    @classmethod
    def from_dto(cls, data: dict) -> 'Mosaic':
        amount = util.dto_to_uint64(data['amount'])
        return cls(MosaicId.from_dto(data['id']), amount)

    @util.doc(util.Model.to_catbuffer.__doc__)
    def to_catbuffer(self) -> bytes:
        return self.id.to_catbuffer() + struct.pack('<Q', self.amount)

    @util.doc(util.Model.from_catbuffer.__doc__)
    @classmethod
    def from_catbuffer(cls, data: bytes) -> ('Mosaic', bytes):
        assert len(data) >= 16
        id = MosaicId.from_catbuffer(data)[0]
        amount = struct.unpack('<Q', data[8:16])[0]
        inst = cls(id, amount)
        return inst, data[16:]
