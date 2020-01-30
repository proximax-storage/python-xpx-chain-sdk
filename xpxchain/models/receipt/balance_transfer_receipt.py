"""
    balance_transfer_receipt
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
    'BalanceTransferReceipt',
]


@util.inherit_doc
@util.dataclass(frozen=True)
@register_receipt('BALANCE_TRANSFER')
class BalanceTransferReceipt(Receipt):
    """
    Balance Transfer Receipt.

    :param network_type: Network type.
    :param version: The version of the receipt.    
    :param sender: The public key of the sender.
    :param recipient: The public key of the recipient.
    :param mosaicId: Mosaic.
    :param amount: Amount to change.
    """

    #account: PublicAccount
    sender: str
    recipient: str
    mosaic_id: int
    amount: int

    def __init__(
        self,
        #network_type: NetworkType,
        version: ReceiptVersion,
        sender: str,
        recipient: str,
        mosaic_id: int,
        amount: int
    ) -> None:
        super().__init__(
            ReceiptVersion.BALANCE_CHANGE,
            #network_type,
            version,
            sender,
            recipient,
            mosaic_id,
            amount
        )
        self._set('sender', sender)
        self._set('recipient', recipient)
        self._set('mosaic_id', mosaic_id)
        self._set('amount', amount)

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'sender', 'recipient', 'mosaicId', 'amount'}
        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        #network_type: NetworkType,
    ) -> dict:
        return {
            #'account': self.account.public_key,
            'sender': self.sender,
            'recipient': self.recipient,
            'mosaic': util.u64_to_dto(self.mosaic_id),
            'amount': util.u64_to_dto(self.amount),
        }

    def load_dto_specific(
        self,
        data: dict,
        #network_type: NetworkType,
    ) -> None:
        #account = PublicAccount.create_from_public_key(data['account'], network_type)
        sender = data['sender']
        recipient = data['recipient']
        mosaic_id = util.u64_from_dto(data['mosaicId'])
        amount = util.u64_from_dto(data['amount'])

        self._set('sender', sender)
        self._set('recipient', recipient)
        self._set('mosaic_id', mosaic_id)
        self._set('amount', amount)


