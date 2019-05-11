"""
    multsig_cosignatory_modification
    ================================

    Multisig cosignatory modification.

    Enables the addition or deletion of a cosignatory from a multisig account.

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

from .multisig_cosignatory_modification_type import MultisigCosignatoryModificationType
from ..account.public_account import PublicAccount
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['MultisigCosignatoryModification']

ModificationType = MultisigCosignatoryModificationType


@util.inherit_doc
@util.dataclass(frozen=True)
class MultisigCosignatoryModification(util.Serializable):
    """
    Multisig cosignatory modification.

    :param type: Multi-signature modification type.
    :param cosignatory_public_account: Cosignatory public account.
    """

    type: ModificationType
    cosignatory_public_account: PublicAccount
    CATBUFFER_SIZE: typing.ClassVar[int] = 33 * util.U8_BYTES

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'cosignatoryPublicKey': self.cosignatory_public_account.to_dto(network_type),
            'type': self.type.to_dto(network_type),
        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        public_key = data['cosignatoryPublicKey']
        type = ModificationType.from_dto(data['type'], network_type)
        public_account = PublicAccount.from_dto(public_key, network_type)
        return cls(type, public_account)

    def to_catbuffer(
        self,
        network_type: OptionalNetworkType = None,
    ) -> bytes:
        type = self.type.to_catbuffer(network_type)
        cosignatory = self.cosignatory_public_account.to_catbuffer(network_type)
        return type + cosignatory

    @classmethod
    def from_catbuffer(
        cls,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ):
        type, data = ModificationType.from_catbuffer_pair(data, network_type)
        cosignatory = PublicAccount.from_catbuffer(data, network_type)
        return cls(type, cosignatory)
