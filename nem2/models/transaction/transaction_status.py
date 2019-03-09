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

from nem2 import util
from .deadline import Deadline
from .transaction_status_group import TransactionStatusGroup


@util.inherit_doc
@util.dataclass(frozen=True)
class TransactionStatus(util.Dto):
    """
    Basic information describing announced transaction.

    :param group: Transaction status group.
    :param status: Status information describing error or success.
    :param hash: Transaction hash (hex-encoded).
    :param deadline: Transaction deadline.
    :param height: Block height at which it was confirmed or rejected.
    """

    group: 'TransactionStatusGroup'
    status: str
    hash: str
    deadline: 'Deadline'
    height: int

    def to_dto(self) -> dict:
        return {
            'group': self.group.to_dto(),
            'status': self.status,
            'hash': self.hash,
            'deadline': self.deadline.to_dto(),
            'height': util.uint64_to_dto(self.height),
        }

    @classmethod
    def from_dto(cls, data: dict) -> 'TransactionStatus':
        return cls(
            group=TransactionStatusGroup.from_dto(data['group']),
            status=data['status'],
            hash=data['hash'],
            deadline=Deadline.from_dto(data['deadline']),
            height=util.dto_to_uint64(data['height']),
        )
