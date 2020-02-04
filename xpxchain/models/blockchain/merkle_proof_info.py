"""
    merkle_proof_info
    =================

    Describes a merkle proof.

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

from .merkle_path_item import MerklePathItem
from .network_type import OptionalNetworkType
from ... import util


__all__ = ['MerkleProofInfo']


# TODO(ahuszagh) Add unittests.
@util.inherit_doc
@util.dataclass(frozen=True)
class MerkleProofInfo(util.DTO):
    """
    Merkle proof information.

    :param merkle_path: The complementary data needed to calculate the merkle root.

    DTO Format:
        .. code-block:: yaml

            MerkleProofInfoDTO:
                merklePath: MerklePathItemDTO[]
    """

    merkle_path: typing.Sequence[MerklePathItem]

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'merklePath'}
        return (
            # Level 1
            cls.validate_dto_required(data, required_l1)
            and cls.validate_dto_all(data, required_l1)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'merklePath': [i.to_dto(network_type) for i in self.merkle_path],
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        path = data['merklePath']
        return cls(
            merkle_path=[MerklePathItem.create_from_dto(i, network_type) for i in path]
        )
