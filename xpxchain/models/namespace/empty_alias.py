"""
    empty_alias
    ===========

    Empty alias without data.

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

from .alias import Alias, dto_to_kwds
from .alias_type import AliasType
from ..blockchain.network_type import OptionalNetworkType

__all__ = ['EmptyAlias']


class EmptyAlias(Alias):
    """Empty alias without data."""

    __slots__ = ()

    def __init__(self, value: None = None) -> None:
        super().__init__(AliasType.NONE, value)

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        kwds = dto_to_kwds(data, network_type)
        if kwds.pop('type') != AliasType.NONE:
            raise ValueError('Alias type is not a none.')
        return cls(**kwds)
