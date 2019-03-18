"""
    sync_announce
    =============

    Signed transaction to announce and sync to network.

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

from nem2 import util

__all__ = ['SyncAnnounce']


# TODO(ahuszagh) str or bytes??
@util.dataclass(frozen=True)
class SyncAnnounce:
    """
    Signed transaction to announce and sync.

    :param payload: Signed transaction data.
    :param hash: Transaction hash.
    :param address: Transaction address.
    """

    payload: bytes
    hash: bytes
    address: bytes

    # TODO(ahuszagh) Implement
    # from_dto
    # to_dto
