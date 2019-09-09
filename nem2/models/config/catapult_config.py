
from __future__ import annotations

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
                blockChainConfig: string
                supportedEntityVersions: string

            CatapultConfigDTO:
                catapultConfig: ConfigDTO
    """

    height: int
    blockchain_config: str
    supported_entity_versions: str

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'catapultConfig'}
        required_l2 = {
            'height',
            'blockChainConfig',
            'supportedEntityVersions'
        }
        return (
            # Level 1
            cls.validate_dto_required(data, required_l1)
            and cls.validate_dto_all(data, required_l1)
            # Level 2
            and cls.validate_dto_required(data['catapultConfig'], required_l2)
            and cls.validate_dto_all(data['catapultConfig'], required_l2)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        catapult_config = {
            'height': util.u64_to_dto(self.height),
            'blockChainConfig': self.public_key,
            'supportedEntityVersions': self.supported_entity_versions
        }

        return {
            'catapultConfig': catapult_config,
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        catapult_config = data['catapultConfig']
        return cls(
            height=util.u64_from_dto(catapult_config.get('height', [0, 0])),
            blockchain_config=catapult_config['blockChainConfig'],
            supported_entity_versions=catapult_config['supportedEntityVersions']
        )
