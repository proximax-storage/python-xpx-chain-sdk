"""
    transaction_type
    ================

    Enumerations for transaction types.

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

import enum
import struct
import typing

from nem2 import util


@util.inherit_doc
class TransactionType(util.Catbuffer, util.EnumMixin, enum.IntEnum):
    """Transaction type."""

    TRANSFER = 0x4154
    REGISTER_NAMESPACE = 0x414E
    ADDRESS_ALIAS = 0x424E
    MOSAIC_ALIAS = 0x434E
    MOSAIC_DEFINITION = 0x414D
    MOSAIC_SUPPLY_CHANGE = 0x424D
    MODIFY_MULTISIG_ACCOUNT = 0x4155
    AGGREGATE_COMPLETE = 0x4141
    AGGREGATE_BONDED = 0x4241
    LOCK = 0x4148
    SECRET_LOCK = 0x4152
    SECRET_PROOF = 0x4252
    CATBUFFER_SIZE: typing.ClassVar[int]

    def description(self) -> str:
        return DESCRIPTION[self]

    def to_catbuffer(self) -> bytes:
        return struct.pack('<H', int(self))

    @classmethod
    def from_catbuffer(cls, data: bytes) -> typing.Tuple['TransactionType', bytes]:
        assert len(data) >= cls.CATBUFFER_SIZE
        inst = cls(struct.unpack('<H', data[:cls.CATBUFFER_SIZE])[0])
        return inst, data[cls.CATBUFFER_SIZE:]


TransactionType.CATBUFFER_SIZE = 2

DESCRIPTION = {
    TransactionType.TRANSFER: "Transfer Transaction transaction type.",
    TransactionType.REGISTER_NAMESPACE: "Register namespace transaction type.",
    TransactionType.ADDRESS_ALIAS: "Address alias transaction type.",
    TransactionType.MOSAIC_ALIAS: "Mosaic alias transaction type.",
    TransactionType.MOSAIC_DEFINITION: "Mosaic definition transaction type.",
    TransactionType.MOSAIC_SUPPLY_CHANGE: "Mosaic supply change transaction.",
    TransactionType.MODIFY_MULTISIG_ACCOUNT: "Modify multisig account transaction type.",
    TransactionType.AGGREGATE_COMPLETE: "Aggregate complete transaction type.",
    TransactionType.AGGREGATE_BONDED: "Aggregate bonded transaction type.",
    TransactionType.LOCK: "Lock transaction type.",
    TransactionType.SECRET_LOCK: "Secret Lock Transaction type.",
    TransactionType.SECRET_PROOF: "Secret Proof transaction type.",
}
