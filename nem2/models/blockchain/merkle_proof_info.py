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

    :param payload: Proof payload.
    :param type: Data type.

    DTO Format:
        .. code-block:: yaml

            MerkleProofInfoPayloadDTO:
                merklePath: MerklePathItemDTO[]

            MerkleProofInfoDTO:
                payload: MerkleProofInfoPayloadDTO
                type: str
    """

    payload: typing.Sequence[MerklePathItem]
    type: str

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'payload', 'type'}
        required_l2 = {'merklePath'}
        return (
            # Level 1
            cls.validate_dto_required(data, required_l1)
            and cls.validate_dto_all(data, required_l1)
            # Level 2
            and cls.validate_dto_required(data['payload'], required_l2)
            and cls.validate_dto_all(data['payload'], required_l2)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'payload': {
                'merklePath': [i.to_dto(network_type) for i in self.payload],
            },
            'type': self.type,
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        payload = data['payload']
        path = payload['merklePath']
        return cls(
            payload=[MerklePathItem.create_from_dto(i, network_type) for i in path],
            type=data['type'],
        )
