"""
    mosaic_alias_transaction
    ========================

    Mosaic alias transaction.

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
from ..mosaic.mosaic_id import MosaicId
from ..namespace.alias_action_type import AliasActionType
from ..namespace.namespace_id import NamespaceId
from ... import util

__all__ = ['MosaicAliasTransaction']


@util.inherit_doc
@util.dataclass(frozen=True)
@register_transaction('MOSAIC_ALIAS')
class MosaicAliasTransaction(Transaction):
    """
    Mosaic alias transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param action_type: Alias action type.
    :param namespace_id: Resulting namespace ID that will be an alias.
    :param mosaic_id: Mosaic to be aliased.
    :param signature: (Optional) Transaction signature (missing if embedded transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    action_type: AliasActionType
    namespace_id: NamespaceId
    mosaic_id: MosaicId

    def __init__(
        self,
        network_type: NetworkType,
        version: TransactionVersion,
        deadline: Deadline,
        action_type: AliasActionType,
        namespace_id: NamespaceId,
        mosaic_id: MosaicId,
        max_fee: int = 0,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None,
    ) -> None:
        super().__init__(
            TransactionType.MOSAIC_ALIAS,
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
        self._set('mosaic_id', mosaic_id)

    @classmethod
    def create(
        cls,
        deadline: Deadline,
        action_type: AliasActionType,
        namespace_id: NamespaceId,
        mosaic_id: MosaicId,
        network_type: NetworkType,
        max_fee: int = 0,
    ):
        """
        Create new mosaic alias transaction.

        :param deadline: Deadline to include transaction.
        :param action_type: Alias action type.
        :param namespace_id: Resulting namespace ID that will be an alias.
        :param mosaic_id: Mosaic to be aliased.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """
        return cls(
            network_type,
            TransactionVersion.MOSAIC_ALIAS,
            deadline,
            action_type,
            namespace_id,
            mosaic_id,
            max_fee,
        )

    # CATBUFFER

    def catbuffer_size_specific(self) -> int:
        action_type_size = AliasActionType.CATBUFFER_SIZE
        namespace_id_size = util.U64_BYTES
        mosaic_id_size = util.U64_BYTES
        return action_type_size + namespace_id_size + mosaic_id_size

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export mosaic alias-specific data to catbuffer."""

        # uint8_t action_type
        # uint64_t namespace_id
        # uint64_t mosaic_id
        action_type = self.action_type.to_catbuffer(network_type)
        namespace_id = util.u64_to_catbuffer(int(self.namespace_id))
        mosaic_id = util.u64_to_catbuffer(int(self.mosaic_id))

        return action_type + namespace_id + mosaic_id

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load mosaic alias-specific data data from catbuffer."""

        # uint8_t action_type
        # uint64_t namespace_id
        # uint64_t mosaic_id
        action_type = AliasActionType.create_from_catbuffer(data, network_type)
        namespace_id = NamespaceId(util.u64_from_catbuffer(data[1:9]))
        mosaic_id = MosaicId(util.u64_from_catbuffer(data[9:17]))
        data = data[17:]

        self._set('action_type', action_type)
        self._set('namespace_id', namespace_id)
        self._set('mosaic_id', mosaic_id)

        return data

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'aliasAction', 'namespaceId', 'mosaicId'}
        return (
            cls.validate_dto_required(data, required_keys)
        )

    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        return {
            'aliasAction': self.action_type.to_dto(network_type),
            'namespaceId': util.u64_to_dto(int(self.namespace_id)),
            'mosaicId': util.u64_to_dto(int(self.mosaic_id)),
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        action_type = AliasActionType.create_from_dto(data['aliasAction'], network_type)
        namespace_id = NamespaceId(util.u64_from_dto(data['namespaceId']))
        mosaic_id = MosaicId(util.u64_from_dto(data['mosaicId']))

        self._set('action_type', action_type)
        self._set('namespace_id', namespace_id)
        self._set('mosaic_id', mosaic_id)


@register_transaction('MOSAIC_ALIAS')
class MosaicAliasInnerTransaction(InnerTransaction, MosaicAliasTransaction):
    """Embedded mosaic alias transaction."""

    __slots__ = ()
