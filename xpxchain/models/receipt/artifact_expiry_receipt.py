"""
    artifact_expiry_receipt
    ====================

    Transfer transaction.

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

from ..blockchain.network_type import OptionalNetworkType
from .receipt_version import ReceiptVersion
from .receipt_type import ReceiptType
from .receipt import Receipt
from .registry import register_receipt
from ... import util

__all__ = [
    'ArtifactExpiryReceipt',
    'MosaicExpiredReceipt',
    'NamespaceExpiredReceipt',
]


@util.inherit_doc
@util.dataclass(frozen=True)
class ArtifactExpiryReceipt(Receipt):
    """
    Artifact Expiry Receipt.

    :param type: The type of the receipt.
    :param version: The version of the receipt.
    :param artifactId: Artifact in question.
    :param network_type: Network type.
    """

    artifact_id: int

    def __init__(
        self,
        type: ReceiptType,
        version: ReceiptVersion,
        artifact_id: int,
        network_type: OptionalNetworkType,
    ) -> None:
        super().__init__(
            type,
            version,
            network_type,
        )
        self._set('artifact_id', artifact_id)

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'artifactId'}
        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        network_type: OptionalNetworkType,
    ) -> dict:
        return {
            'artifactId': util.u64_to_dto(self.artifact_id),
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: OptionalNetworkType,
    ) -> None:
        artifact_id = util.u64_from_dto(data['artifactId'])

        self._set('artifact_id', artifact_id)


@util.inherit_doc
@register_receipt('MOSAIC_EXPIRED')
class MosaicExpiredReceipt(ArtifactExpiryReceipt):
    """
    Balance Change Receipt.

    :param network_type: Network type.
    :param version: The version of the receipt.
    :param account: The target account public key.
    :param mosaicId: Mosaic.
    :param amount: Amount to change.
    """

    @classmethod
    def create(
        cls,
        type: ReceiptType,
        version: ReceiptVersion,
        artifact_id: int,
        network_type: OptionalNetworkType,
    ) -> MosaicExpiredReceipt:
        return cls(
            type,
            version,
            artifact_id,
            network_type,
        )


@util.inherit_doc
@register_receipt('NAMESPACE_EXPIRED')
class NamespaceExpiredReceipt(ArtifactExpiryReceipt):
    """
    Balance Change Receipt.

    :param network_type: Network type.
    :param version: The version of the receipt.
    :param account: The target account public key.
    :param mosaicId: Mosaic.
    :param amount: Amount to change.
    """

    @classmethod
    def create(
        cls,
        type: ReceiptType,
        version: ReceiptVersion,
        artifact_id: int,
        network_type: OptionalNetworkType,
    ) -> NamespaceExpiredReceipt:
        return cls(
            type,
            version,
            artifact_id,
            network_type,
        )
