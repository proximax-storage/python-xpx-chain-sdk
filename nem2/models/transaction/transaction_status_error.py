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

    DTO Format:
        .. code-block:: yaml

            # The DTO format is implied from the typescript SDK,
            # and is only returned by listeners.
            TransactionStatusDTO:
                status: string
                # Hex(Hash) (64-bytes)
                hash: string
                deadline: UInt64DTO
    """

    hash: str
    status: str
    deadline: Deadline

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'hash', 'status', 'deadline'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'hash': self.hash,
            'status': self.status,
            'deadline': util.u64_to_dto(self.deadline.to_timestamp()),
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        return cls(
            hash=data['hash'],
            status=data['status'],
            deadline=Deadline.create_from_timestamp(util.u64_from_dto(data['deadline'])),
        )
