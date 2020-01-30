"""
    sha3
    ====

    Python wrappers for the ed25519-sha3 elliptical curve algorithm.

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

try:
    from ed25519sha3 import (
        BadSignatureError,
        SigningKey,
        VerifyingKey,
        create_keypair
    )
except ImportError:
    from xpxchain.util import hashlib
    from . import fallback

    def hash512(data: bytes):
        return hashlib.sha3_512(data).digest()

    (
        BadSignatureError,
        SigningKey,
        VerifyingKey,
        create_keypair
    ) = fallback.generate_api(hash512)
