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

import struct
import typing

from nem2 import util
from .hash_type import HashType
from .inner_transaction import InnerTransaction
from .transaction import Transaction
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion

if typing.TYPE_CHECKING:
    from .deadline import Deadline
    from .transaction_info import TransactionInfo
    from ..account.public_account import PublicAccount
    from ..blockchain.network_type import NetworkType


@util.inherit_doc
@util.dataclass(frozen=True)
class SecretProofTransaction(Transaction):
    """
    Secret-proof transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param fee: Fee for the transaction. Higher fees increase transaction priority.
    :param hash_type: Hash algorithm secret was generated with.
    :param secret: Hex-encoded seed-proof hash.
    :param proof: Hex-encoded seed proof.
    :param signature: (Optional) Transaction signature (missing if aggregate transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    hash_type: 'HashType'
    secret: str
    proof: str

    def __init__(self,
        network_type: 'NetworkType',
        version: 'TransactionVersion',
        deadline: 'Deadline',
        fee: int,
        hash_type: 'HashType',
        secret: str,
        proof: str,
        signature: typing.Optional[str] = None,
        signer: typing.Optional['PublicAccount'] = None,
        transaction_info: typing.Optional['TransactionInfo'] = None,
    ):
        if not hash_type.validate(secret):
            raise ValueError("HashType and secret have incompatible lengths.")
        super().__init__(
            TransactionType.SECRET_PROOF,
            network_type,
            version,
            deadline,
            fee,
            signature,
            signer,
            transaction_info,
        )
        object.__setattr__(self, 'hash_type', hash_type)
        object.__setattr__(self, 'secret', secret)
        object.__setattr__(self, 'proof', proof)

    @classmethod
    def create(
        cls,
        deadline: 'Deadline',
        hash_type: 'HashType',
        secret: str,
        proof: str,
        network_type: 'NetworkType',
    ) -> 'SecretProofTransaction':
        """
        Create new secret proof transaction.

        :param deadline: Deadline to include transaction.
        :param hash_type: Hash algorithm secret was generated with.
        :param secret: Hex-encoded seed-proof hash.
        :param proof: Hex-encoded seed proof.
        :param network_type: Network type.
        """
        return SecretProofTransaction(
            network_type,
            TransactionVersion.SECRET_PROOF,
            deadline,
            0,
            hash_type,
            secret,
            proof
        )

    def entity_size(self) -> int:
        # extra 3 bytes, 1 for hash_type, 2 for proof size.
        shared_size = self.shared_entity_size()
        secret_size = len(self.secret) // 2
        proof_size = len(self.proof) // 2

        return shared_size + secret_size + proof_size + 3

    def to_catbuffer_specific(self) -> bytes:
        """Export secret proof-specific data to catbuffer."""

        # uint8_t hash_type
        # uint8_t[32] secret
        # uint16_t proof_size
        # uint8_t[proof_size] proof
        proof_size = len(self.proof) // 2
        hash_type = self.hash_type.to_catbuffer()
        secret = util.unhexlify(self.secret)
        proof = struct.pack('<H', proof_size) + util.unhexlify(self.proof)
        return hash_type + secret + proof

    def load_catbuffer_specific(self, data: bytes) -> bytes:
        """Load secret proof-specific data data from catbuffer."""

        # uint8_t hash_type
        # uint8_t[32] secret
        # uint16_t proof_size
        # uint8_t[proof_size] proof
        hash_type, data = HashType.from_catbuffer(data)
        hash_length = hash_type.hash_length() // 2
        secret = util.hexlify(data[:hash_length])
        proof_size = struct.unpack('<H', data[hash_length: hash_length + 2])[0]
        proof = util.hexlify(data[hash_length + 2: hash_length + proof_size + 2])

        object.__setattr__(self, 'hash_type', hash_type)
        object.__setattr__(self, 'secret', secret)
        object.__setattr__(self, 'proof', proof)

        return data[hash_length + proof_size + 2:]

    def to_aggregate(self, signer: 'PublicAccount') -> 'SecretProofInnerTransaction':
        """Convert transaction to inner transaction."""

        data = self.asdict()
        data['signer'] = signer
        data.pop('type')
        return SecretProofInnerTransaction(**data)


class SecretProofInnerTransaction(InnerTransaction, SecretProofTransaction):
    """Embedded secret proof transaction."""

    __slots__ = ()
