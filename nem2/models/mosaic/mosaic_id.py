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
import typing

from nem2 import util

if typing.TYPE_CHECKING:
    from .mosaic_nonce import MosaicNonce
    from ..account.public_account import PublicAccount


@util.inherit_doc
@util.dataclass(frozen=True, id=0)
class MosaicId(util.IntMixin, util.Model):
    """
    Mosaic identifier.

    :param id: Raw identifier for mosaic.
    """

    id: int
    CATBUFFER_SIZE: typing.ClassVar[int] = 8

    def __int__(self) -> int:
        return self.id

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

    def to_dto(self) -> util.U64DTOType:
        return util.uint64_to_dto(self.id)

    @classmethod
    def from_dto(cls, data: util.U64DTOType) -> 'MosaicId':
        return cls(util.dto_to_uint64(data))

    def to_catbuffer(self) -> bytes:
        return struct.pack('<Q', self.id)

    @classmethod
    def from_catbuffer(cls, data: bytes) -> typing.Tuple['MosaicId', bytes]:
        assert len(data) >= cls.CATBUFFER_SIZE
        inst = cls(struct.unpack('<Q', data[:cls.CATBUFFER_SIZE])[0])
        return inst, data[cls.CATBUFFER_SIZE:]
