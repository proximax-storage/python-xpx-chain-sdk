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

from .deadline import Deadline
from .inner_transaction import InnerTransaction
from .registry import register_transaction
from .transaction import Transaction
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.address import Address
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ..namespace.alias_action_type import AliasActionType
from ..namespace.namespace_id import NamespaceId
from ... import util

__all__ = [
    'AddressAliasTransaction',
    'AddressAliasInnerTransaction',
]


@util.inherit_doc
@util.dataclass(frozen=True)
@register_transaction('ADDRESS_ALIAS')
class AddressAliasTransaction(Transaction):
    """
    Address alias transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param action_type: Alias action type.
    :param namespace_id: Resulting namespace ID that will be an alias.
    :param address: Address to be aliased.
    :param signature: (Optional) Transaction signature (missing if embedded transaction).
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
        action_type: AliasActionType,
        namespace_id: NamespaceId,
        address: Address,
        max_fee: int = 0,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None,
    ) -> None:
        super().__init__(
            TransactionType.ADDRESS_ALIAS,
            network_type,
            version,
            deadline,
            max_fee,
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
        max_fee: int = 0,
    ):
        """
        Create new address alias transaction.

        :param deadline: Deadline to include transaction.
        :param action_type: Alias action type.
        :param namespace_id: Resulting namespace ID that will be an alias.
        :param address: Address to be aliased.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """
        return cls(
            network_type,
            TransactionVersion.ADDRESS_ALIAS,
            deadline,
            action_type,
            namespace_id,
            address,
            max_fee,
        )

    # CATBUFFER

    def catbuffer_size_specific(self) -> int:
        action_type_size = AliasActionType.CATBUFFER_SIZE
        namespace_id_size = util.U64_BYTES
        address_size = 25 * util.U8_BYTES
        return action_type_size + namespace_id_size + address_size

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export address alias-specific data to catbuffer."""

        # uint8_t action_type
        # uint64_t namespace_id
        # Address address
        action_type = self.action_type.to_catbuffer(network_type)
        namespace_id = util.u64_to_catbuffer(int(self.namespace_id))
        address = self.address.encoded

        return action_type + namespace_id + address

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load address alias-specific data data from catbuffer."""

        # uint8_t action_type
        # uint64_t namespace_id
        # Address address
        action_type = AliasActionType.create_from_catbuffer(data, network_type)
        namespace_id = NamespaceId(util.u64_from_catbuffer(data[1:9]))
        address = Address.create_from_encoded(data[9:34])
        data = data[34:]

        self._set('action_type', action_type)
        self._set('namespace_id', namespace_id)
        self._set('address', address)

        return data

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'aliasAction', 'namespaceId', 'address'}
        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        return {
            'aliasAction': self.action_type.to_dto(network_type),
            'namespaceId': util.u64_to_dto(int(self.namespace_id)),
            'address': util.hexlify(self.address.encoded),
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        action_type = AliasActionType.create_from_dto(data['aliasAction'], network_type)
        namespace_id = NamespaceId(util.u64_from_dto(data['namespaceId']))
        address = Address.create_from_encoded(data['address'])

        self._set('action_type', action_type)
        self._set('namespace_id', namespace_id)
        self._set('address', address)


@register_transaction('ADDRESS_ALIAS')
class AddressAliasInnerTransaction(InnerTransaction, AddressAliasTransaction):
    """Embedded address alias transaction."""

    __slots__ = ()
