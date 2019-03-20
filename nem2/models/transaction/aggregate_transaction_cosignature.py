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

from nem2 import util
from ..account.public_account import PublicAccount
from ..blockchain.network_type import OptionalNetworkType

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

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'signature': self.signature,
            'signer': self.signer.to_dto(network_type),
        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        signature = data['signature']
        signer = PublicAccount.from_dto(data['signer'], network_type)
        return cls(signature, signer)

    def to_catbuffer(
        self,
        network_type: OptionalNetworkType = None,
    ) -> bytes:
        # uint8_t[32] signer
        # uint8_t[64] signature
        signer = self.signer.to_catbuffer(network_type)
        signature = util.unhexlify(self.signature)
        return signer + signature

    @classmethod
    def from_catbuffer(
        cls,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ):
        # uint8_t[32] signer
        # uint8_t[64] signature
        signer = PublicAccount.from_catbuffer(data[:32], network_type)
        signature = data[32:96]
        return cls(signature, signer)
