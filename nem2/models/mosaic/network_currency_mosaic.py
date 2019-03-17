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

from nem2 import util
from .mosaic import Mosaic
from .mosaic_id import MosaicId
from ..namespace.namespace_id import NamespaceId


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
        mosaic_id = MosaicId(self.NAMESPACE_ID.id)
        super().__init__(mosaic_id, amount)

    @classmethod
    def create_relative(cls, amount: int) -> NetworkCurrencyMosaic:
        """
        Create `NetworkCurrencyMosaic` using relative (divisibility) units.

        :param amount: Mosaic quantity in relative units.

        Example:
            .. code-block:: python

                >>> NetworkCurrencyMosaic.create_relative(1).amount
                1000000
        """
        return NetworkCurrencyMosaic(amount * 10 ** cls.DIVISIBILITY)

    createRelative = util.undoc(create_relative)

    @classmethod
    def create_absolute(cls, amount: int) -> NetworkCurrencyMosaic:
        """
        Create `NetworkCurrencyMosaic` using absolute (smallest) units.

        :param amount: Mosaic quantity in absolute units.

        Example:
            .. code-block:: python

                >>> NetworkCurrencyMosaic.create_relative(1).amount
                1
        """
        return NetworkCurrencyMosaic(amount)

    createAbsolute = util.undoc(create_absolute)
