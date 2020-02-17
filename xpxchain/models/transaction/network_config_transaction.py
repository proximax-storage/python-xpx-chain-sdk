"""
    network_config_transaction
    ====================

    Transfer transaction.

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

from .deadline import Deadline
from .inner_transaction import InnerTransaction
from .registry import register_transaction
from .transaction import Transaction
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ... import util

__all__ = [
    'NetworkConfigTransaction',
    'NetworkConfigInnerTransaction',
]


@util.inherit_doc
@util.dataclass(frozen=True)
@register_transaction('NETWORK_CONFIG')
class NetworkConfigTransaction(Transaction):
    """
    Network configuration transaction.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param applyHeightDelta: Blockchain height from which the configuration is applied.
    :param networkConfig: Network configuration.
    :param supportedEntityVersions: Supported entities.
    :param signature: (Optional) Transaction signature (missing if embedded transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    apply_height_delta: int
    network_config: str
    supported_entity_versions: str

    def __init__(
        self,
        network_type: NetworkType,
        version: TransactionVersion,
        deadline: Deadline,
        apply_height_delta: int,
        network_config: str,
        supported_entity_versions: str,
        max_fee: int = 0,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None
    ) -> None:
        super().__init__(
            TransactionType.TRANSFER,
            network_type,
            version,
            deadline,
            max_fee,
            signature,
            signer,
            transaction_info
        )
        self._set('apply_height_delta', apply_height_delta)
        self._set('network_config', network_config)
        self._set('supported_entity_versions', supported_entity_versions)

    @classmethod
    def create(
        cls,
        deadline: Deadline,
        network_type: NetworkType,
        apply_height_delta: int,
        network_config: str,
        supported_entity_versions: str,
        max_fee: int = 0,
    ):
        """
        Create new network configuration transaction.

        :param deadline: Deadline to include transaction.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """
        return cls(
            network_type,
            TransactionVersion.TRANSFER,
            deadline,
            apply_height_delta,
            network_config,
            supported_entity_versions,
            max_fee,
        )

    # CATBUFFER

    def catbuffer_size_specific(self) -> int:
        apply_height_delta_size = util.U64_BYTES
        extra_size = util.U8_BYTES + util.U16_BYTES
        network_config_size = util.U8_BYTES * len(self.network_config)
        supported_entity_versions_size = util.U8_BYTES * len(self.supported_entity_versions)

        return apply_height_delta_size + extra_size + network_config_size + supported_entity_versions_size

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export transfer-specific data to catbuffer."""

        # uint64_t apply_height_delta
        # uint16_t network_config_size
        # uint16_t supported_entity_versions_size
        # uint8_t[network_config_size] network_config
        # uint8_t[supported_entity_versions_size] supported_entity_versions
        apply_height_delta = util.u64_to_catbuffer(self.apply_height_delta)
        network_config_size = util.u16_to_catbuffer(len(self.network_config))
        supported_entity_versions_size = util.u16_to_catbuffer(len(self.supported_entity_versions))
        network_config = self.network_config.encode('utf-8')
        supported_entity_versions = self.supported_entity_versions.encode('utf-8')

        return apply_height_delta
        + network_config_size
        + supported_entity_versions_size
        + network_config
        + supported_entity_versions

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load transfer-specific data from catbuffer."""

        # uint64_t apply_height_delta
        # uint16_t network_config_size
        # uint16_t supported_entity_versions_size
        # uint8_t[network_config_size] network_config
        # uint8_t[supported_entity_versions_size] supported_entity_versions
        apply_height_delta = util.u64_from_catbuffer(data[:util.U64_BYTES])
        data = data[util.U64_BYTES:]
        network_config_size = util.u16_from_catbuffer(data[:util.U16_BYTES])
        data = data[util.U16_BYTES:]
        supported_entity_versions_size = util.u16_from_catbuffer(data[:util.U16_BYTES])
        data = data[util.U16_BYTES:]
        network_config = data[:network_config_size].decode('utf-8')
        data = data[:network_config_size]
        supported_entity_versions = data[:supported_entity_versions_size].decode('utf-8')
        data = data[:supported_entity_versions_size]

        self._set('apply_height_delta', apply_height_delta)
        self._set('network_config', network_config)
        self._set('supported_entity_versions', supported_entity_versions)

        return data

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'applyHeightDelta', 'networkConfig', 'supportedEntityVersions'}

        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        return {
            'applyHeightDelta': util.u64_to_dto(self.apply_height_delta),
            'networkConfig': self.network_config,
            'supportedEntityVersions': self.supported_entity_versions,
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        apply_height_delta = util.u64_from_dto(data['applyHeightDelta'])
        network_config = data['networkConfig']
        supported_entity_versions = data['supportedEntityVersions']

        self._set('apply_height_delta', apply_height_delta)
        self._set('network_config', network_config)
        self._set('supported_entity_versions', supported_entity_versions)


@register_transaction('NETWORK_CONFIG')
class NetworkConfigInnerTransaction(InnerTransaction, NetworkConfigTransaction):
    """Embedded network configuration transaction."""

    __slots__ = ()
