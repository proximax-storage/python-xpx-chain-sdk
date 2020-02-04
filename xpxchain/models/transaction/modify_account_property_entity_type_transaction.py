"""
    modify_account_property_entity_type_transaction
    ===============================================

    Transaction to modify account property entity types.

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

from .account_property_modification import AccountPropertyModification
from .deadline import Deadline
from .inner_transaction import InnerTransaction
from .registry import register_transaction
from .transaction import Transaction
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.property_modification_type import PropertyModificationType
from ..account.property_type import PropertyType
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ... import util

__all__ = [
    'ModifyAccountPropertyEntityTypeTransaction',
    'ModifyAccountPropertyEntityTypeInnerTransaction',
]

AccountPropertyModificationList = typing.Sequence[AccountPropertyModification]
PROPERTY_TYPES = (
    PropertyType.ALLOW_TRANSACTION,
    PropertyType.BLOCK_TRANSACTION
)


def to_catbuffer(modification: AccountPropertyModification) -> bytes:
    """Serialize account property mosaic modification to catbuffer."""

    # uint8_t modification_type
    # uint16_t value
    type = modification.modification_type.to_catbuffer()
    value = util.u16_to_catbuffer(int(typing.cast(TransactionType, modification.value)))
    return type + value


def from_catbuffer(data: bytes) -> AccountPropertyModification:
    """Deserialize account property mosaic modification from catbuffer."""

    # uint8_t modification_type
    # uint16_t value
    modification_type = PropertyModificationType.create_from_catbuffer(data[:1])
    value = TransactionType(util.u16_from_catbuffer(data[1:3]))
    return AccountPropertyModification(modification_type, value)


@util.inherit_doc
@util.dataclass(frozen=True)
@register_transaction('MODIFY_ACCOUNT_PROPERTY_ENTITY_TYPE')
class ModifyAccountPropertyEntityTypeTransaction(Transaction):
    """
    Modify account property entity types transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param property_type: Account property type.
    :param modifications: List of account modifications.
    :param signature: (Optional) Transaction signature (missing if embedded transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    property_type: PropertyType
    modifications: AccountPropertyModificationList

    def __init__(
        self,
        network_type: NetworkType,
        version: TransactionVersion,
        deadline: Deadline,
        property_type: PropertyType,
        modifications: AccountPropertyModificationList,
        max_fee: int = 0,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None,
    ) -> None:
        if property_type not in PROPERTY_TYPES:
            raise ValueError('Property type must be a mosaic type.')
        if not all(i.is_entity_type() for i in modifications):
            raise ValueError('Modify account property entity types got invalid value.')
        super().__init__(
            TransactionType.MODIFY_ACCOUNT_PROPERTY_ENTITY_TYPE,
            network_type,
            version,
            deadline,
            max_fee,
            signature,
            signer,
            transaction_info,
        )
        self._set('property_type', property_type)
        self._set('modifications', modifications)

    @classmethod
    def create(
        cls,
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
        return cls(
            network_type,
            TransactionVersion.MODIFY_ACCOUNT_PROPERTY_ENTITY_TYPE,
            deadline,
            property_type,
            modifications,
            max_fee,
        )

    # CATBUFFER

    def catbuffer_size_specific(self) -> int:
        property_type_size = PropertyType.CATBUFFER_SIZE
        count_size = util.U8_BYTES
        modification_size = util.U8_BYTES + util.U16_BYTES
        modifications_size = modification_size * len(self.modifications)
        return property_type_size + count_size + modifications_size

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export modify account entity types-specific data to catbuffer."""

        # uint8_t property_type
        # uint8_t modifications_count
        # typedef Modification { type: uint8_t, value: uint16_t }
        # Modification[modifications_count] modifications
        property_type = self.property_type.to_catbuffer(network_type)
        modifications_count = util.u8_to_catbuffer(len(self.modifications))
        modifications = b''.join(map(to_catbuffer, self.modifications))
        return property_type + modifications_count + modifications

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load modify account entity types-specific data data from catbuffer."""

        # uint8_t property_type
        # uint8_t modifications_count
        # typedef Modification { type: uint8_t, value: uint16_t }
        # Modification[modifications_count] modifications
        property_type = PropertyType.create_from_catbuffer(data[:1], network_type)
        modifications_count = util.u8_from_catbuffer(data[1:2])
        data = data[2:]
        modifications = []
        for _ in range(modifications_count):
            modifications.append(from_catbuffer(data))
            data = data[3:]

        self._set('property_type', property_type)
        self._set('modifications', modifications)

        return data

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'propertyType', 'modifications'}
        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        to_dto = AccountPropertyModification.sequence_to_dto
        return {
            'propertyType': self.property_type.to_dto(network_type),
            'modifications': to_dto(self.modifications, network_type),
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        from_dto = AccountPropertyModification.sequence_from_dto
        property_type = PropertyType.create_from_dto(data['propertyType'])
        modifications = from_dto(data['modifications'])
        self._set('property_type', property_type)
        self._set('modifications', modifications)


@register_transaction('MODIFY_ACCOUNT_PROPERTY_ENTITY_TYPE')
class ModifyAccountPropertyEntityTypeInnerTransaction(
    InnerTransaction,
    ModifyAccountPropertyEntityTypeTransaction
):
    """Embedded modify account entity types transaction."""

    __slots__ = ()
