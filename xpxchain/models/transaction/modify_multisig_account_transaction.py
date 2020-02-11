"""
    modify_multisig_account_transaction
    ===================================

    Modify multisig account transaction.

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
from .multisig_cosignatory_modification import MultisigCosignatoryModification
from .registry import register_transaction
from .transaction import Transaction
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ... import util

__all__ = [
    'ModifyMultisigAccountTransaction',
    'ModifyMultisigAccountInnerTransaction',
]

MultisigCosignatoryModificationList = typing.Sequence[MultisigCosignatoryModification]


@util.inherit_doc
@util.dataclass(frozen=True)
@register_transaction('MODIFY_MULTISIG_ACCOUNT')
class ModifyMultisigAccountTransaction(Transaction):
    """
    Modify multisig account transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param min_approval_delta: Minimum approval relative change.
    :param min_removal_delta: Minimum removal relative change.
    :param modifications: List of modifications.
    :param signature: (Optional) Transaction signature (missing if embedded transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    min_approval_delta: int
    min_removal_delta: int
    modifications: typing.Sequence[MultisigCosignatoryModification]

    def __init__(
        self,
        network_type: NetworkType,
        version: TransactionVersion,
        deadline: Deadline,
        min_approval_delta: int,
        min_removal_delta: int,
        max_fee: int = 0,
        modifications: typing.Optional[MultisigCosignatoryModificationList] = None,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None,
    ) -> None:
        super().__init__(
            TransactionType.MODIFY_MULTISIG_ACCOUNT,
            network_type,
            version,
            deadline,
            max_fee,
            signature,
            signer,
            transaction_info,
        )
        self._set('min_approval_delta', min_approval_delta)
        self._set('min_removal_delta', min_removal_delta)
        self._set('modifications', modifications or [])

    @classmethod
    def create(
        cls,
        deadline: Deadline,
        min_approval_delta: int,
        min_removal_delta: int,
        modifications: MultisigCosignatoryModificationList,
        network_type: NetworkType,
        max_fee: int = 0,
    ):
        """
        Create new transfer transaction.

        :param deadline: Deadline to include transaction.
        :param min_approval_delta: Minimum approval relative change.
        :param min_removal_delta: Minimum removal relative change.
        :param modifications: List of modifications.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """
        return cls(
            network_type,
            TransactionVersion.MODIFY_MULTISIG_ACCOUNT,
            deadline,
            min_approval_delta,
            min_removal_delta,
            max_fee,
            modifications
        )

    # CATBUFFER

    def catbuffer_size_specific(self) -> int:
        approval_size = util.I8_BYTES
        removal_size = util.I8_BYTES
        modification_size = MultisigCosignatoryModification.CATBUFFER_SIZE
        modifications_size = util.U8_BYTES + modification_size * len(self.modifications)
        return approval_size + removal_size + modifications_size

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export modify multisig account-specific data to catbuffer."""

        # int8 min_removal_delta
        # int8 min_approval_delta
        # uint8 modifications_count
        # CosignatoryModification { uint8 modification_type; uint8[32] key; }
        # CosignatoryModification[modifications_count] modifications
        removal = util.i8_to_catbuffer(self.min_removal_delta)
        approval = util.i8_to_catbuffer(self.min_approval_delta)
        modifications_count = util.u8_to_catbuffer(len(self.modifications))
        modifications = MultisigCosignatoryModification.sequence_to_catbuffer(
            self.modifications,
            network_type
        )

        return removal + approval + modifications_count + modifications

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load modify multisig account-specific data from catbuffer."""

        from_catbuffer = MultisigCosignatoryModification.sequence_from_catbuffer_pair
        # int8 min_removal_delta
        # int8 min_approval_delta
        # uint8 modifications_count
        # CosignatoryModification { uint8 modification_type; uint8[32] key; }
        # CosignatoryModification[modifications_count] modifications
        removal = util.i8_from_catbuffer(data[:1])
        approval = util.i8_from_catbuffer(data[1:2])
        modifications_count = util.u8_from_catbuffer(data[2:3])
        data = data[3:]
        modifications, data = from_catbuffer(data, modifications_count, network_type)

        self._set('min_removal_delta', removal)
        self._set('min_approval_delta', approval)
        self._set('modifications', modifications)

        return data

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'minApprovalDelta', 'minRemovalDelta', 'modifications'}
        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        return {
            'minApprovalDelta': util.u8_to_dto(self.min_approval_delta),
            'minRemovalDelta': util.u8_to_dto(self.min_removal_delta),
            'modifications': MultisigCosignatoryModification.sequence_to_dto(
                self.modifications,
                network_type
            ),
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        approval = util.i8_from_dto(data['minApprovalDelta'])
        removal = util.i8_from_dto(data['minRemovalDelta'])
        modifications = MultisigCosignatoryModification.sequence_from_dto(
            data.get('modifications', []),
            network_type
        )

        self._set('min_approval_delta', approval)
        self._set('min_removal_delta', removal)
        self._set('modifications', modifications)


@register_transaction('MODIFY_MULTISIG_ACCOUNT')
class ModifyMultisigAccountInnerTransaction(
    InnerTransaction,
    ModifyMultisigAccountTransaction
):
    """Embedded modify multisig account transaction."""

    __slots__ = ()
