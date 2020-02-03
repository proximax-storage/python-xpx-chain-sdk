"""
    modify_namespace_metadata_transaction
    =========================

    Modify namespace metadata transaction.

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
from ..namespace.namespace_id import NamespaceId
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ..metadata.metadata_type import MetadataType
from ..metadata.metadata_modification_type import MetadataModificationType
from ..metadata.metadata_modification import MetadataModification
from ... import util


MetadataModificationList = typing.Sequence[MetadataModification]

__all__ = [
    'ModifyNamespaceMetadataTransaction',
    'ModifyNamespaceMetadataInnerTransaction',
]

TYPES = (
    TransactionType.MODIFY_NAMESPACE_METADATA,
)


@util.inherit_doc
@util.dataclass(frozen=True)
@register_transaction('MODIFY_NAMESPACE_METADATA')
class ModifyNamespaceMetadataTransaction(Transaction):
    """
    Modify namespace metadata transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param metadata_type: type of the metadata
    :param metadata_id: namespace ID for which metadata is modified (used only when address is not specified)
    :param modifications: the modification to make
    :param signature: (Optional) Transaction signature (missing if embedded transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.

    """

    metadata_type: MetadataType
    metadata_id: NamespaceId
    modifications: MetadataModificationList

    def __init__(
        self,
        network_type: NetworkType,
        type: TransactionType,
        version: TransactionVersion,
        deadline: Deadline,
        metadata_type: MetadataType,
        metadata_id: NamespaceId,
        modifications: MetadataModificationList,
        max_fee: int = 0,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None,
    ) -> None:
        if type not in TYPES:
            raise ValueError('Invalid transaction type.')
        super().__init__(
            type,
            network_type,
            version,
            deadline,
            max_fee,
            signature,
            signer,
            transaction_info,
        )
        self._set('metadata_type', metadata_type)
        self._set('metadata_id', metadata_id)
        self._set('modifications', modifications)

    @classmethod
    def create(
        cls,
        deadline: Deadline,
        metadata_type: MetadataType,
        metadata_id: NamespaceId,
        modifications: MetadataModificationList,
        network_type: NetworkType,
        max_fee: int = 0,
    ):
        """
        Create new namespace metadata modification transaction.

        :param deadline: Deadline to include transaction.
        :param metadata_type: type of the metadata
        :param metadata_id: namespace for which metadata is modified
        :param modifications: the modification to make
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """
        return cls(
            network_type,
            TransactionType.MODIFY_NAMESPACE_METADATA,
            TransactionVersion.MODIFY_NAMESPACE_METADATA,
            deadline,
            metadata_type,
            metadata_id,
            modifications,
            max_fee,
        )

    # CATBUFFER

    def catbuffer_size_specific(self) -> int:
        metadata_type_size = MetadataModificationType.CATBUFFER_SIZE
        metadata_id_size = util.U64_BYTES
        modifications_size = sum([x.catbuffer_size_specific() for x in self.modifications])
        return metadata_type_size + metadata_id_size + modifications_size

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export address alias-specific data to catbuffer."""

        # uint8_t metadata_type
        # metadata_id

        metadata_type = util.u8_to_catbuffer(self.metadata_type)
        metadata_id = util.u64_to_catbuffer(int(self.metadata_id))
        modifications = b''.join([x.to_catbuffer_specific(network_type) for x in self.modifications])

        return metadata_type + metadata_id + modifications

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load address alias-specific data data from catbuffer."""
        raise ValueError('Not implemented.')

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'metadataType', 'metadataId', 'modifications'}
        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        return {
            'metadataType': util.u8_to_dto(self.metadata_type),
            'metadataId': util.u8_to_dto(int(self.metadata_id)),
            'modifications': [MetadataModification.to_dto(x, network_type) for x in self.modifications],
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        metadata_type = MetadataType.create_from_dto(data['metadataType'], network_type)
        metadata_id = NamespaceId(util.u64_from_dto(data['metadataId']))
        modifications = [MetadataModification.create_from_dto(x, network_type) for x in data['modifications']]

        self._set('metadata_type', metadata_type)
        self._set('metadata_id', metadata_id)
        self._set('modifications', modifications)


@register_transaction('MODIFY_NAMESPACE_METADATA')
class ModifyNamespaceMetadataInnerTransaction(InnerTransaction, ModifyNamespaceMetadataTransaction):
    """Embedded namespace metadata modification transaction."""

    __slots__ = ()
