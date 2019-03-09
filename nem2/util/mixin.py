"""
    mixin
    =====

    Mixins classes.

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

__all__ = [
    'EnumMixin',
    'IntMixin',
]


class EnumMixin:
    """Mixin defining shared methods for enumerations."""

    def description(self) -> str:
        """Describe enumerated values in detail."""
        raise NotImplementedError


class IntMixin:
    """Mixin for classes that can be interpreted as integers."""

    __slots__ = ()

    def __int__(self) -> int:
        raise NotImplementedError

    def __index__(self) -> int:
        return self.__int__()

    def __format__(self, format_spec: str):
        return int(self).__format__(format_spec)

    @classmethod
    def from_hex(cls, data: str):
        """
        Create instance of class from hex string.

        :param data: Hex-encoded ID data (with or without '0x' prefix).
        """
        return cls(int(data, 16))
