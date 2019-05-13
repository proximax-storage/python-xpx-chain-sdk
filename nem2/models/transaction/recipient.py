"""
    recipient
    =========

    Recipient utilities to handle both addresses and namespace IDs.

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

from ..account.address import Address
from ..blockchain.network_type import NetworkType
from ..namespace.namespace_id import NamespaceId
from ... import util
from ...util import bit

RecipientType = typing.Union[Address, NamespaceId]


class Recipient(util.Object):
    """Wrapper for the recipient DTO and catbuffer objects."""

    CATBUFFER_SIZE: typing.ClassVar[int] = 25

    @staticmethod
    def to_dto(
        obj: RecipientType,
        network_type: NetworkType,
    ) -> str:
        return util.hexlify(Recipient.to_catbuffer(obj, network_type))

    @staticmethod
    def create_from_dto(
        data: str,
        network_type: NetworkType,
    ) -> RecipientType:
        return Recipient.create_from_catbuffer(util.unhexlify(data), network_type)

    @staticmethod
    def to_catbuffer(
        obj: RecipientType,
        network_type: NetworkType,
    ) -> bytes:
        if isinstance(obj, Address):
            # The first byte is always the network type.
            return obj.encoded
        # The first byte is always the network type + 1.
        leading = util.u8_to_catbuffer(int(network_type) + 1)
        trailing = bytes(16)
        return leading + util.unhexlify(obj.encoded) + trailing

    @staticmethod
    def create_from_catbuffer(
        data: bytes,
        network_type: NetworkType,
    ) -> RecipientType:
        # For addresses, the first byte is the network type,
        # which are always even. If it's odd, we have a namespace ID.
        # Otherwise, for the namespace ID, the first byte is a sentinel,
        # and the next 8 bytes are the relevant data.
        # The first byte without the first bit is always the network type.
        assert bit.clear(data[0], 0) == int(network_type)
        if bit.get(data[0], 0) == 0:
            return typing.cast(Address, Address.create_from_encoded(data[:25]))
        return typing.cast(NamespaceId, NamespaceId.create_from_encoded(data[1:9]))

    @staticmethod
    def create_from_catbuffer_pair(
        data: bytes,
        network_type: NetworkType,
    ) -> typing.Tuple[RecipientType, bytes]:
        size = Recipient.CATBUFFER_SIZE
        inst = Recipient.create_from_catbuffer(data, network_type)
        return inst, data[size:]
