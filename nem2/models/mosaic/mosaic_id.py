"""
    mosaic_id
    =========

    Identifier for an asset.

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
    """Mosaic identifier."""

    __slots__ = ('_id',)
    _id: int

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

    def __format__(self, format_spec: str):
        return int(self).__format__(format_spec)

    @classmethod
    def from_hex(cls, data: str) -> 'MosaicId':
        """
        Create instance of class from hex string.

        :param data: Hex-encoded ID data (with or without '0x' prefix).
        """

        return MosaicId(int(data, 16))

    @classmethod
    def create_from_nonce(cls, nonce: 'MosaicNonce', owner: 'PublicAccount') -> 'MosaicId':
        """
        Create mosaic ID from nonce and owner.

        :param nonce: Mosaic nonce.
        :param owner: Account of mosaic owner.
        """
        key: bytes = util.unhexlify(owner.public_key)
        return cls(util.generate_mosaic_id(nonce.nonce, key))

    createFromNonce = util.undoc(create_from_nonce)

    @util.doc(util.Tie.tie)
    def tie(self) -> tuple:
        return super().tie()

    @util.doc(util.Model.to_dto)
    def to_dto(self) -> util.Uint64DtoType:
        return util.uint64_to_dto(self.id)

    @util.doc(util.Model.from_dto)
    @classmethod
    def from_dto(cls, data: util.Uint64DtoType) -> 'MosaicId':
        return cls(util.dto_to_uint64(data))

    @util.doc(util.Model.to_catbuffer)
    def to_catbuffer(self) -> bytes:
        return struct.pack('<Q', self.id)

    @util.doc(util.Model.from_catbuffer)
    @classmethod
    def from_catbuffer(cls, data: bytes) -> ('MosaicId', bytes):
        assert len(data) >= 8
        inst = cls(struct.unpack('<Q', data[:8])[0])
        return inst, data[8:]
