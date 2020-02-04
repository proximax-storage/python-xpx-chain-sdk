"""
    inflation_receipt
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
from ..mosaic.mosaic import Mosaic
from .receipt import Receipt
from .registry import register_receipt
from ... import util

__all__ = [
    'InflationReceipt',
]


@util.inherit_doc
@util.dataclass(frozen=True)
@register_receipt('INFLATION')
class InflationReceipt(Receipt):
    """
    Native currency mosaics were created due to inflation..

    :param network_type: Network type.
    :param version: The version of the receipt.
    :param mosaicId: Mosaic.
    :param amount: Amount to change.
    """

    mosaic: Mosaic

    def __init__(
        self,
        type: ReceiptType,
        version: ReceiptVersion,
        mosaic: Mosaic,
        network_type: OptionalNetworkType,
    ) -> None:
        super().__init__(
            type,
            version,
            network_type,
        )
        self._set('mosaic', mosaic)

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'mosaicId', 'amount'}
        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        network_type: OptionalNetworkType,
    ) -> dict:
        mosaic_data = self.mosaic.to_dto(network_type)

        return {
            'mosaicId': mosaic_data['id'],
            'amount': mosaic_data['amount'],
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: OptionalNetworkType,
    ) -> None:
        mosaic = Mosaic.create_from_dto({'id': data['mosaicId'], 'amount': data['amount']})

        self._set('mosaic', mosaic)
