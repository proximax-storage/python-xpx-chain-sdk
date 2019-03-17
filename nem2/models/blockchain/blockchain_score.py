"""
    block_info
    ==========

    Blockchain data describing the block difficulty.

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

from nem2 import util
from .network_type import NetworkType

OptionalNetworkType = typing.Optional[NetworkType]


@util.inherit_doc
@util.dataclass(frozen=True, score=0)
class BlockchainScore(util.DTO):
    """
    Blockchain score describing the block difficulty.

    :param score: Blockchain score.
    """

    score: int

    @property
    def score_low(self) -> int:
        """Get the low 64-bits of the blockchain score."""
        return util.u128_low(self.score)

    scoreLow = util.undoc(score_low)

    @property
    def score_high(self) -> int:
        """Get the high 64-bits of the blockchain score."""
        return util.u128_high(self.score)

    scoreHigh = util.undoc(score_high)

    def to_dto(
        self,
        network_type: OptionalNetworkType = None
    ) -> dict:
        return {
            'scoreLow': util.u64_to_dto(self.score_low),
            'scoreHigh': util.u64_to_dto(self.score_high),
        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ) -> BlockchainScore:
        score_low = data['scoreLow']
        score_high = data['scoreHigh']
        return cls(util.u128_from_dto([score_low, score_high]))
