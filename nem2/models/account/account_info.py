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

from __future__ import annotations
import typing

from nem2 import util
from .address import Address
from .public_account import PublicAccount
from ..mosaic.mosaic import Mosaic

MosaicListType = typing.Sequence[Mosaic]


@util.inherit_doc
@util.dataclass(frozen=True)
class AccountInfo:
    """
    Basic information describing an account.

    :param meta: Account metadata.
    :param address: Account address.
    :param address_height: Chain height when address was published.
    :param public_key: Account public key.
    :param public_key_height: Chain height when public key was published.
    :param mosaics: List of mosaics owned by account.
    :param importance: Importance of the account.
    :param importance_height: Importance height of the account.
    """

    meta: typing.Any       # TODO(ahuszagh) Fix...
    address: Address
    address_height: int
    public_key: str
    public_key_height: int
    mosaics: MosaicListType
    importance: int
    importance_height: int

    @property
    def public_account(self) -> PublicAccount:
        """Get public account."""
        return PublicAccount(self.address, self.public_key)

    publicAccount = util.undoc(public_account)
