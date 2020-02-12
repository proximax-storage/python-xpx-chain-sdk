
from __future__ import annotations

from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['CatapultUpgrade', 'Upgrade']


@util.inherit_doc
@util.dataclass(frozen=True)
class Upgrade(util.DTO):

    height: int
    blockchain_version: int

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'height', 'blockChainVersion'}
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
            'height': util.u64_to_dto(self.height),
            'blockChainVersion': util.u64_to_dto(self.blockchain_version),
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
            height=util.u64_from_dto(data['height']),
            blockchain_version=util.u64_from_dto(data['blockChainVersion']),
        )


@util.inherit_doc
@util.dataclass(frozen=True)
class CatapultUpgrade(util.DTO):
    """
    Basic information describing a blockchain upgrade.

    :param blockchain_upgrade: Blockchain upgrade.

    """

    blockchain_upgrade: Upgrade

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'blockchainUpgrade'}
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
            'blockchainUpgrade': self.blockchain_upgrade.to_dto(),
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
            blockchain_upgrade=Upgrade.create_from_dto(data['blockchainUpgrade']),
        )
