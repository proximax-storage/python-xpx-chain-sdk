"""
    plain_message
    =============

    Plain message, sent to the network as hex-encoded bytes.

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

from nem2 import util
from .message import Message
from .message_type import MessageType


@util.inherit_doc
class PlainMessage(Message):
    """
    Defines a plain message object. Sent to the network as hex.

    :param payload: Message data.
    """

    __slots__ = ()

    def __init__(self, payload: bytes):
        super().__init__(MessageType.PLAIN, payload)

    @classmethod
    def create(cls, payload: bytes) -> 'PlainMessage':
        return cls(payload)

    def to_dto(self) -> str:
        return util.hexlify(self.payload)

    @classmethod
    def from_dto(cls, data: str) -> 'PlainMessage':
        return cls.create(util.unhexlify(data))


EMPTY_MESSAGE = PlainMessage(b'')
