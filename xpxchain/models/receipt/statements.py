"""
    statements
    =================

    Describes statements.

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
from .transaction_statement import TransactionStatement
from .resolution_statement import ResolutionStatement
from ... import util


__all__ = ['Statements']


@util.inherit_doc
@util.dataclass(frozen=True)
class Statements(util.DTO):
    """
    Statements information.

    DTO Format:
        .. code-block:: yaml

            StatementsDTO:
                transactionStatements: TransactionStatementDTO[]
                addressResolutionStatements: ResolutionStatementDTO[]
                mosaicResolutionStatements: ResolutionStatementDTO[]
    """

    transaction_statements: typing.Sequence[TransactionStatement]
    address_resolution_statements: typing.Sequence[ResolutionStatement]
    mosaic_resolution_statements: typing.Sequence[ResolutionStatement]

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'transactionStatements', 'addressResolutionStatements', 'mosaicResolutionStatements'}
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
            'transactionStatements': [i.to_dto(network_type) for i in self.transaction_statements],
            'addressResolutionStatements': [i.to_dto(network_type) for i in self.address_resolution_statements],
            'mosaicResolutionStatements': [i.to_dto(network_type) for i in self.mosaic_resolution_statements],
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
            transaction_statements=[
                TransactionStatement.create_from_dto(i, network_type) for i in data['transactionStatements']
            ],
            address_resolution_statements=[
                ResolutionStatement.create_from_dto(i, network_type) for i in data['addressResolutionStatements']
            ],
            mosaic_resolution_statements=[
                ResolutionStatement.create_from_dto(i, network_type) for i in data['mosaicResolutionStatements']
            ]
        )
