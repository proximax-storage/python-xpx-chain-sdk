"""
    network_currency_mosaic
    =======================

    Description of a per-network currency mosaic.

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

from .mosaic import Mosaic
from ..blockchain.network_type import OptionalNetworkType
from ..namespace.namespace_id import NamespaceId
from ... import util

__all__ = ['NetworkCurrencyMosaic']


class NetworkCurrencyMosaic(Mosaic):
    """
    Per-network currency mosaic.

    :param amount: Mosaic quantity in the smallest unit possible.
    :cvar NAMESPACE_ID: Namespace identifier for asset.
    :cvar DIVISIBILITY: Decimal place mosaic can be divided into.
    :cvar INITIAL_SUPPLY: Initial supply of asset.
    :cvar TRANSFERABLE: Allow transfer of funds from accounts other than creator.
    :cvar SUPPLY_MUTABLE: Mosaic allows supply change later.
    :cvar LEVY_MUTABLE: If levy is mutable.
    """

    __slots__ = ()
    NAMESPACE_ID: typing.ClassVar[NamespaceId] = NamespaceId("cat.currency")
    DIVISIBILITY: typing.ClassVar[int] = 6
    INITIAL_SUPPLY: typing.ClassVar[int] = 8999999998
    TRANSFERABLE: typing.ClassVar[bool] = True
    SUPPLY_MUTABLE: typing.ClassVar[bool] = False
    LEVY_MUTABLE: typing.ClassVar[bool] = False

    def __init__(self, amount: int) -> None:
        super().__init__(self.NAMESPACE_ID, amount)

    @classmethod
    def create_relative(cls, amount: int):
        """
        Create `NetworkCurrencyMosaic` using relative (divisibility) units.

        :param amount: Mosaic quantity in relative units.

        Example:
            .. code-block:: python

                >>> NetworkCurrencyMosaic.create_relative(1).amount
                1000000
        """
        return cls(amount * 10 ** cls.DIVISIBILITY)

    @classmethod
    def create_absolute(cls, amount: int):
        """
        Create `NetworkCurrencyMosaic` using absolute (smallest) units.

        :param amount: Mosaic quantity in absolute units.

        Example:
            .. code-block:: python

                >>> NetworkCurrencyMosaic.create_relative(1).amount
                1
        """
        return cls(amount)

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        id = NamespaceId(util.u64_from_dto(data['id']))
        amount = util.u64_from_dto(data['amount'])
        if int(id) != int(cls.NAMESPACE_ID):
            raise ValueError('Network currency mosaic ID does not match.')
        return cls(amount)

    @classmethod
    def create_from_catbuffer(
        cls,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ):
        id = NamespaceId(util.u64_from_catbuffer(data[:8]))
        amount = util.u64_from_catbuffer(data[8:16])
        if int(id) != int(cls.NAMESPACE_ID):
            raise ValueError('Network currency mosaic ID does not match.')
        return cls(amount)
