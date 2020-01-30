"""
    hash_type
    =========

    Validators for hashes.

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
import string

from ... import util

__all__ = ['HashType']


class HashType(util.U8Mixin, util.EnumMixin, enum.IntEnum):
    """Enumerations for support hash types."""

    SHA3_256 = 0
    KECCAK_256 = 1
    HASH_160 = 2
    HASH_256 = 3

    def description(self) -> str:
        return DESCRIPTION[self]

    def hash_length(self) -> int:
        """Calculate the expected hash length."""
        return LENGTH[self]

    def validate(self, input: str) -> bool:
        """
        Validate hex-encoded hash as type.

        :param input: Hex-encoded hash data.
        """
        if all(i in string.hexdigits for i in input):
            return self.hash_length() == len(input)
        return False


DESCRIPTION = {
    HashType.SHA3_256: "SHA3-256 (default).",
    HashType.KECCAK_256: "Keccak-256 (ETH compatibility).",
    HashType.HASH_160: "SHA3-256 to RIPEMD-160 (BTC compatibility).",
    HashType.HASH_256: "SHA3-256 to SHA3-256 (BTC compatibility).",
}

LENGTH = {
    HashType.SHA3_256: 64,
    HashType.KECCAK_256: 64,
    HashType.HASH_160: 40,
    HashType.HASH_256: 64,
}
