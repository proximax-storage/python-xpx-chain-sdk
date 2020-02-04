"""
    modify_account_property_transaction
    ===================================

    Abstract class for modification to account property transactions.

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
from .modify_account_property_address_transaction import (
    ModifyAccountPropertyAddressTransaction
)
from .modify_account_property_entity_type_transaction import (
    ModifyAccountPropertyEntityTypeTransaction
)
from .modify_account_property_mosaic_transaction import (
    ModifyAccountPropertyMosaicTransaction
)
from .account_property_modification import AccountPropertyModification
from .transaction import TransactionBase
from .transaction_type import TransactionType
from ..account.address import Address
from ..account.property_modification_type import PropertyModificationType
from ..account.property_type import PropertyType
from ..blockchain.network_type import NetworkType
from ..mosaic.mosaic_id import MosaicId

__all__ = ['AccountPropertyTransaction']

AccountPropertyModificationList = typing.Sequence[AccountPropertyModification]


class AccountPropertyTransaction(TransactionBase):
    """Abstract class for account property modification transactions."""

    __slots__ = ()

    @staticmethod
    def create_address_property_modification_transaction(
        deadline: Deadline,
        property_type: PropertyType,
        modifications: AccountPropertyModificationList,
        network_type: NetworkType,
        max_fee: int = 0,
    ):
        """
        Create new modify account addresses transaction.

        :param deadline: Deadline to include transaction.
        :param property_type: Account property type.
        :param modifications: List of account modifications.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """

        return ModifyAccountPropertyAddressTransaction.create(
            deadline,
            property_type,
            modifications,
            network_type,
            max_fee,
        )

    @staticmethod
    def create_mosaic_property_modification_transaction(
        deadline: Deadline,
        property_type: PropertyType,
        modifications: AccountPropertyModificationList,
        network_type: NetworkType,
        max_fee: int = 0,
    ):
        """
        Create new modify account mosaics transaction.

        :param deadline: Deadline to include transaction.
        :param property_type: Account property type.
        :param modifications: List of account modifications.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """

        return ModifyAccountPropertyMosaicTransaction.create(
            deadline,
            property_type,
            modifications,
            network_type,
            max_fee,
        )

    @staticmethod
    def create_entity_type_property_modification_transaction(
        deadline: Deadline,
        property_type: PropertyType,
        modifications: AccountPropertyModificationList,
        network_type: NetworkType,
        max_fee: int = 0,
    ):
        """
        Create new modify account entity types transaction.

        :param deadline: Deadline to include transaction.
        :param property_type: Account property type.
        :param modifications: List of account modifications.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """

        return ModifyAccountPropertyEntityTypeTransaction.create(
            deadline,
            property_type,
            modifications,
            network_type,
            max_fee,
        )

    @staticmethod
    def create_address_filter(
        modification_type: PropertyModificationType,
        address: Address,
    ) -> AccountPropertyModification:
        """
        Create address filter for account property modification.

        :param modification_type: Add or remove modification.
        :param address: Address value for modification.
        """
        return AccountPropertyModification(modification_type, address)

    @staticmethod
    def create_mosaic_filter(
        modification_type: PropertyModificationType,
        mosaic_id: MosaicId,
    ) -> AccountPropertyModification:
        """
        Create mosaic filter for account property modification.

        :param modification_type: Add or remove modification.
        :param mosaic_id: Mosaic ID value for modification.
        """
        return AccountPropertyModification(modification_type, mosaic_id)

    @staticmethod
    def create_entity_type_filter(
        modification_type: PropertyModificationType,
        entity_type: TransactionType,
    ) -> AccountPropertyModification:
        """
        Create entity type filter for account property modification.

        :param modification_type: Add or remove modification.
        :param entity_type: Transaction type value for modification.
        """
        return AccountPropertyModification(modification_type, entity_type)
