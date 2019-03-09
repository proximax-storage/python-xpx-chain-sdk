"""
    mosaic
    ======

    Description of an asset.

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
from .mosaic_id import MosaicId


@util.inherit_doc
@util.dataclass(frozen=True, amount=0)
class Mosaic(util.Model):
    """
    Basic information describing a mosaic.

    :param id: Identifier for mosaic.
    :param amount: Mosaic quantity in the smallest unit possible.
    """

    id: 'MosaicId'
    amount: int

    def to_dto(self) -> dict:
        return {
            'amount': util.uint64_to_dto(self.amount),
            'id': self.id.to_dto(),
        }

    @classmethod
    def from_dto(cls, data: dict) -> 'Mosaic':
        amount = util.dto_to_uint64(data['amount'])
        return cls(MosaicId.from_dto(data['id']), amount)

    def to_catbuffer(self) -> bytes:
        id: bytes = self.id.to_catbuffer()
        amount: bytes = struct.pack('<Q', self.amount)
        return id + amount

    @classmethod
    def from_catbuffer(cls, data: bytes) -> typing.Tuple['Mosaic', bytes]:
        assert len(data) >= 16
        id = MosaicId.from_catbuffer(data)[0]
        amount = struct.unpack('<Q', data[8:16])[0]
        inst = cls(id, amount)
        return inst, data[16:]
