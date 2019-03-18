"""
    alias_transaction
    =================

    Abstract class for alias transactions.

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

from nem2 import util
from .deadline import Deadline
from .transaction import Transaction
from ..account.address import Address
from ..blockchain.network_type import NetworkType
from ..mosaic.mosaic_id import MosaicId
from ..namespace.alias_action_type import AliasActionType
from ..namespace.namespace_id import NamespaceId

__all__ = ['AliasTransaction']


class AliasTransaction(Transaction):
    """Abstract class for alias transactions."""

    __slots__ = ()

    @classmethod
    def create_for_address(
        cls,
        deadline: Deadline,
        action_type: AliasActionType,
        namespace_id: NamespaceId,
        address: Address,
        network_type: NetworkType,
    ):
        """
        Create new address alias transaction.

        :param deadline: Deadline to include transaction.
        :param action_type: Alias action type.
        :param namespace_id: Resulting namespace ID that will be an alias.
        :param address: Address to be aliased.
        :param network_type: Network type.
        """

        from . import address_alias_transaction as mod
        return mod.AddressAliasTransaction.create(
            deadline,
            action_type,
            namespace_id,
            address,
            network_type,
        )

    createForAddress = util.undoc(create_for_address)

    @classmethod
    def create_for_mosaic(
        cls,
        deadline: Deadline,
        action_type: AliasActionType,
        namespace_id: NamespaceId,
        mosaic_id: MosaicId,
        network_type: NetworkType,
    ):
        """
        Create new mosaic alias transaction.

        :param deadline: Deadline to include transaction.
        :param action_type: Alias action type.
        :param namespace_id: Resulting namespace ID that will be an alias.
        :param mosaic_id: Mosaic to be aliased.
        :param network_type: Network type.
        """

        from . import mosaic_alias_transaction as mod
        return mod.MosaicAliasTransaction.create(
            deadline,
            action_type,
            namespace_id,
            mosaic_id,
            network_type,
        )

    createForMosaic = util.undoc(create_for_mosaic)
