"""
    balance_change_receipt
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
    'BalanceChangeReceipt',
    'BalanceChangeCreditReceipt',
    'BalanceChangeDebitReceipt',
    'ValidateFeeReceipt',
    'LockHashCreatedReceipt',
    'LockHashCompletedReceipt',
    'LockHashExpiredReceipt',
    'LockSecretCreatedReceipt',
    'LockSecretCompletedReceipt',
    'LockSecretExpiredReceipt',
]


@util.inherit_doc
@util.dataclass(frozen=True)
class BalanceChangeReceipt(Receipt):
    """
    Balance Change Receipt.

    :param network_type: Network type.
    :param version: The version of the receipt.
    :param account: The target account public key.
    :param mosaicId: Mosaic.
    :param amount: Amount to change.
    """

    account: PublicAccount
    mosaic: Mosaic

    def __init__(
        self,
        type: ReceiptType,
        version: ReceiptVersion,
        account: PublicAccount,
        mosaic: Mosaic,
        network_type: OptionalNetworkType,
    ) -> None:
        super().__init__(
            type,
            version,
            network_type,
        )
        self._set('account', account)
        self._set('mosaic', mosaic)
    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'account', 'mosaicId', 'amount'}
        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        network_type: OptionalNetworkType,
    ) -> dict:
        mosaic_data = self.mosaic.to_dto(network_type)

        return {
            'account': self.account.public_key,
            'mosaicId': mosaic_data['id'],
            'amount': mosaic_data['amount'],
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: OptionalNetworkType,
    ) -> None:
        account = PublicAccount.create_from_public_key(data['account'], network_type)
        mosaic = Mosaic.create_from_dto({'id': data['mosaicId'], 'amount': data['amount']})

        self._set('account', account)
        self._set('mosaic', mosaic)


@util.inherit_doc
class BalanceChangeCreditReceipt(BalanceChangeReceipt):
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
        account: PublicAccount,
        mosaic: Mosaic,
        network_type: OptionalNetworkType,
    ) -> BalanceChangeCreditReceipt:
        return cls(
            type,
            version,
            account,
            mosaic,
            network_type
        )


@util.inherit_doc
class BalanceChangeDebitReceipt(BalanceChangeReceipt):
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
        account: PublicAccount,
        mosaic: Mosaic,
        network_type: OptionalNetworkType,
    ) -> BalanceChangeDebitReceipt:
        return cls(
            type,
            version,
            account,
            mosaic,
            network_type
        )


@util.inherit_doc
@register_receipt('VALIDATE_FEE')
class ValidateFeeReceipt(BalanceChangeCreditReceipt):
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
        account: PublicAccount,
        mosaic: Mosaic,
        network_type: OptionalNetworkType,
    ) -> ValidateFeeReceipt:
        return cls(
            type,
            version,
            account,
            mosaic,
            network_type
        )


@util.inherit_doc
@register_receipt('LOCKHASH_CREATED')
class LockHashCreatedReceipt(BalanceChangeDebitReceipt):
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
        account: PublicAccount,
        mosaic: Mosaic,
        network_type: OptionalNetworkType,
    ) -> LockHashCreatedReceipt:
        return cls(
            type,
            version,
            account,
            mosaic,
            network_type
        )


@util.inherit_doc
@register_receipt('LOCKHASH_COMPLETED')
class LockHashCompletedReceipt(BalanceChangeCreditReceipt):
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
        account: PublicAccount,
        mosaic: Mosaic,
        network_type: OptionalNetworkType,
    ) -> LockHashCompletedReceipt:
        return cls(
            type,
            version,
            account,
            mosaic,
            network_type
        )


@util.inherit_doc
@register_receipt('LOCKHASH_EXPIRED')
class LockHashExpiredReceipt(BalanceChangeCreditReceipt):
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
        account: PublicAccount,
        mosaic: Mosaic,
        network_type: OptionalNetworkType,
    ) -> LockHashExpiredReceipt:
        return cls(
            type,
            version,
            account,
            mosaic,
            network_type
        )


@util.inherit_doc
@register_receipt('LOCKSECRET_CREATED')
class LockSecretCreatedReceipt(BalanceChangeDebitReceipt):
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
        account: PublicAccount,
        mosaic: Mosaic,
        network_type: OptionalNetworkType,
    ) -> LockSecretCreatedReceipt:
        return cls(
            type,
            version,
            account,
            mosaic,
            network_type
        )


@util.inherit_doc
@register_receipt('LOCKSECRET_COMPLETED')
class LockSecretCompletedReceipt(BalanceChangeCreditReceipt):
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
        account: PublicAccount,
        mosaic: Mosaic,
        network_type: OptionalNetworkType,
    ) -> LockSecretCompletedReceipt:
        return cls(
            type,
            version,
            account,
            mosaic,
            network_type
        )


@util.inherit_doc
@register_receipt('LOCKSECRET_EXPIRED')
class LockSecretExpiredReceipt(BalanceChangeCreditReceipt):
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
        account: PublicAccount,
        mosaic: Mosaic,
        network_type: OptionalNetworkType,
    ) -> LockSecretExpiredReceipt:
        return cls(
            type,
            version,
            account,
            mosaic,
            network_type
        )
