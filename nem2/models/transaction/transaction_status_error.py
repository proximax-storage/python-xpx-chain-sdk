"""
    transaction_status_error
    ========================

    Model representing errors in transactions from listeners.

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
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['TransactionStatusError']


@util.inherit_doc
@util.dataclass(frozen=True)
class TransactionStatusError(util.DTO):
    """
    Model representing errors in transactions from listeners.

    :param hash: Transaction hash.
    :param status: Status error message.
    :param deadline: Transaction deadline.
    """

    hash: str
    status: str
    deadline: Deadline

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'hash': self.hash,
            'status': self.status,
            'deadline': self.deadline.to_dto(network_type),
        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        return cls(
            hash=data['hash'],
            status=data['status'],
            deadline=Deadline.from_dto(data['deadline'], network_type),
        )
