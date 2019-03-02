"""
    account_info
    ============

    Account data and metadata pair.

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

from typing import Sequence

from nem2 import util
from .public_account import PublicAccount
from ..mosaic import Mosaic

MosaicListType = Sequence[Mosaic]


class AccountInfo:
    """Basic information describing a NEM account."""

    def __init__(self,
        # TODO(ahuszagh) Need to describe the metadata structure.
        # THis isn't described even in the typescript SDK.
        meta,
        address: Address,
        address_height: int,
        public_key: str,
        public_key_height: int,
        mosaics: MosaicListType,
        importance: int,
        importance_height: int,
    ):
        self._meta = meta
        self._address = address
        self._address_height = address_height
        self._public_key = public_key
        self._public_key_height = public_key_height
        self._mosaics = mosaics
        self._importance = importance
        self._importance_height = importance_height

    @property
    def address(self):
        """Get address."""
        return self._address

    @property
    def address_height(self):
        return self._address_height

    addressHeight = util.undoc(address_height)

    @property
    def public_key(self):
        """Get public key."""
        return self._public_key

    publicKey = util.undoc(public_key)

    @property
    def public_key_height(self):
        return self._public_key_height

    publicKeyHeight = util.undoc(public_key_height)

    @property
    def mosaics(self):
        return self._mosaics

    @property
    def importance(self):
        """Get account importance."""
        return self._importance

    @property
    def importance_height(self):
        return self._importance_height

    importanceHeight = util.undoc(importance_height)

    @property
    def public_account(self) -> PublicAccount:
        """Get public account."""
        return PublicAccount(self.address, self.public_key)

    publicAccount = util.undoc(public_account)
