"""
    aggregate_transaction_cosignature
    =================================

    Aggregate transaction signer and signature.

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

from ..account.public_account import PublicAccount
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['AggregateTransactionCosignature']

SIZE = PublicAccount.CATBUFFER_SIZE + 64 * util.U8_BYTES


@util.inherit_doc
@util.dataclass(frozen=True)
class AggregateTransactionCosignature(util.Model):
    """
    Aggregate transaction signer and signature.

    :param signature: Signature of aggregate transaction done by cosigner.
    :param signer: Cosigner account.
    """

    signature: str
    signer: PublicAccount
    CATBUFFER_SIZE: typing.ClassVar[int] = SIZE

    def __init__(
        self,
        signature: typing.AnyStr,
        signer: PublicAccount,
    ) -> None:
        signature = util.encode_hex(signature)
        if len(signature) != 128:
            raise ValueError("Invalid signature length")
        self._set('signature', signature)
        self._set('signer', signer)

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'signature', 'signer'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'signature': self.signature,
            'signer': self.signer.public_key,
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        signature = data['signature']
        signer = PublicAccount.create_from_public_key(data['signer'], network_type)
        return cls(signature, signer)

    def to_catbuffer(
        self,
        network_type: OptionalNetworkType = None,
        fee_strategy: util.FeeCalculationStrategy = util.FeeCalculationStrategy.MEDIUM,
    ) -> bytes:
        # uint8_t[32] signer
        # uint8_t[64] signature
        signer = util.unhexlify(self.signer.public_key)
        signature = util.unhexlify(self.signature)
        return signer + signature

    @classmethod
    def create_from_catbuffer(
        cls,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ):
        # uint8_t[32] signer
        # uint8_t[64] signature
        signer = PublicAccount.create_from_public_key(data[:32], network_type)
        signature = data[32:96]
        return cls(signature, signer)  # type: ignore
