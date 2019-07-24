"""
    transaction_announce_response
    =============================

    Response from announcing a transaction.

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

__all__ = ['TransactionAnnounceResponse']


@util.inherit_doc
@util.dataclass(frozen=True)
class TransactionAnnounceResponse(util.DTO):
    """
    Response from announcing a transaction.

    DTO Format:
        .. code-block:: yaml

            AnnounceTransactionInfoDTO:
                message: string
    """

    message: str

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'message'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {'message': self.message}

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        return cls(data['message'])
