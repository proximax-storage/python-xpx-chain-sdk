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

from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['MosaicNonce']

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


# TODO(ahuszagh) Change to an object, not an actual Model.
@util.inherit_doc
@util.dataclass(frozen=True)
class MosaicNonce(util.Model):
    """
    Nonce for a mosaic.

    :param nonce: Mosaic nonce.
    """

    nonce: bytes
    CATBUFFER_SIZE = util.U32_BYTES

    def __init__(self, nonce: typing.Union[int, str, bytes]) -> None:
        self._set('nonce', nonce_as_bytes(nonce))
        if len(self.nonce) != 4:
            raise ValueError("Nonce length is incorrect.")

    def __int__(self) -> int:
        return util.u32_from_catbuffer(self.nonce)

    @classmethod
    def create_random(cls, entropy=os.urandom):
        """
        Create new mosaic nonce from random bytes.

        :param entropy: (Optional) Callback to generate random bytes.
        """
        nonce: bytes = entropy(4)
        return cls(nonce)

    @classmethod
    def create_from_hex(cls, data: str):
        """
        Create mosaic nonce from hex-encoded nonce.

        :param data: Hex-encoded nonce data.
        """
        return cls(util.unhexlify(data))

    @classmethod
    def create_from_int(cls, nonce: int):
        """
        Create mosaic nonce from 32-bit integer.

        :param nonce: Nonce as 32-bit unsigned integer.
        """
        return cls(nonce)

    @classmethod
    def validate_dto(cls, data: int) -> bool:
        """Validate the data-transfer object."""
        return isinstance(data, int) and 0 <= data < (1 << 32)

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> int:
        return int(self)

    @classmethod
    def create_from_dto(
        cls,
        data: int,
        network_type: OptionalNetworkType = None,
    ):
        # Rest api returns negative number but it should be unsigned. Anyway, the size
        # stays 4B so this mask should be OK
        data &= 0xFFFFFFFF

        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        return cls(data)

    def to_catbuffer(
        self,
        network_type: OptionalNetworkType = None,
        fee_strategy: typing.Optional[util.FeeCalculationStrategy] = util.FeeCalculationStrategy.MEDIUM,
    ) -> bytes:
        return util.u32_to_catbuffer(int(self))

    @classmethod
    def create_from_catbuffer(
        cls,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ):
        size = cls.CATBUFFER_SIZE
        return cls(util.u32_from_catbuffer(data[:size]))
