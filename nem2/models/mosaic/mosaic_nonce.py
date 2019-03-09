"""
    mosaic_nonce
    ============

    Nonce for a mosaic.

    Nonces are arbitrary numbers used for cryptographic communications,
    used to avoid replay attacks.

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

import os
import struct
import typing

from nem2 import util


@util.inherit_doc
@util.dataclass(frozen=True)
class MosaicNonce(util.IntMixin, util.Model):
    """
    Nonce for a mosaic.

    :param nonce: Mosaic nonce.
    """

    nonce: bytes
    CATBUFFER_SIZE: typing.ClassVar[int] = 4

    def __init__(self, nonce: typing.Union[int, bytes]) -> None:
        if isinstance(nonce, int):
            object.__setattr__(self, 'nonce', struct.pack('<I', nonce))
        elif isinstance(nonce, bytes):
            if len(nonce) != 4:
                raise ValueError("Nonce length is incorrect.")
            object.__setattr__(self, 'nonce', nonce)
        else:
            raise TypeError(f"Invalid nonce type, got {type(nonce)}.")

    def __int__(self) -> int:
        return typing.cast(int, struct.unpack('<I', self.nonce)[0])

    @classmethod
    def create_random(cls, entropy=os.urandom) -> 'MosaicNonce':
        """
        Create new mosaic nonce from random bytes.

        :param entropy: (Optional) Callback to generate random bytes.
        """
        nonce: bytes = entropy(4)
        return cls(nonce)

    createRandom = util.undoc(create_random)

    @classmethod
    def create_from_hex(cls, data: str) -> 'MosaicNonce':
        """
        Create mosaic nonce from hex-encoded nonce.

        :param data: Hex-encoded nonce data.
        """
        return MosaicNonce(util.unhexlify(data))

    createFromHex = util.undoc(create_from_hex)

    @classmethod
    def create_from_int(cls, nonce: int) -> 'MosaicNonce':
        """
        Create mosaic nonce from 32-bit integer.

        :param nonce: Nonce as 32-bit unsigned integer.
        """
        return MosaicNonce(nonce)

    createFromInt = util.undoc(create_from_int)

    def to_dto(self) -> util.U64DTOType:
        return list(self.nonce)

    @classmethod
    def from_dto(cls, data: util.U64DTOType) -> 'MosaicNonce':
        return cls(bytes(data))

    def to_catbuffer(self) -> bytes:
        return self.nonce

    @classmethod
    def from_catbuffer(cls, data: bytes) -> typing.Tuple['MosaicNonce', bytes]:
        assert len(data) >= cls.CATBUFFER_SIZE
        inst = cls(data[:cls.CATBUFFER_SIZE])
        return inst, data[cls.CATBUFFER_SIZE:]
