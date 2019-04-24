"""
    register_namespace_transaction
    ==============================

    Register namespace transaction.

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
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ..namespace.namespace_id import NamespaceId
from ..namespace.namespace_name import NamespaceName
from ..namespace.namespace_type import NamespaceType
from ... import util

__all__ = [
    'RegisterNamespaceTransaction',
    'RegisterNamespaceInnerTransaction',
]


def to_namespace_id(namespace: typing.Union[str, NamespaceId]) -> NamespaceId:
    """Convert namespace name or ID to namespace ID."""

    if isinstance(namespace, str):
        return NamespaceId(namespace)
    return namespace


@util.inherit_doc
@util.dataclass(frozen=True)
@register_transaction('REGISTER_NAMESPACE')
class RegisterNamespaceTransaction(Transaction):
    """
    Register namespace transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param namespace_type: Root or sub namespace.
    :param namespace_name: Name and ID of namespace to register.
    :param duration: (Optional) Duration of the namespace.
    :param parent_id: (Optional) Parent namespace ID.
    :param signature: (Optional) Transaction signature (missing if embedded transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    namespace_type: NamespaceType
    namespace_name: NamespaceName
    duration: typing.Optional[int]
    parent_id: typing.Optional[NamespaceId]

    def __init__(
        self,
        network_type: NetworkType,
        version: TransactionVersion,
        deadline: Deadline,
        max_fee: int,
        namespace_type: NamespaceType,
        namespace_name: NamespaceName,
        duration: typing.Optional[int] = None,
        parent_id: typing.Optional[NamespaceId] = None,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None,
    ) -> None:
        if namespace_type == NamespaceType.ROOT_NAMESPACE and duration is None:
            raise ValueError('Registering a root namespace without a duration.')
        elif namespace_type == NamespaceType.SUB_NAMESPACE and parent_id is None:
            raise ValueError('Registering a sub namespace without a parent.')
        if duration is not None and parent_id is not None:
            raise ValueError('Cannot have both namespace duration and parent.')
        super().__init__(
            TransactionType.REGISTER_NAMESPACE,
            network_type,
            version,
            deadline,
            max_fee,
            signature,
            signer,
            transaction_info,
        )
        self._set('namespace_type', namespace_type)
        self._set('namespace_name', namespace_name)
        self._set('duration', duration)
        self._set('parent_id', parent_id)

    @classmethod
    def create_root_namespace(
        cls,
        deadline: Deadline,
        namespace_name: str,
        duration: int,
        network_type: NetworkType,
    ):
        """
        Create new root namespace transaction.

        :param deadline: Deadline to include transaction.
        :param namespace_name: Name of the namespace to register.
        :param duration: Duration of the namespace.
        :param network_type: Network type.
        """
        return cls(
            network_type,
            TransactionVersion.REGISTER_NAMESPACE,
            deadline,
            0,
            NamespaceType.ROOT_NAMESPACE,
            NamespaceName.create_from_name(namespace_name),
            duration,
        )

    @classmethod
    def create_sub_namespace(
        cls,
        deadline: Deadline,
        namespace_name: str,
        parent_namespace: typing.Union[str, NamespaceId],
        network_type: NetworkType,
    ):
        """
        Create new sub namespace transaction.

        Multiple parent names may be provided using a `.` delimiter to
        separate parent namespaces, up to a depth of 2, or a parent
        namespace identifier may be provided instead.

        :param deadline: Deadline to include transaction.
        :param namespace_name: Name of the namespace to register.
        :param parent_namespace: Name or identifier of the parent namespace.
        :param network_type: Network type.
        """
        parent_id = to_namespace_id(parent_namespace)
        id = util.generate_sub_namespace_id(parent_id.id, namespace_name)
        return cls(
            network_type,
            TransactionVersion.REGISTER_NAMESPACE,
            deadline,
            0,
            NamespaceType.SUB_NAMESPACE,
            NamespaceName(NamespaceId(id), namespace_name),
            None,
            parent_id
        )

    @property
    def namespace_id(self) -> NamespaceId:
        """Get the namespace ID from name struct."""
        return self.namespace_name.namespace_id

    @property
    def name(self) -> str:
        """Get the namespace name from name struct."""
        return self.namespace_name.name

    # CATBUFFER

    def catbuffer_size_specific(self) -> int:
        # Duration size includes both either the parent ID or the duration.
        # We have 1 extra byte, as a marker for the size of the namespace name.
        extra_size = util.U8_BYTES
        namespace_type_size = util.U8_BYTES
        duration_size = util.U64_BYTES
        namespace_id_size = NamespaceId.CATBUFFER_SIZE
        namespace_name_size = util.U8_BYTES * len(self.namespace_name.name)
        return (
            extra_size
            + namespace_type_size
            + duration_size
            + namespace_id_size
            + namespace_name_size
        )

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export register namespace-specific data to catbuffer."""

        # uint8_t namespace_type
        # uint64_t duration || parent_id
        # NamespaceName namespace_name
        namespace_type = self.namespace_type.to_catbuffer(network_type)
        if self.duration is not None:
            duration_or_id = util.u64_to_catbuffer(self.duration)
        else:
            duration_or_id = self.parent_id.to_catbuffer(network_type)
        namespace_name = self.namespace_name.to_catbuffer(network_type)

        return namespace_type + duration_or_id + namespace_name

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load transfer-specific data from catbuffer."""

        # uint8_t namespace_type
        # uint64_t duration || parent_id
        # NamespaceName namespace_name
        namespace_type, data = NamespaceType.from_catbuffer_pair(data, network_type)
        if namespace_type == NamespaceType.ROOT_NAMESPACE:
            duration = util.u64_from_catbuffer(data[:8])
            parent_id = None
        else:
            duration = None
            parent_id = NamespaceId.from_catbuffer(data, network_type)
        namespace_name, data = NamespaceName.from_catbuffer_pair(data[8:], network_type)

        self._set('namespace_type', namespace_type)
        self._set('namespace_name', namespace_name)
        self._set('duration', duration)
        self._set('parent_id', parent_id)

        return data

    # DTO

    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        data = self.namespace_name.to_dto(network_type)
        data.update({'namespaceType': self.namespace_type.to_dto(network_type)})

        if self.duration is not None:
            data['duration'] = util.u64_to_dto(self.duration)
        if self.parent_id is not None:
            data['parentId'] = self.parent_id.to_dto(network_type)

        return data

    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        namespace_type = NamespaceType.from_dto(data['namespaceType'], network_type)
        namespace_name = NamespaceName.from_dto(data, network_type)
        if namespace_type == NamespaceType.ROOT_NAMESPACE:
            duration = util.u64_from_dto(data['duration'])
            parent_id = None
        else:
            duration = None
            parent_id = NamespaceId.from_dto(data['parentId'], network_type)

        self._set('namespace_type', namespace_type)
        self._set('namespace_name', namespace_name)
        self._set('duration', duration)
        self._set('parent_id', parent_id)


@register_transaction('REGISTER_NAMESPACE')
class RegisterNamespaceInnerTransaction(InnerTransaction, RegisterNamespaceTransaction):
    """Embedded transfer transaction."""

    __slots__ = ()
