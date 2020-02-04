"""
    secret_proof_transaction
    ========================

    Secret-proof transaction.

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
from .registry import register_transaction
from .recipient import Recipient, RecipientType
from .transaction import Transaction
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ... import util

__all__ = [
    'SecretProofTransaction',
    'SecretProofInnerTransaction',
]


@util.inherit_doc
@util.dataclass(frozen=True)
@register_transaction('SECRET_PROOF')
class SecretProofTransaction(Transaction):
    """
    Secret-proof transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param hash_type: Hash algorithm secret was generated with.
    :param secret: Hex-encoded or raw seed-proof hash.
    :param proof: Hex-encoded or raw seed proof.
    :param signature: (Optional) Transaction signature (missing if embedded transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    hash_type: HashType
    secret: str
    recipient: RecipientType
    proof: str

    def __init__(
        self,
        network_type: NetworkType,
        version: TransactionVersion,
        deadline: Deadline,
        hash_type: HashType,
        secret: str,
        recipient: RecipientType,
        proof: str,
        max_fee: int = 0,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None,
    ) -> None:
        secret = util.encode_hex(secret)
        proof = util.encode_hex(proof)
        if not hash_type.validate(secret):
            raise ValueError("HashType and secret have incompatible lengths.")
        super().__init__(
            TransactionType.SECRET_PROOF,
            network_type,
            version,
            deadline,
            max_fee,
            signature,
            signer,
            transaction_info,
        )
        self._set('hash_type', hash_type)
        self._set('secret', secret)
        self._set('recipient', recipient)
        self._set('proof', proof)

    @classmethod
    def create(
        cls,
        deadline: Deadline,
        hash_type: HashType,
        secret: str,
        recipient: RecipientType,
        proof: str,
        network_type: NetworkType,
        max_fee: int = 0,
    ):
        """
        Create new secret proof transaction.

        :param deadline: Deadline to include transaction.
        :param hash_type: Hash algorithm secret was generated with.
        :param secret: Hex-encoded or raw seed-proof hash.
        :param proof: Hex-encoded or raw seed proof.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """
        return cls(
            network_type,
            TransactionVersion.SECRET_PROOF,
            deadline,
            hash_type,
            secret,
            recipient,
            proof,
            max_fee,
        )

    # CATBUFFER

    def catbuffer_size_specific(self) -> int:
        # extra 3 bytes, 1 for hash_type, 2 for proof size.
        # The proof size is always 32, even if HASH_160 is used.
        # The hash is just 0-padded to 32 bytes.
        extra_size = util.U8_BYTES + util.U16_BYTES
        secret_size = 32
        recipient_size = 25
        proof_size = len(self.proof) // 2
        return extra_size + secret_size + recipient_size + proof_size

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export secret proof-specific data to catbuffer."""

        # uint8_t hash_type
        # uint8_t[32] secret
        # uint16_t proof_size
        # uint8_t[proof_size] proof
        proof_size = len(self.proof) // 2
        hash_type = self.hash_type.to_catbuffer(network_type)
        secret = util.unhexlify(self.secret)
        secret = secret + b'\x00' * (32 - len(secret))
        recipient = Recipient.to_catbuffer(self.recipient, network_type)
        proof = util.u16_to_catbuffer(proof_size) + util.unhexlify(self.proof)
        return hash_type + secret + recipient + proof

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load secret proof-specific data data from catbuffer."""

        # uint8_t hash_type
        # uint8_t[32] secret
        # uint16_t proof_size
        # uint8_t[proof_size] proof
        hash_type, data = HashType.create_from_catbuffer_pair(data, network_type)
        hash_length = hash_type.hash_length() // 2
        secret = util.hexlify(data[:hash_length])
        data = data[32:]
        recipient, data = Recipient.create_from_catbuffer_pair(data, network_type)
        proof_size = util.u16_from_catbuffer(data[:2])
        proof = util.hexlify(data[2: proof_size + 2])

        self._set('hash_type', hash_type)
        self._set('secret', secret)
        self._set('recipient', recipient)
        self._set('proof', proof)

        return data[proof_size + 2:]

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'hashAlgorithm', 'secret', 'recipient', 'proof'}
        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        return {
            'hashAlgorithm': self.hash_type.to_dto(network_type),
            'secret': self.secret,
            'recipient': Recipient.to_dto(self.recipient, network_type),
            'proof': self.proof,
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        hash_type = HashType.create_from_dto(data['hashAlgorithm'], network_type)
        recipient = Recipient.create_from_dto(data['recipient'], network_type)

        self._set('hash_type', hash_type)
        self._set('secret', data['secret'])
        self._set('proof', data['proof'])
        self._set('recipient', recipient)


@register_transaction('SECRET_PROOF')
class SecretProofInnerTransaction(InnerTransaction, SecretProofTransaction):
    """Embedded secret proof transaction."""

    __slots__ = ()
