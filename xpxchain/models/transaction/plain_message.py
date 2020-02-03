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

from __future__ import annotations
import typing

from .message import Message
from .message_type import MessageType
from ... import util

__all__ = ['PlainMessage']


@util.inherit_doc
class PlainMessage(Message):
    """
    Defines a plain message object. Sent to the network as hex.

    :param payload: Message data, as bytes or hex.
    """

    __slots__ = ()

    def __init__(self, payload: typing.AnyStr) -> None:
        payload = util.decode_hex(payload, with_prefix=True)
        super().__init__(MessageType.PLAIN, payload)

    @classmethod
    def create(cls, payload: typing.AnyStr):
        return cls(payload)  # type: ignore


EMPTY_MESSAGE = PlainMessage(b'')
