"""
    transaction_status
    ==================

    Basic information describing announced transaction.

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

from .deadline import Deadline, TIMESTAMP_NEMESIS_BLOCK, TIMESTAMP_NEMESIS_BLOCK_DTO
from .transaction_status_group import TransactionStatusGroup
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['TransactionStatus']


@util.inherit_doc
@util.dataclass(frozen=True)
class TransactionStatus(util.DTO):
    """
    Basic information describing announced transaction.

    :param group: Transaction status group.
    :param status: Status information describing error or success.
    :param hash: Transaction hash (hex-encoded).
    :param deadline: Transaction deadline.
    :param height: Block height at which it was confirmed or rejected.

    DTO Format:
        .. code-block:: yaml

            TransactionStatusDTO:
                group?: string
                status: string
                # Hex(Hash) (64-bytes)
                hash?: string
                deadline?: UInt64DTO
                height?: UInt64DTO
    """

    group: TransactionStatusGroup
    status: str
    hash: str
    deadline: Deadline
    height: int

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'status'}
        all_keys = required_keys | {'group', 'hash', 'deadline', 'height'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, all_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        data: dict = {'status': self.status}
        timestamp = self.deadline.to_timestamp()
        if self.group != TransactionStatusGroup.UNKNOWN:
            data['group'] = typing.cast(str, self.group.value)
        if self.hash:
            data['hash'] = self.hash
        if timestamp != TIMESTAMP_NEMESIS_BLOCK:
            data['deadline'] = util.u64_to_dto(timestamp)
        if self.height:
            data['height'] = util.u64_to_dto(self.height)

        return data

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        group = data.get('group', 'unknown')
        hash = data.get('hash', '')
        timestamp = data.get('deadline', TIMESTAMP_NEMESIS_BLOCK_DTO)
        height = data.get('height', [0, 0])
        return cls(
            group=TransactionStatusGroup(group),
            status=data['status'],
            hash=hash,
            deadline=Deadline.create_from_timestamp(util.u64_from_dto(timestamp)),
            height=util.u64_from_dto(height),
        )
