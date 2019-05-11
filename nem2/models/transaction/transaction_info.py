"""
    transaction_info
    ================

    Transaction metadata.

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

from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['TransactionInfo']


@util.inherit_doc
@util.dataclass(frozen=True, hash=None, merkle_component_hash=None)
class TransactionInfo(util.DTOSerializable):
    """Transaction metadata."""

    height: int
    index: int
    id: str
    hash: typing.Optional[str]
    merkle_component_hash: typing.Optional[str]

    def is_unconfirmed(self):
        """Is transaction pending to be included."""

        return (
            self.height == 0
            and self.hash is None
            and self.merkle_component_hash is None
        )

    def is_confirmed(self) -> bool:
        """Is transaction already included."""
        return self.height > 0

    def has_missing_signatures(self) -> bool:
        """Does the transaction have missing signatures."""
        return (
            self.height == 0
            and self.hash != self.merkle_component_hash
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        data = {
            'height': util.u64_to_dto(self.height),
            'index': self.index,
            'id': self.id,
        }
        if self.hash is not None:
            data['hash'] = self.hash
        if self.merkle_component_hash is not None:
            data['merkleComponentHash'] = self.merkle_component_hash
        return data

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        return cls(
            height=util.u64_from_dto(data['height']),
            index=data['index'],
            id=data['id'],
            hash=data.get('hash'),
            merkle_component_hash=data.get('merkleComponentHash'),
        )
