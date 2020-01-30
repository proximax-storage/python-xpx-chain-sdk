
from __future__ import annotations

from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['CatapultConfig']


@util.inherit_doc
@util.dataclass(frozen=True)
class CatapultConfig(util.DTO):
    """
    Basic information describing an account.

    :param catapult_config: Catapult config.

    DTO Format:
        .. code-block:: yaml

            ConfigDTO:
                height: UInt64DTO
                networkConfig: string
                supportedEntityVersions: string

            CatapultConfigDTO:
                catapultConfig: ConfigDTO
    """

    height: int
    network_config: str
    supported_entity_versions: str

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'networkConfig'}
        required_l2 = {
            'height',
            'networkConfig',
            'supportedEntityVersions'
        }
        return (
            # Level 1
            cls.validate_dto_required(data, required_l1)
            and cls.validate_dto_all(data, required_l1)
            # Level 2
            and cls.validate_dto_required(data['networkConfig'], required_l2)
            and cls.validate_dto_all(data['networkConfig'], required_l2)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        network_config = {
            'height': util.u64_to_dto(self.height),
            'networkConfig': self.network_config,
            'supportedEntityVersions': self.supported_entity_versions
        }

        return {
            'networkConfig': network_config,
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        network_config = data['networkConfig']
        return cls(
            height=util.u64_from_dto(network_config.get('height', [0, 0])),
            network_config=network_config['networkConfig'],
            supported_entity_versions=network_config['supportedEntityVersions']
        )
