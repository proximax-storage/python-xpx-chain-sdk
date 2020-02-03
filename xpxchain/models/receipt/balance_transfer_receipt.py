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

from ..blockchain.network_type import OptionalNetworkType
from ..account.public_account import PublicAccount
from ..mosaic.mosaic import Mosaic
from .receipt_version import ReceiptVersion
from .receipt_type import ReceiptType
from .receipt import Receipt
from .registry import register_receipt
from ... import util

__all__ = [
    'BalanceTransferReceipt',
    'MosaicLevyReceipt',
    'MosaicRentalFeeReceipt',
    'NamespaceRentalFeeReceipt',
]


@util.inherit_doc
@util.dataclass(frozen=True)
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

    sender: PublicAccount
    recipient: PublicAccount
    mosaic: Mosaic

    def __init__(
        self,
        type: ReceiptType,
        version: ReceiptVersion,
        sender: PublicAccount,
        recipient: PublicAccount,
        mosaic: Mosaic,
        network_type: OptionalNetworkType,
    ) -> None:
        super().__init__(
            type,
            version,
            network_type,
        )
        self._set('sender', sender)
        self._set('recipient', recipient)
        self._set('mosaic', mosaic)

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'sender', 'recipient', 'mosaicId', 'amount'}
        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        network_type: OptionalNetworkType,
    ) -> dict:
        mosaic_data = self.mosaic.to_dto(network_type)

        return {
            'sender': self.sender.public_key,
            'recipient': self.recipient.public_key,
            'mosaicId': mosaic_data['id'],
            'amount': mosaic_data['amount'],

        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: OptionalNetworkType,
    ) -> None:
        sender = PublicAccount.create_from_public_key(data['sender'], network_type)
        recipient = PublicAccount.create_from_public_key(data['recipient'], network_type)
        mosaic = Mosaic.create_from_dto({'id': data['mosaicId'], 'amount': data['amount']})

        self._set('sender', sender)
        self._set('recipient', recipient)
        self._set('mosaic', mosaic)


@util.inherit_doc
@register_receipt('MOSAIC_LEVY')
class MosaicLevyReceipt(BalanceTransferReceipt):
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
        sender: PublicAccount,
        recipient: PublicAccount,
        mosaic: Mosaic,
        network_type: OptionalNetworkType,
    ) -> MosaicLevyReceipt:
        return cls(
            type,
            version,
            sender,
            recipient,
            mosaic,
            network_type,
        )


@util.inherit_doc
@register_receipt('MOSAIC_RENTAL_FEE')
class MosaicRentalFeeReceipt(BalanceTransferReceipt):
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
        sender: PublicAccount,
        recipient: PublicAccount,
        mosaic: Mosaic,
        network_type: OptionalNetworkType,
    ) -> MosaicRentalFeeReceipt:
        return cls(
            type,
            version,
            sender,
            recipient,
            mosaic,
            network_type,
        )


@util.inherit_doc
@register_receipt('NAMESPACE_RENTAL_FEE')
class NamespaceRentalFeeReceipt(BalanceTransferReceipt):
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
        sender: PublicAccount,
        recipient: PublicAccount,
        mosaic: Mosaic,
        network_type: OptionalNetworkType,
    ) -> NamespaceRentalFeeReceipt:
        return cls(
            type,
            version,
            sender,
            recipient,
            mosaic,
            network_type,
        )
