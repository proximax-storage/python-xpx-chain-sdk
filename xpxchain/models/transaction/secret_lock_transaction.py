"""
    secret_lock_transaction
    ========================

    Secret-lock transaction, which locks a given mosaic.

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
from .hash_type import HashType
from .inner_transaction import InnerTransaction
from .recipient import Recipient, RecipientType
from .registry import register_transaction
from .transaction import Transaction
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ..mosaic.mosaic import Mosaic
from ..mosaic.mosaic_id import MosaicId
from ... import util

__all__ = [
    'SecretLockTransaction',
    'SecretLockInnerTransaction',
]


@util.inherit_doc
@util.dataclass(frozen=True)
@register_transaction('SECRET_LOCK')
class SecretLockTransaction(Transaction):
    """
    Secret-proof transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param mosaic: Mosaic to be locked.
    :param duration: Duration for funds to be released or returned.
    :param hash_type: Hash algorithm secret was generated with.
    :param secret: Hex-encoded or raw seed-proof hash.
    :param recipient: Recipient of funds.
    :param signature: (Optional) Transaction signature (missing if embedded transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    mosaic: Mosaic
    duration: int
    hash_type: HashType
    secret: str
    recipient: RecipientType

    def __init__(
        self,
        network_type: NetworkType,
        version: TransactionVersion,
        deadline: Deadline,
        mosaic: Mosaic,
        duration: int,
        hash_type: HashType,
        secret: str,
        recipient: RecipientType,
        max_fee: int = 0,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None,
    ) -> None:
        secret = util.encode_hex(secret)
        if not hash_type.validate(secret):
            raise ValueError("HashType and secret have incompatible lengths.")
        super().__init__(
            TransactionType.SECRET_LOCK,
            network_type,
            version,
            deadline,
            max_fee,
            signature,
            signer,
            transaction_info,
        )
        self._set('mosaic', mosaic)
        self._set('duration', duration)
        self._set('hash_type', hash_type)
        self._set('secret', secret)
        self._set('recipient', recipient)

    @classmethod
    def create(
        cls,
        deadline: Deadline,
        mosaic: Mosaic,
        duration: int,
        hash_type: HashType,
        secret: str,
        recipient: RecipientType,
        network_type: NetworkType,
        max_fee: int = 0,
    ):
        """
        Create new secret proof transaction.

        :param deadline: Deadline to include transaction.
        :param mosaic: Mosaic to be locked.
        :param duration: Duration for funds to be released or returned.
        :param hash_type: Hash algorithm secret was generated with.
        :param secret: Hex-encoded or raw seed-proof hash.
        :param recipient: Recipient of funds.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """
        return cls(
            network_type,
            TransactionVersion.SECRET_LOCK,
            deadline,
            mosaic,
            duration,
            hash_type,
            secret,
            recipient,
            max_fee,
        )

    # CATBUFFER

    def catbuffer_size_specific(self) -> int:
        mosaic_size = Mosaic.CATBUFFER_SIZE
        duration_size = util.U64_BYTES
        hash_size = util.U8_BYTES
        secret_size = 32
        recipient_size = 25

        return mosaic_size + duration_size + hash_size + secret_size + recipient_size

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export secret lock-specific data to catbuffer."""

        # Mosaic mosaic
        # uint64_t duration
        # uint8_t hash_type
        # uint8_t[32] secret
        # uint8_t[25] recipient
        mosaic = self.mosaic.to_catbuffer(network_type)
        duration = util.u64_to_catbuffer(self.duration)
        hash_type = self.hash_type.to_catbuffer(network_type)
        secret = util.unhexlify(self.secret)
        secret = secret + b'\x00' * (32 - len(secret))
        recipient = Recipient.to_catbuffer(self.recipient, network_type)
        return mosaic + duration + hash_type + secret + recipient

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load secret proof-specific data data from catbuffer."""

        # Mosaic mosaic
        # uint64_t duration
        # uint8_t hash_type
        # uint8_t[32] secret
        # uint8_t[25] recipient
        mosaic, data = Mosaic.create_from_catbuffer_pair(data, network_type)
        duration = util.u64_from_catbuffer(data[:8])
        hash_type, data = HashType.create_from_catbuffer_pair(data[8:], network_type)
        hash_length = hash_type.hash_length() // 2
        secret = util.hexlify(data[:hash_length])
        data = data[32:]
        recipient, data = Recipient.create_from_catbuffer_pair(data, network_type)

        self._set('mosaic', mosaic)
        self._set('duration', duration)
        self._set('hash_type', hash_type)
        self._set('secret', secret)
        self._set('recipient', recipient)

        return data

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {
            'mosaicId',
            'amount',
            'duration',
            'hashAlgorithm',
            'secret',
            'recipient',
        }
        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        return {
            'mosaicId': util.u64_to_dto(int(self.mosaic.id)),
            'amount': util.u64_to_dto(self.mosaic.amount),
            'duration': util.u64_to_dto(self.duration),
            'hashAlgorithm': self.hash_type.to_dto(network_type),
            'secret': self.secret,
            'recipient': Recipient.to_dto(self.recipient, network_type),
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        mosaic_id = MosaicId(util.u64_from_dto(data['mosaicId']))
        amount = util.u64_from_dto(data['amount'])
        mosaic = Mosaic(mosaic_id, amount)
        duration = util.u64_from_dto(data['duration'])
        hash_type = HashType.create_from_dto(data['hashAlgorithm'], network_type)
        recipient = Recipient.create_from_dto(data['recipient'], network_type)

        self._set('mosaic', mosaic)
        self._set('duration', duration)
        self._set('hash_type', hash_type)
        self._set('secret', data['secret'])
        self._set('recipient', recipient)


@register_transaction('SECRET_LOCK')
class SecretLockInnerTransaction(InnerTransaction, SecretLockTransaction):
    """Embedded secret proof transaction."""

    __slots__ = ()
