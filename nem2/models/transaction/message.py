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

from nem2 import util
from .message_type import MessageType


@util.dataclass(frozen=True)
class Message(util.DTO):
    """
    Abstract message type.

    :param type: Message type.
    :param payload: Message data, in bytes.
    """

    type: MessageType
    payload: bytes

    @classmethod
    def create(cls, data: typing.AnyStr) -> Message:
        """Create a message from raw bytes."""
        raise NotImplementedError
