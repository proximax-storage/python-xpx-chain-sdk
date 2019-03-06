"""
    namespace_name
    ==============

    Describes a namespace by name and identifier.

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

from nem2 import util
from .namespace_id import NamespaceId


class NamespaceName(util.Tie):
    """Namespace name and identifier."""

    __slots__ = (
        '_namespace_id',
        '_name',
    )

    def __init__(self, namespace_id: 'NamespaceId', name: str):
        """
        :param namespace_id: Namespace ID.
        :param name: Namespace name.
        """
        self._namespace_id = namespace_id
        self._name = name

    @property
    def namespace_id(self):
        """Get the namespace ID."""
        return self._namespace_id

    @property
    def name(self):
        """Get the namespace name."""
        return self._name

    @util.doc(util.Tie.tie)
    def tie(self) -> tuple:
        return super().tie()
