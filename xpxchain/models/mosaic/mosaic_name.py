"""
    mosaic_name
    ===========

    Describes a mosaic by name and identifier.

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
from .mosaic_id import MosaicId
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['MosaicName']


@util.inherit_doc
@util.dataclass(frozen=True)
class MosaicName(util.DTO):
    """
    Mosaic name and identifiers.

    :param mosaic_id: Mosaic ID.
    :param names: Mosaic name.

    DTO Format:
        .. code-block:: yaml

            MosaicNameDTO:
                mosaicId: UInt64DTO
                names: string
    """

    mosaic_id: MosaicId
    names: typing.Sequence[str]

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'mosaicId', 'names'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'mosaicId': util.u64_to_dto(int(self.mosaic_id)),
            'names': self.names,
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
            mosaic_id=MosaicId(util.u64_from_dto(data['mosaicId'])),
            names=data['names'],
        )
