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
class MultisigCosignatoryModification(util.Model):
    """
    Multisig cosignatory modification.

    :param type: Multi-signature modification type.
    :param cosignatory_public_account: Cosignatory public account.
    """

    type: ModificationType
    cosignatory_public_account: PublicAccount
    CATBUFFER_SIZE: typing.ClassVar[int] = 33 * util.U8_BYTES

    def __init__(
        self,
        cosignatory_public_account: PublicAccount,
        type: ModificationType
    ) -> None:
        self._set('cosignatory_public_account', cosignatory_public_account)
        self._set('type', type)

    @classmethod
    def create(
        cls,
        cosignatory_public_account: PublicAccount,
        type: ModificationType
    ):
        return cls(
            cosignatory_public_account,
            type
        )

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'cosignatoryPublicKey', 'type'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'cosignatoryPublicKey': self.cosignatory_public_account.public_key,
            'type': self.type.to_dto(network_type),
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        public_key = data['cosignatoryPublicKey']
        type = ModificationType.create_from_dto(data['type'], network_type)
        public_account = PublicAccount.create_from_public_key(public_key, network_type)
        return cls(public_account, type)

    def to_catbuffer(
        self,
        network_type: OptionalNetworkType = None,
        fee_strategy: util.FeeCalculationStrategy = util.FeeCalculationStrategy.MEDIUM,
    ) -> bytes:
        type = self.type.to_catbuffer(network_type)
        cosignatory = util.unhexlify(self.cosignatory_public_account.public_key)
        return type + cosignatory

    @classmethod
    def create_from_catbuffer(
        cls,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ):
        type, data = ModificationType.create_from_catbuffer_pair(data, network_type)
        cosignatory = PublicAccount.create_from_public_key(data[:32], network_type)
        return cls(cosignatory, type)
