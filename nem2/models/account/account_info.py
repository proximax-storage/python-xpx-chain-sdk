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

import typing

from nem2 import util
from .public_account import PublicAccount

if typing.TYPE_CHECKING:
    from .address import Address
    from ..mosaic.mosaic import Mosaic      # noqa: F401

MosaicListType = typing.Sequence['Mosaic']


class AccountInfo(util.Tie):
    """Basic information describing an account."""

    # _meta: any
    _address: 'Address'
    _address_height: int
    _public_key: str
    _public_key_height: int
    _mosaics: MosaicListType
    _importance: int
    _importance_height: int

    def __init__(self,
        # TODO(ahuszagh) Need to describe the metadata structure.
        # THis isn't described even in the typescript SDK.
        # https://github.com/nemtech/nem2-sdk-typescript-javascript/blob/master/src/infrastructure/AccountHttp.ts
        meta,
        address: 'Address',
        address_height: int,
        public_key: str,
        public_key_height: int,
        mosaics: MosaicListType,
        importance: int,
        importance_height: int,
    ) -> None:
        """
        :param meta: Account metadata.
        :param address: Account address.
        :param address_height: Chain height when address was published.
        :param public_key: Account public key.
        :param public_key_height: Chain height when public key was published.
        :param mosaics: List of mosaics owned by account.
        :param importance: Importance of the account.
        :param importance_height: Importance height of the account.
        """
        self._meta = meta
        self._address = address
        self._address_height = address_height
        self._public_key = public_key
        self._public_key_height = public_key_height
        self._mosaics = mosaics
        self._importance = importance
        self._importance_height = importance_height

# TODO(ahuszagh) Restore.
#    @property
#    def meta(self) -> Address:
#        """Get account metadata."""
#        return self._meta

    @property
    def address(self) -> 'Address':
        """Get address."""
        return self._address

    @property
    def address_height(self) -> int:
        """Get chain height when address was published."""
        return self._address_height

    addressHeight = util.undoc(address_height)

    @property
    def public_key(self) -> str:
        """Get public key."""
        return self._public_key

    publicKey = util.undoc(public_key)

    @property
    def public_key_height(self) -> int:
        """Get chain height when public key was published."""
        return self._public_key_height

    publicKeyHeight = util.undoc(public_key_height)

    @property
    def mosaics(self) -> MosaicListType:
        """Get list of mosaics owned by account."""
        return self._mosaics

    @property
    def importance(self) -> int:
        """Get account importance."""
        return self._importance

    @property
    def importance_height(self) -> int:
        """Get importance height of the account."""
        return self._importance_height

    importanceHeight = util.undoc(importance_height)

    @property
    def public_account(self) -> 'PublicAccount':
        """Get public account."""
        return PublicAccount(self.address, self.public_key)

    publicAccount = util.undoc(public_account)
