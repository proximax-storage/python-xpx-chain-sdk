"""
    mosaic_definition_transaction
    =============================

    Mosaic-definition transaction.

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
from ..mosaic.mosaic_nonce import MosaicNonce
from ..mosaic.mosaic_properties import MosaicProperties
from ... import util

__all__ = [
    'MosaicDefinitionTransaction',
    'MosaicDefinitionInnerTransaction',
]


@util.inherit_doc
@util.dataclass(frozen=True)
@register_transaction('MOSAIC_DEFINITION')
class MosaicDefinitionTransaction(Transaction):
    """
    Mosaic-definition transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param nonce: Mosaic nonce (random data for mosaic uniqueness).
    :param mosaic_id: Identifier for mosaic.
    :param mosaic_properties: Mosaic properties.
    :param signature: (Optional) Transaction signature (missing if embedded transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    nonce: MosaicNonce
    mosaic_id: MosaicId
    mosaic_properties: MosaicProperties

    def __init__(
        self,
        network_type: NetworkType,
        version: TransactionVersion,
        deadline: Deadline,
        max_fee: int,
        nonce: MosaicNonce,
        mosaic_id: MosaicId,
        mosaic_properties: MosaicProperties,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None,
    ) -> None:
        super().__init__(
            TransactionType.MOSAIC_DEFINITION,
            network_type,
            version,
            deadline,
            max_fee,
            signature,
            signer,
            transaction_info,
        )
        self._set('nonce', nonce)
        self._set('mosaic_id', mosaic_id)
        self._set('mosaic_properties', mosaic_properties)

    @classmethod
    def create(
        cls,
        deadline: Deadline,
        nonce: MosaicNonce,
        mosaic_id: MosaicId,
        mosaic_properties: MosaicProperties,
        network_type: NetworkType,
        max_fee: int = 0,
    ):
        """
        Create new mosaic definition transaction.

        :param deadline: Deadline to include transaction.
        :param nonce: Mosaic nonce (random data for mosaic uniqueness).
        :param mosaic_id: Identifier for mosaic.
        :param mosaic_properties: Mosaic properties.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """
        return cls(
            network_type,
            TransactionVersion.MOSAIC_DEFINITION,
            deadline,
            max_fee,
            nonce,
            mosaic_id,
            mosaic_properties,
        )

    # CATBUFFER

    def catbuffer_size_specific(self) -> int:
        nonce_size = MosaicNonce.CATBUFFER_SIZE
        id_size = MosaicId.CATBUFFER_SIZE
        properties_size = self.mosaic_properties.catbuffer_size()
        return nonce_size + id_size + properties_size

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export mosaic definition-specific data to catbuffer."""

        # MosaicNonce nonce
        # MosaicId mosaic_id
        # MosaicProperties properties
        nonce = self.nonce.to_catbuffer(network_type)
        mosaic_id = self.mosaic_id.to_catbuffer(network_type)
        properties = self.mosaic_properties.to_catbuffer(network_type)
        return nonce + mosaic_id + properties

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load mosaic definition-specific data data from catbuffer."""

        # MosaicNonce nonce
        # MosaicId mosaic_id
        # MosaicProperties properties
        nonce, data = MosaicNonce.from_catbuffer_pair(data, network_type)
        mosaic_id, data = MosaicId.from_catbuffer_pair(data, network_type)
        properties, data = MosaicProperties.from_catbuffer_pair(data, network_type)

        self._set('nonce', nonce)
        self._set('mosaic_id', mosaic_id)
        self._set('mosaic_properties', properties)

        return typing.cast(bytes, data)

    # DTO

    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        return {
            'mosaicNonce': self.nonce.to_dto(network_type),
            'mosaicId': self.mosaic_id.to_dto(network_type),
            'properties': self.mosaic_properties.to_dto_v2(network_type),
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        nonce = MosaicNonce.from_dto(data['mosaicNonce'], network_type)
        mosaic_id = MosaicId.from_dto(data['mosaicId'], network_type)
        properties = MosaicProperties.from_dto_v2(data['properties'], network_type)
        self._set('nonce', nonce)
        self._set('mosaic_id', mosaic_id)
        self._set('mosaic_properties', properties)


@register_transaction('MOSAIC_DEFINITION')
class MosaicDefinitionInnerTransaction(InnerTransaction, MosaicDefinitionTransaction):
    """Embedded mosaic definition transaction."""

    __slots__ = ()
