"""
    address_alias_transaction
    =========================

    Address alias transaction.

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
from .alias_transaction import AliasTransaction
from .deadline import Deadline
from .inner_transaction import InnerTransaction
from .transaction import Transaction
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.address import Address
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ..namespace.alias_action_type import AliasActionType
from ..namespace.namespace_id import NamespaceId

__all__ = [
    'AddressAliasTransaction',
    'AddressAliasInnerTransaction',
]

OptionalNetworkType = typing.Optional[NetworkType]


@util.inherit_doc
@util.dataclass(frozen=True)
class AddressAliasTransaction(AliasTransaction):
    """
    Address alias transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param fee: Fee for the transaction. Higher fees increase transaction priority.
    :param action_type: Alias action type.
    :param namespace_id: Resulting namespace ID that will be an alias.
    :param address: Address to be aliased.
    :param signature: (Optional) Transaction signature (missing if aggregate transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    action_type: AliasActionType
    namespace_id: NamespaceId
    address: Address

    def __init__(
        self,
        network_type: NetworkType,
        version: TransactionVersion,
        deadline: Deadline,
        fee: int,
        action_type: AliasActionType,
        namespace_id: NamespaceId,
        address: Address,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None,
    ):
        super().__init__(
            TransactionType.ADDRESS_ALIAS,
            network_type,
            version,
            deadline,
            fee,
            signature,
            signer,
            transaction_info,
        )
        self._set('action_type', action_type)
        self._set('namespace_id', namespace_id)
        self._set('address', address)

    @classmethod
    def create(
        cls,
        deadline: Deadline,
        action_type: AliasActionType,
        namespace_id: NamespaceId,
        address: Address,
        network_type: NetworkType,
    ) -> AddressAliasTransaction:
        """
        Create new address alias transaction.

        :param deadline: Deadline to include transaction.
        :param action_type: Alias action type.
        :param namespace_id: Resulting namespace ID that will be an alias.
        :param address: Address to be aliased.
        :param network_type: Network type.
        """
        return AddressAliasTransaction(
            network_type,
            TransactionVersion.ADDRESS_ALIAS,
            deadline,
            0,
            action_type,
            namespace_id,
            address
        )

    def catbuffer_size_specific(self) -> int:
        action_type_size = AliasActionType.CATBUFFER_SIZE
        namespace_id_size = NamespaceId.CATBUFFER_SIZE
        address_size = Address.CATBUFFER_SIZE
        return action_type_size + namespace_id_size + address_size

    def to_catbuffer_specific(
        self,
        network_type: OptionalNetworkType = None,
    ) -> bytes:
        """Export address alias-specific data to catbuffer."""

        # uint8_t action_type
        # NamespaceId namespace_id
        # Address address
        action_type = self.action_type.to_catbuffer()
        namespace_id = self.namespace_id.to_catbuffer()
        address = self.address.to_catbuffer()

        return action_type + namespace_id + address

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ) -> bytes:
        """Load address alias-specific data data from catbuffer."""

        # uint8_t action_type
        # NamespaceId namespace_id
        # Address address
        action_type, data = AliasActionType.from_catbuffer_pair(data, network_type)
        namespace_id, data = NamespaceId.from_catbuffer_pair(data, network_type)
        address, data = Address.from_catbuffer_pair(data, network_type)

        self._set('action_type', action_type)
        self._set('namespace_id', namespace_id)
        self._set('address', address)

        return typing.cast(bytes, data)

    def to_aggregate(
        self,
        signer: PublicAccount
    ) -> AddressAliasInnerTransaction:
        """Convert transaction to inner transaction."""
        inst = AddressAliasInnerTransaction.from_transaction(self, signer)
        return typing.cast(AddressAliasInnerTransaction, inst)


class AddressAliasInnerTransaction(InnerTransaction, AddressAliasTransaction):
    """Embedded address alias transaction."""

    __slots__ = ()


Transaction.HOOKS[TransactionType.ADDRESS_ALIAS] = (
    AddressAliasTransaction.from_catbuffer_pair,
    AddressAliasTransaction.from_dto,
)


InnerTransaction.HOOKS[TransactionType.ADDRESS_ALIAS] = (
    AddressAliasInnerTransaction.from_catbuffer_pair,
    AddressAliasInnerTransaction.from_dto,
)
