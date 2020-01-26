"""
    aggregate_transaction_info
    ==========================

    Aggregate transaction metadata.

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

from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['AggregateTransactionInfo']


@util.inherit_doc
@util.dataclass(frozen=True)
class AggregateTransactionInfo(util.DTO):
    """Aggregate transaction metadata."""

    height: int
    index: int
    id: str
    aggregate_hash: str
    aggregate_id: str

    def is_unconfirmed(self) -> bool:
        """Is transaction pending to be included."""

        return (
            self.height == 0
            and self.aggregate_hash == self.aggregate_id
        )

    def is_confirmed(self) -> bool:
        """Is transaction already included."""
        return self.height > 0

    def has_missing_signatures(self) -> bool:
        """Does the transaction have missing signatures."""
        return (
            self.height == 0
            and self.aggregate_hash != self.aggregate_id
        )

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {
            'height',
            'index',
            'id',
            'aggregateHash',
            'aggregateId',
        }
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'height': util.u64_to_dto(self.height),
            'index': self.index,
            'id': self.id,
            'aggregateHash': self.aggregate_hash,
            'aggregateId': self.aggregate_id,
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
            height=util.u64_from_dto(data['height']),
            index=data['index'],
            id=data['id'],
            aggregate_hash=data['aggregateHash'],
            aggregate_id=data['aggregateId'],
        )
