"""
    node_info
    =========

    Describes the NEM node.

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

from ..blockchain.network_type import NetworkType, OptionalNetworkType
from ... import util

__all__ = ['NodeInfo']


# TODO(ahuszagh) Add unittests.
@util.inherit_doc
@util.dataclass(frozen=True)
class NodeInfo(util.DTO):
    """
    Node information.

    :param public_key: Public key of node.
    :param port: Port to communicate with node over.

    DTO Format:
        .. code-block:: yaml

            NodeInfoDTO:
                # Hex(PublicKey) (64-bytes)
                publicKey: str
                port: integer
                networkIdentifier: integer
                version: integer
                roles: integer
                host: str
                friendlyName: str
    """

    public_key: str
    port: int
    network_identifier: NetworkType
    version: int
    roles: int
    host: str
    friendly_name: str

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'publicKey': self.public_key,
            'port': self.port,
            'networkIdentifier': self.network_identifier.to_dto(network_type),
            'version': self.version,
            'roles': self.roles,
            'host': self.host,
            'friendlyName': self.friendly_name,
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        identifier = NetworkType.create_from_dto(data['networkIdentifier'], network_type)
        return cls(
            public_key=data['publicKey'],
            port=data['port'],
            network_identifier=identifier,
            version=data['version'],
            roles=data['roles'],
            host=data['host'],
            friendly_name=data['friendlyName'],
        )
