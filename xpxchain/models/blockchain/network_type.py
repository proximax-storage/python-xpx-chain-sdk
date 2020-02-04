"""
    network_type
    ============

    Constants for the network type.

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
import enum
import typing

from ... import util


__all__ = ['NetworkType']


@util.inherit_doc
class NetworkType(util.U8Mixin, util.EnumMixin, enum.IntEnum):
    """
    Identifier for the network type.

    DTO Format:
        .. code-block:: yaml

            NetworkTypeDTO:
                name: string
                description: string
    """

    MAIN_NET   = 0xb8       # noqa: E221
    TEST_NET   = 0xa8       # noqa: E221
    MIJIN      = 0x60       # noqa: E221
    MIJIN_TEST = 0x90       # noqa: E221

    def description(self) -> str:
        return DESCRIPTION[self]

    def identifier(self) -> bytes:
        """Get address identifier from type."""
        return TO_IDENTIFIER[self]

    @classmethod
    def create_from_identifier(cls, identifier: bytes):
        """
        Identify and create the network type from the raw address identifier.

        :param identifier: First character of the raw address.
        """

        assert len(identifier) == 1
        return FROM_IDENTIFIER[identifier]

    @classmethod
    def create_from_raw_address(cls, address: str):
        """
        Identify and create the network type from the raw address.

        :param address: Base32-decoded, upper-case, stripped address.
        """

        assert len(address) == 40
        return cls.create_from_identifier(address[0].encode('ascii'))


DESCRIPTION = {
    NetworkType.MAIN_NET: "Main network",
    NetworkType.TEST_NET: "Test network",
    NetworkType.MIJIN: "Mijin network",
    NetworkType.MIJIN_TEST: "Mijin test network",
}

TO_IDENTIFIER = {
    NetworkType.MAIN_NET: b"X",
    NetworkType.TEST_NET: b"V",
    NetworkType.MIJIN: b"M",
    NetworkType.MIJIN_TEST: b"S",
}

FROM_IDENTIFIER = {
    b"X": NetworkType.MAIN_NET,
    b"V": NetworkType.TEST_NET,
    b"M": NetworkType.MIJIN,
    b"S": NetworkType.MIJIN_TEST,
}

OptionalNetworkType = typing.Optional[NetworkType]
