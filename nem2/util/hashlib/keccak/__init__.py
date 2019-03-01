"""
    hashlib
    =======

    Keccak (pre-standard SHA3) crytographic hash functions.

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

try:
    from .crypto import keccak_224, keccak_256, keccak_384, keccak_512
except ImportError:
    from .fallback import keccak_224, keccak_256, keccak_384, keccak_512

__all__ = [
    'keccak_224',
    'keccak_256',
    'keccak_384',
    'keccak_512',
]
