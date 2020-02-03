"""
    transaction_statement
    =================

    Describes a transaction statement.

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
from ..blockchain.network_type import OptionalNetworkType
from .balance_change_receipt import BalanceChangeReceipt
from .balance_transfer_receipt import BalanceTransferReceipt
from .artifact_expiry_receipt import ArtifactExpiryReceipt
from .inflation_receipt import InflationReceipt
from .receipt import Receipt
from .source import Source
from ... import util


__all__ = ['TransactionStatement']

ReceiptValue = typing.Union[
    BalanceChangeReceipt,
    BalanceTransferReceipt,
    ArtifactExpiryReceipt,
    InflationReceipt,
]
ReceiptValueList = typing.Sequence[ReceiptValue]


@util.inherit_doc
@util.dataclass(frozen=True)
class TransactionStatement(util.DTO):
    """
    Transaction statement information.

    :param height:
    :param source:
    :param receipts: The array of receipts.

    DTO Format:
        .. code-block:: yaml

            TransactionStatementsDTO:
                height: UInt64DTO
                source: SourceDTO
                receipts: anyOf(
                    BalanceTransferReceiptDTO,
                    BalanceChangeReceiptDTO,
                    ArtifactExpiryReceiptDTO,
                    InflationReceiptDTO
                )[]
    """

    height: int
    source: Source
    receipts: typing.Sequence[Receipt]

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'height', 'source', 'receipts'}
        return (
            # Level 1
            cls.validate_dto_required(data, required_l1)
            and cls.validate_dto_all(data, required_l1)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'height': util.u64_to_dto(self.height),
            'source': self.source.to_dto(network_type),
            'receipts': [i.to_dto(network_type) for i in self.receipts]
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        return cls(
            height=util.u64_from_dto(data['height']),
            source=Source.create_from_dto(data['source'], network_type),
            receipts=[Receipt.create_from_dto(i, network_type) for i in data['receipts']]
        )
