"""
    node_time
    =========

    Describes the time of the NEM node.

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

__all__ = ['NodeTime']


# TODO(ahuszagh) Add unittests.
@util.inherit_doc
@util.dataclass(frozen=True)
class NodeTime(util.DTO):
    """
    Node information.

    :param public_key: Public key of node.
    :param port: Port to communicate with node over.

    DTO Format:
        .. code-block:: yaml

            CommunicationTimestampsDTO:
                sendTimestamp: UInt64DTO
                receiveTimestamp: UInt64DTO

            NodeTimeDTO:
                communicationTimestamps: CommunicationTimestampsDTO
    """

    send_timestamp: int
    receive_timestamp: int

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'communicationTimestamps': {
                'sendTimestamp': util.u64_to_dto(self.send_timestamp),
                'receiveTimestamp': util.u64_to_dto(self.receive_timestamp),
            },
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        timestamps = data['communicationTimestamps']
        return cls(
            send_timestamp=util.u64_from_dto(timestamps['sendTimestamp']),
            receive_timestamp=util.u64_from_dto(timestamps['receiveTimestamp']),
        )
