"""
    transfer_transaction
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

from .deadline import Deadline
from .inner_transaction import InnerTransaction
from .message import Message
from .plain_message import EMPTY_MESSAGE, PlainMessage
from .recipient import Recipient, RecipientType
from .registry import register_transaction
from .transaction import Transaction
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ..mosaic.mosaic import Mosaic, MosaicList
from ... import util

__all__ = [
    'TransferTransaction',
    'TransferInnerTransaction',
]


@util.inherit_doc
@util.dataclass(frozen=True)
@register_transaction('TRANSFER')
class TransferTransaction(Transaction):
    """
    Transfer transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param recipient: Address or namespace ID alias of recipient.
    :param mosaics: Sequence of mosaics.
    :param message: Transaction message (up to 2048 characters).
    :param signature: (Optional) Transaction signature (missing if embedded transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    recipient: RecipientType
    mosaics: MosaicList
    message: Message

    def __init__(
        self,
        network_type: NetworkType,
        version: TransactionVersion,
        deadline: Deadline,
        recipient: RecipientType,
        max_fee: int = 0,
        mosaics: typing.Optional[MosaicList] = None,
        message: Message = EMPTY_MESSAGE,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None
    ) -> None:
        super().__init__(
            TransactionType.TRANSFER,
            network_type,
            version,
            deadline,
            max_fee,
            signature,
            signer,
            transaction_info
        )
        self._set('recipient', recipient)
        self._set('mosaics', mosaics or [])
        self._set('message', message)

    @classmethod
    def create(
        cls,
        deadline: Deadline,
        recipient: RecipientType,
        network_type: NetworkType,
        mosaics: typing.Optional[MosaicList] = None,
        message: Message = EMPTY_MESSAGE,
        max_fee: int = 0,
    ):
        """
        Create new transfer transaction.

        :param deadline: Deadline to include transaction.
        :param recipient: Address or namespace ID alias of recipient.
        :param mosaics: Sequence of mosaics.
        :param message: Transaction message (up to 2048 characters).
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """
        return cls(
            network_type,
            TransactionVersion.TRANSFER,
            deadline,
            recipient,
            max_fee,
            mosaics,
            message
        )

    # CATBUFFER

    def catbuffer_size_specific(self) -> int:
        # Extra 3 + address_size + message_size + $MOSAIC_SIZE * mosaics_count
        # 2 for message_size, and 1 for mosaics_count.
        extra_size = util.U8_BYTES + util.U16_BYTES
        recipient_size = Recipient.CATBUFFER_SIZE
        message_size = self.message.catbuffer_size_specific()
        mosaics_size = Mosaic.CATBUFFER_SIZE * len(self.mosaics)
        return extra_size + recipient_size + message_size + mosaics_size

    def to_mosaics_bytes(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Get the serialized byte array of all mosaics."""

        return util.Model.sequence_to_catbuffer(
            self.mosaics,
            network_type
        )

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export transfer-specific data to catbuffer."""

        # uint8_t[25] recipient
        # uint16_t message_size
        # uint8_t mosaics_count
        # uint8_t message type
        # uint8_t[message_size] message
        # Mosaic[mosaics_count] mosaics
        recipient = Recipient.to_catbuffer(self.recipient, network_type)
        message_size = util.u16_to_catbuffer(self.message.catbuffer_size_specific())
        mosaics_count = util.u8_to_catbuffer(len(self.mosaics))
        message = self.message.to_catbuffer(network_type)
        mosaics = self.to_mosaics_bytes(network_type)

        return recipient + message_size + mosaics_count + message + mosaics

    def load_mosaics_bytes(
        self,
        data: bytes,
        count: int,
        network_type: NetworkType,
    ) -> bytes:
        """Load mosaics data from catbuffer."""

        mosaics, data = Mosaic.sequence_from_catbuffer_pair(data, count, network_type)
        self._set('mosaics', mosaics)
        return data

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load transfer-specific data from catbuffer."""

        # uint8_t[25] recipient
        # uint16_t message_size
        # uint8_t mosaics_count
        # uint8_t[message_size] message
        # Mosaic[mosaics_count] mosaics
        recipient, data = Recipient.create_from_catbuffer_pair(data, network_type)
        message_size = util.u16_from_catbuffer(data[:util.U16_BYTES])
        data = data[util.U16_BYTES:]
        mosaics_count = util.u8_from_catbuffer(data[:util.U8_BYTES])
        data = data[util.U8_BYTES:]
        message = PlainMessage(data[1:message_size])
        data = data[message_size:]
        data = self.load_mosaics_bytes(data, mosaics_count, network_type)

        self._set('recipient', recipient)
        self._set('message', message)

        return data

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'recipient'}
        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        return {
            'recipient': Recipient.to_dto(self.recipient, network_type),
            'mosaics': Mosaic.sequence_to_dto(self.mosaics, network_type),
            'message': self.message.to_dto(network_type),
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        recipient = Recipient.create_from_dto(data['recipient'], network_type)
        mosaics = Mosaic.sequence_from_dto(data.get('mosaics', []), network_type)
        message = EMPTY_MESSAGE
        if 'message' in data:
            message = PlainMessage.create_from_dto(data['message'], network_type)

        self._set('recipient', recipient)
        self._set('mosaics', mosaics)
        self._set('message', message)


@register_transaction('TRANSFER')
class TransferInnerTransaction(InnerTransaction, TransferTransaction):
    """Embedded transfer transaction."""

    __slots__ = ()
