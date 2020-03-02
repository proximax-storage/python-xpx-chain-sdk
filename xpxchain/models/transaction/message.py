"""
    message
    =======

    Abstract message class as base for message types.

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

from .message_type import MessageType
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['Message']


@util.dataclass(frozen=True)
class Message(util.Model):
    """
    Abstract message type.

    :param type: Message type.
    :param payload: Message data, in bytes.
    """

    type: MessageType
    payload: bytes

    @classmethod
    def create(cls, data: typing.AnyStr):
        """Create a message from raw bytes."""
        raise util.AbstractMethodError

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'type', 'payload'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'type': self.type.to_dto(network_type),
            'payload': util.hexlify(self.payload),
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        payload = util.unhexlify(data['payload'])
        return cls.create(payload)

    def to_catbuffer(
        self,
        network_type: OptionalNetworkType = None,
        fee_strategy: util.FeeCalculationStrategy = util.FeeCalculationStrategy.MEDIUM,
    ) -> bytes:
        return util.u8_to_catbuffer(self.type) + self.payload

    @classmethod
    def create_from_catbuffer_pair(
        cls,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ):
        return cls.create(data[1:]), data[len(data):]

    def catbuffer_size_specific(self) -> int:
        return util.U8_BYTES + len(self.payload)
