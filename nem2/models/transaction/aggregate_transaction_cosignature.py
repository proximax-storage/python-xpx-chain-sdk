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
from ..blockchain.network_type import NetworkType

OptionalNetworkType = typing.Optional[NetworkType]


@util.inherit_doc
@util.dataclass(frozen=True)
class AggregateTransactionCosignature:
    """
    Aggregate transaction signer and signature.

    :param signature: Signature of aggregate transaction done by cosigner.
    :param signer: Cosigner account.
    """

    signature: str
    signer: PublicAccount

    def to_dto(
        self,
        network_type: OptionalNetworkType = None
    ) -> dict:
        return {
            'signature': self.signature,
            'signer': self.signer.public_key,
        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None
    ) -> AggregateTransactionCosignature:
        signature = data['signature']
        signer = PublicAccount.create_from_public_key(data['signer'], network_type)
        return cls(signature, signer)
