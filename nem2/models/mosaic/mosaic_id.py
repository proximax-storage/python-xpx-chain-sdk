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

from __future__ import annotations

from .mosaic_nonce import MosaicNonce
from ..account.public_account import PublicAccount
from ... import util

__all__ = ['MosaicId']


@util.inherit_doc
@util.dataclass(frozen=True, id=0)
class MosaicId(util.IntMixin, util.Object):
    """
    Mosaic identifier.

    :param id: Raw identifier for mosaic.
    """

    id: int

    def __int__(self) -> int:
        return self.id

    def get_id(self) -> str:
        return util.hexlify(self.id.to_bytes(8, 'big'))

    @classmethod
    def create_from_nonce(
        cls,
        nonce: MosaicNonce,
        owner: PublicAccount,
    ):
        """
        Create mosaic ID from nonce and owner.

        :param nonce: Mosaic nonce.
        :param owner: Account of mosaic owner.
        """
        key = util.unhexlify(owner.public_key)
        return cls(util.generate_mosaic_id(nonce.nonce, key))
