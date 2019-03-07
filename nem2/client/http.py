"""
    http
    ====

    Synchronous NIS client.

    The core HTTP client shares a global session, to share a connection
    pool to speed up requests.

    Example
    -------

    .. code-block:: python

       >>> from nem2.client import Http
       >>> http = Http("http://176.9.68.110:7890/")
       >>> http.heartbeat()
       <Heartbeat.OK: 1>

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

__all__ = ['factory']

import typing

from nem2 import models
from nem2 import util
from . import documentation
from . import host
from . import nis


def factory(callback: typing.Callable) -> tuple:
    """Factory to create the synchronous HTTP clients."""

    class HttpBase:
        """Base class for HTTP clients."""

        def __init__(self, endpoint: str) -> None:
            self._host = callback(endpoint)
            self._network_type = None

        @classmethod
        def from_http(cls, http: 'HttpBase') -> 'HttpBase':
            """
            Initialize AsyncHttp directly from existing HTTP client.
            For internal use, do not use directly.

            :param http: HTTP client.
            """
            inst = cls.__new__(cls)
            inst._host = http._host
            inst._network_type = http._network_type
            return inst

        @property
        def network_type(self) -> 'NetworkType':
            """Get network type for client."""
            if self._network_type is None:
                network = NetworkHttp.from_http(self)
                self._network_type = network.get_network_type()
            return self._network_type

        networkType = util.undoc(network_type)


    class Http(HttpBase):
        """Main client for the synchronous NIS API."""

        @util.doc(documentation.INIT)
        def __init__(self, endpoint: str) -> None:
            super().__init__(endpoint)

        @property
        def account(self) -> 'AccountHttp':
            """Get AccountHttp to the same endpoint."""
            return AccountHttp.from_http(self)

        @property
        def blockchain(self) -> 'BlockchainHttp':
            """Get BlockchainHttp to the same endpoint."""
            return BlockchainHttp.from_http(self)

        @property
        def mosaic(self) -> 'MosaicHttp':
            """Get MosaicHttp to the same endpoint."""
            return MosaicHttp.from_http(self)

        @property
        def namespace(self) -> 'NamespaceHttp':
            """Get NamespaceHttp to the same endpoint."""
            return NamespaceHttp.from_http(self)

        @property
        def network(self) -> 'NetworkHttp':
            """Get NetworkHttp to the same endpoint."""
            return NetworkHttp.from_http(self)

        @property
        def transaction(self) -> 'TransactionHttp':
            """Get TransactionHttp to the same endpoint."""
            return TransactionHttp.from_http(self)


    class AccountHttp(HttpBase):
        """Account client for the synchronous NIS API."""

        @util.doc(documentation.INIT)
        def __init__(self, endpoint: str) -> None:
            super().__init__(endpoint)

        #TODO(ahuszagh) Implement...


    class BlockchainHttp(HttpBase):
        """Blockchain client for the synchronous NIS API."""

        @util.doc(documentation.INIT)
        def __init__(self, endpoint: str) -> None:
            super().__init__(endpoint)

        @util.doc(documentation.GET_BLOCK_BY_HEIGHT)
        def get_block_by_height(self, height: int, timeout=None) -> 'BlockInfo':
            return nis.get_block_by_height[0](self._host, height, timeout=timeout)

        getBlockByHeight = util.undoc(get_block_by_height)

        #TODO(ahuszagh) Implement...
        # getBlockByHeight
        # getBlockTransactions
        # getBlocksByHeightWithLimit
        # getBlockchainHeight
        # getBlockchainScore
        # getDiagnosticStorage
        pass


    class MosaicHttp(HttpBase):
        """Mosaic client for the synchronous NIS API."""

        @util.doc(documentation.INIT)
        def __init__(self, endpoint: str) -> None:
            super().__init__(endpoint)


    class NamespaceHttp(HttpBase):
        """Namespace client for the synchronous NIS API."""

        @util.doc(documentation.INIT)
        def __init__(self, endpoint: str) -> None:
            super().__init__(endpoint)

        @util.doc(documentation.GET_NAMESPACE_NAMES)
        def get_namespace_names(self, ids: typing.Sequence['NamespaceId'], timeout=None) -> typing.Sequence['NamespaceName']:
            return nis.get_namespace_names[0](self._host, ids, timeout=timeout)

        getNamespaceNames = util.undoc(get_namespace_names)


    class NetworkHttp(HttpBase):
        """Network client for the synchronous NIS API."""

        @util.doc(documentation.INIT)
        def __init__(self, endpoint: str) -> None:
            super().__init__(endpoint)

        @util.doc(documentation.GET_NETWORK_TYPE)
        def get_network_type(self, timeout=None) -> 'NetworkType':
            return nis.get_network_type[0](self._host, timeout=timeout)

        getNetworkType = util.undoc(get_network_type)


    class TransactionHttp(HttpBase):
        """Transaction client for the synchronous NIS API."""

        @util.doc(documentation.INIT)
        def __init__(self, endpoint: str) -> None:
            super().__init__(endpoint)

    return (
        Http,
        AccountHttp,
        BlockchainHttp,
        MosaicHttp,
        NamespaceHttp,
        NetworkHttp,
        TransactionHttp,
    )
