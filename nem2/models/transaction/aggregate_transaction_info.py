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

from nem2 import util


@util.inherit_doc
@util.dataclass(frozen=True)
class AggregateTransactionInfo(util.Dto):
    """Aggregate transaction metadata."""

    height: int
    index: int
    id: str
    aggregate_hash: str
    aggregate_id: str

    def is_unconfirmed(self):
        """Is transaction pending to be included."""

        return all((
            self.height == 0,
            self.aggregate_hash == self.aggregate_id,
        ))

    isUnconfirmed = util.undoc(is_unconfirmed)

    def is_confirmed(self) -> bool:
        """Is transaction already included."""
        return self.height > 0

    isConfirmed = util.undoc(is_confirmed)

    def has_missing_signatures(self) -> bool:
        """Does the transaction have missing signatures."""
        return all((
            self.height == 0,
            self.aggregate_hash != self.aggregate_id,
        ))

    hasMissingSignatures = util.undoc(has_missing_signatures)

    def to_dto(self) -> dict:
        return {
            'height': util.uint64_to_dto(self.height),
            'index': self.index,
            'id': self.id,
            'aggregateHash': self.aggregate_hash,
            'aggregateId': self.aggregate_id,
        }

    @classmethod
    def from_dto(cls, data: dict) -> 'TransactionInfo':
        return cls(
            height=util.dto_to_uint64(data['height']),
            index=data['index'],
            id=data['id'],
            aggregate_hash=data['aggregateHash'],
            aggregate_id=data['aggregateId'],
        )
