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

import struct
import typing

from nem2 import util
from .inner_transaction import InnerTransaction
from .plain_message import EMPTY_MESSAGE, PlainMessage
from .transaction import Transaction
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.address import Address
from ..mosaic.mosaic import Mosaic

if typing.TYPE_CHECKING:
    # We dynamically resolve the forward references which are used
    # in an auto-generate __init__ outside of the module.
    # Silence the lint warnings.
    from .deadline import Deadline
    from .message import Message
    from .transaction_info import TransactionInfo       # noqa
    from ..account.public_account import PublicAccount
    from ..blockchain.network_type import NetworkType


@util.inherit_doc
@util.dataclass(frozen=True)
class TransferTransaction(Transaction):
    """
    Transfer transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param fee: Fee for the transaction. Higher fees increase transaction priority.
    :param recipient: Address of recipient.
    :param mosaics: Sequence of mosaics.
    :param message: Transaction message (up to 2048 characters).
    :param signature: (Optional) Transaction signature (missing if aggregate transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    recipient: 'Address'
    mosaics: typing.Sequence['Mosaic']
    message: 'Message'

    def __init__(self,
        network_type: 'NetworkType',
        version: 'TransactionVersion',
        deadline: 'Deadline',
        fee: int,
        recipient: 'Address',
        mosaics: typing.Optional[typing.Sequence['Mosaic']] = None,
        message: 'Message' = EMPTY_MESSAGE,
        signature: typing.Optional[str] = None,
        signer: typing.Optional['PublicAccount'] = None,
        transaction_info: typing.Optional['TransactionInfo'] = None,
    ):
        super().__init__(
            TransactionType.TRANSFER,
            network_type,
            version,
            deadline,
            fee,
            signature,
            signer,
            transaction_info,
        )
        object.__setattr__(self, 'recipient', recipient)
        object.__setattr__(self, 'mosaics', mosaics or [])
        object.__setattr__(self, 'message', message)

    @classmethod
    def create(
        cls,
        deadline: 'Deadline',
        recipient: 'Address',
        mosaics: typing.Optional[typing.Sequence['Mosaic']],
        message: 'Message',
        network_type: 'NetworkType',
    ) -> 'TransferTransaction':
        """
        Create new transfer transaction.

        :param deadline: Deadline to include transaction.
        :param recipient: Address of recipient.
        :param mosaics: Sequence of mosaics.
        :param message: Transaction message (up to 2048 characters).
        :param network_type: Network type.
        """
        return TransferTransaction(
            network_type,
            TransactionVersion.TRANSFER,
            deadline,
            0,
            recipient,
            mosaics,
            message
        )

    def entity_size(self) -> int:
        # Extra 3 + address_size + message_size + $MOSAIC_SIZE * mosaics_count
        # 2 for message_size, and 1 for mosaics_count.
        recipient_size = Address.CATBUFFER_SIZE
        message_size = len(self.message.payload)
        mosaics_size = Mosaic.CATBUFFER_SIZE * len(self.mosaics)
        return recipient_size + message_size + mosaics_size + 3

    def to_catbuffer_specific(self) -> bytes:
        """Export transfer-specific data to catbuffer."""

        # uint8_t[25] recipient
        # uint16_t message_size
        # uint8_t mosaics_count
        # uint8_t[message_size] message
        # Mosaic[mosaics_count] mosaics
        recipient = self.recipient.to_catbuffer()
        message_size = struct.pack('<H', len(self.message.payload))
        mosaics_count = struct.pack('<B', len(self.mosaics))
        message = self.message.payload
        mosaics = b''.join(i.to_catbuffer() for i in self.mosaics)

        return recipient + message_size + mosaics_count + message + mosaics

    def load_catbuffer_specific(self, data: bytes) -> bytes:
        """Load transfer-specific data data from catbuffer."""

        # uint8_t[25] recipient
        # uint16_t message_size
        # uint8_t mosaics_count
        # uint8_t[message_size] message
        # Mosaic[mosaics_count] mosaics
        recipient, data = Address.from_catbuffer(data)
        message_size = struct.unpack('<H', data[:2])[0]
        mosaics_count = struct.unpack('<B', data[2:3])[0]
        message = PlainMessage(data[3: message_size + 3])
        mosaics = []
        data = data[message_size + 3:]
        for i in range(mosaics_count):
            mosaic, data = Mosaic.from_catbuffer(data)
            mosaics.append(mosaic)

        object.__setattr__(self, 'recipient', recipient)
        object.__setattr__(self, 'mosaics', mosaics)
        object.__setattr__(self, 'message', message)

        return data

    def to_aggregate(self, signer: 'PublicAccount') -> 'TransferInnerTransaction':
        """Convert transaction to inner transaction."""
        inst = TransferInnerTransaction.from_transaction(self, signer)
        return typing.cast(TransferInnerTransaction, inst)


class TransferInnerTransaction(InnerTransaction, TransferTransaction):
    """Embedded transfer transaction."""

    __slots__ = ()


Transaction.HOOKS[TransactionType.TRANSFER] = (
    TransferTransaction.from_catbuffer,
    TransferTransaction.from_dto,
)


InnerTransaction.HOOKS[TransactionType.TRANSFER] = (
    TransferInnerTransaction.from_catbuffer,
    TransferInnerTransaction.from_dto,
)
