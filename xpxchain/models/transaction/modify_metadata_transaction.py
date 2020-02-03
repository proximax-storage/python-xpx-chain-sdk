"""
    modify_metadata_transaction
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
from .modify_account_metadata_transaction import (
    ModifyAccountMetadataTransaction
)
from .transaction import TransactionBase
from ..metadata.metadata_type import MetadataType
from ..metadata.metadata_modification import MetadataModification
from .recipient import RecipientType
from ..blockchain.network_type import NetworkType

__all__ = ['ModifyMetadataTransaction']

MetadataModificationList = typing.Sequence[MetadataModification]


class ModifyMetadataTransaction(TransactionBase):
    """Abstract class for account property modification transactions."""

    __slots__ = ()

    @staticmethod
    def create_modify_account_metadata_transaction(
        deadline: Deadline,
        metadata_type: MetadataType,
        metadata_id: RecipientType,
        modifications: MetadataModificationList,
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

        return ModifyAccountMetadataTransaction.create(
            deadline,
            metadata_type,
            metadata_id,
            modifications,
            network_type,
            max_fee,
        )
