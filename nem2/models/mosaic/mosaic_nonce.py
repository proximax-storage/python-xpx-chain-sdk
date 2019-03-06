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

from nem2 import util


class MosaicNonce(util.Model):
    """Nonce for a mosaic."""

    __slots__ = ('_nonce',)

    def __init__(self, nonce: bytes) -> None:
        """
        :param nonce: Mosaic nonce.
        """
        if len(nonce) != 4:
            raise ValueError("Nonce length is incorrect.")
        self._nonce = nonce

    @property
    def nonce(self) -> bytes:
        """Get mosaic nonce."""
        return self._nonce

    def __int__(self) -> int:
        return struct.unpack('<I', self.nonce)[0]

    def __index__(self) -> int:
        return self.__int__()

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

    @util.doc(util.Model.tie)
    def tie(self) -> tuple:
        return super().tie()

    @util.doc(util.Model.to_dto)
    def to_dto(self) -> util.Uint64DtoType:
        return list(self.nonce)

    @util.doc(util.Model.from_dto)
    @classmethod
    def from_dto(cls, data: util.Uint64DtoType) -> 'MosaicNonce':
        return cls(bytes(data))

    @util.doc(util.Model.to_catbuffer)
    def to_catbuffer(self) -> bytes:
        return self.nonce

    @util.doc(util.Model.from_catbuffer)
    @classmethod
    def from_catbuffer(cls, data: bytes) -> ('MosaicNonce', bytes):
        assert len(data) >= 4
        inst = cls(data[:4])
        return inst, data[4:]
