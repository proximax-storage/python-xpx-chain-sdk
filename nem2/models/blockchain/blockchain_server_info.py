"""
    block_info
    ==========

    Blockchain info describing stored data.

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

from .network_type import OptionalNetworkType
from ... import util

__all__ = ['BlockchainServerInfo']


@util.inherit_doc
@util.dataclass(frozen=True)
class BlockchainServerInfo(util.DTO):
    """
    Blockchain information describing stored data.

    :param rest_version: The catapult-rest component version.
    :param sdk_version: The catapult-sdk component version.

    DTO Format:
        .. code-block:: yaml

            BlockchainStorageInfoDTO:
                restVersion: string
                sdkVersion: string
    """

    rest_version: str
    sdk_version: str

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'serverInfo'}
        required_l21 = {'restVersion', 'sdkVersion'}

        return (
            # Level 1
            cls.validate_dto_required(data, required_l1)
            and cls.validate_dto_all(data, required_l1)
            # Level 2
            and cls.validate_dto_required(data['serverInfo'], required_l21)
            and cls.validate_dto_all(data['serverInfo'], required_l21)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'restVersion': self.rest_version,
            'sdkVersion': self.sdk_version
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        server_info = data['serverInfo']

        return cls(
            rest_version=server_info['restVersion'],
            sdk_version=server_info['sdkVersion'],
        )
