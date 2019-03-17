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

from __future__ import annotations
import os
import typing

from nem2 import util
from ..blockchain.network_type import NetworkType

DTOType = typing.Sequence[int]
OptionalNetworkType = typing.Optional[NetworkType]
RawNonceType = typing.Union[int, bytes, str]


def nonce_as_bytes(nonce: RawNonceType):
    """Convert nonce to underlying byte array."""
    if isinstance(nonce, int):
        return util.u32_to_catbuffer(nonce)
    elif isinstance(nonce, str):
        return util.unhexlify(nonce)
    elif isinstance(nonce, bytes):
        return nonce
    else:
        raise TypeError(f"Invalid nonce type, got {type(nonce)}.")


@util.inherit_doc
@util.dataclass(frozen=True)
class MosaicNonce(util.IntMixin, util.Model):
    """
    Nonce for a mosaic.

    :param nonce: Mosaic nonce.
    """

    nonce: bytes
    CATBUFFER_SIZE = util.U32_BYTES

    def __init__(self, nonce: typing.Union[int, bytes]) -> None:
        self._set('nonce', nonce_as_bytes(nonce))
        if len(self.nonce) != 4:
            raise ValueError(f"Nonce length is incorrect.")

    def __int__(self) -> int:
        return util.u32_from_catbuffer(self.nonce)

    @classmethod
    def create_random(cls, entropy=os.urandom) -> MosaicNonce:
        """
        Create new mosaic nonce from random bytes.

        :param entropy: (Optional) Callback to generate random bytes.
        """
        nonce: bytes = entropy(4)
        return cls(nonce)

    createRandom = util.undoc(create_random)

    @classmethod
    def create_from_hex(cls, data: str) -> MosaicNonce:
        """
        Create mosaic nonce from hex-encoded nonce.

        :param data: Hex-encoded nonce data.
        """
        return MosaicNonce(util.unhexlify(data))

    createFromHex = util.undoc(create_from_hex)

    @classmethod
    def create_from_int(cls, nonce: int) -> MosaicNonce:
        """
        Create mosaic nonce from 32-bit integer.

        :param nonce: Nonce as 32-bit unsigned integer.
        """
        return MosaicNonce(nonce)

    createFromInt = util.undoc(create_from_int)

    def to_dto(
        self,
        network_type: OptionalNetworkType = None
    ) -> DTOType:
        return list(self.nonce)

    @classmethod
    def from_dto(
        cls,
        data: DTOType,
        network_type: OptionalNetworkType = None
    ) -> MosaicNonce:
        return cls(bytes(data))

    def to_catbuffer(
        self,
        network_type: OptionalNetworkType = None
    ) -> bytes:
        return util.u32_to_catbuffer(int(self))

    @classmethod
    def from_catbuffer(
        cls,
        data: bytes,
        network_type=None
    ) -> MosaicNonce:
        size = cls.CATBUFFER_SIZE
        return cls(util.u32_from_catbuffer(data[:size]))
