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
import typing

from ..blockchain.network_type import OptionalNetworkType, NetworkType
from ..account.public_account import PublicAccount
from .receipt_version import ReceiptVersion
from .receipt import Receipt
from .registry import register_receipt
from ... import util

__all__ = [
    'ArtifactExpiryReceipt',
]


@util.inherit_doc
@util.dataclass(frozen=True)
@register_receipt('ARTIFACT_EXPIRY')
class ArtifactExpiryReceipt(Receipt):
    """
    Balance Change Receipt.

    :param network_type: Network type.
    :param version: The version of the receipt.    
    :param artifactId: Artifact in question.
    """

    #account: PublicAccount
    artifact_id: int

    def __init__(
        self,
        #network_type: NetworkType,
        version: ReceiptVersion,
        artifact_id: int,
    ) -> None:
        super().__init__(
            ReceiptVersion.BALANCE_CHANGE,
            #network_type,
            version,
            artifact_id,
        )
        self._set('artifact_id', artifact_id)

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'artifactId'}
        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        #network_type: NetworkType,
    ) -> dict:
        return {
            'artifactId': util.u64_to_dto(self.artifact_id),
        }

    def load_dto_specific(
        self,
        data: dict,
        #network_type: NetworkType,
    ) -> None:
        artifact_id = util.u64_from_dto(data['artifactId'])

        self._set('artifact_id', artifact_id)


