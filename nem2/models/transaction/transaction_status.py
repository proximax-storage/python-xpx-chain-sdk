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

from .deadline import Deadline
from .transaction_status_group import TransactionStatusGroup
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['TransactionStatus']


@util.inherit_doc
@util.dataclass(frozen=True)
class TransactionStatus(util.DTOSerializable):
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
                group: string
                status: string
                # Hex(Hash) (64-bytes)
                hash: string
                deadline: UInt64DTO
                height: UInt64DTO
    """

    group: TransactionStatusGroup
    status: str
    hash: str
    deadline: Deadline
    height: int

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'group': self.group.to_dto(network_type),
            'status': self.status,
            'hash': self.hash,
            'deadline': self.deadline.to_dto(network_type),
            'height': util.u64_to_dto(self.height),
        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        return cls(
            group=TransactionStatusGroup.from_dto(data['group'], network_type),
            status=data['status'],
            hash=data['hash'],
            deadline=Deadline.from_dto(data['deadline'], network_type),
            height=util.u64_from_dto(data['height']),
        )
