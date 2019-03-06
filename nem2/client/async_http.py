"""
    async_http
    ==========

    Asynchronous NIS client.

    The core HTTP client shares a global session, to share a connection
    pool to speed up requests.

    Example
    -------

    .. code-block:: python

       >>> from nem2.client import AsyncHttp
       >>> import asyncio
       >>> loop = asyncio.get_event_loop()
       >>> http = AsyncHttp("http://176.9.68.110:7890/")
       >>> loop.run_until_complete(http.heartbeat())
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

import typing

from nem2 import models
from nem2 import util
from . import documentation
from . import host
from . import nis


def factory(callback: typing.Callable) -> tuple:
    """Factory to create the asynchronous HTTP clients."""

    class HttpBase:
        """Base class for HTTP clients."""

        def __init__(self, endpoint: str, loop: util.OptionalLoopType = None) -> None:
            self._loop = loop
            self._host = callback(endpoint, loop)
            self._network_type = None

        @classmethod
        def from_http(cls, http: 'HttpBase') -> 'HttpBase':
            """
            Initialize AsyncHttp directly from existing HTTP client.
            For internal use, do not use directly.

            :param http: HTTP client.
            """
            inst = cls.__new__(cls)
            inst._loop = http._loop
            inst._host = http._host
            inst._network_type = http._network_type
            return inst

        @property
        def loop(self):
            """Get event loop."""
            return self._loop

        @property
        async def network_type(self) -> 'NetworkType':
            """Get network type for client."""
            if self._network_type is None:
                network = AsyncNetworkHttp.from_http(self)
                self._network_type = await network.get_network_type()
            return self._network_type


    class AsyncHttp(HttpBase):
        """Main client for the asynchronous NIS API."""

        @util.doc(documentation.ASYNC_INIT)
        def __init__(self, endpoint: str, loop: util.OptionalLoopType = None) -> None:
            super().__init__(endpoint, loop=loop)

        @property
        def account(self) -> 'AsyncAccountHttp':
            """Get AsyncAccountHttp to the same endpoint."""
            return AsyncAccountHttp.from_http(self)

        @property
        def blockchain(self) -> 'AsyncBlockchainHttp':
            """Get AsyncBlockchainHttp to the same endpoint."""
            return AsyncBlockchainHttp.from_http(self)

        @property
        def mosaic(self) -> 'AsyncMosaicHttp':
            """Get AsyncMosaicHttp to the same endpoint."""
            return AsyncMosaicHttp.from_http(self)

        @property
        def namespace(self) -> 'AsyncNamespaceHttp':
            """Get AsyncNamespaceHttp to the same endpoint."""
            return AsyncNamespaceHttp.from_http(self)

        @property
        def network(self) -> 'AsyncNetworkHttp':
            """Get AsyncNetworkHttp to the same endpoint."""
            return AsyncNetworkHttp.from_http(self)

        @property
        def transaction(self) -> 'AsyncTransactionHttp':
            """Get AsyncTransactionHttp to the same endpoint."""
            return AsyncTransactionHttp.from_http(self)


    class AsyncAccountHttp(HttpBase):
        """Account client for the asynchronous NIS API."""

        @util.doc(documentation.ASYNC_INIT)
        def __init__(self, endpoint: str, loop: util.OptionalLoopType = None) -> None:
            super().__init__(endpoint, loop=loop)

        #TODO(ahuszagh) Implement...


    class AsyncBlockchainHttp(HttpBase):
        """Blockchain client for the asynchronous NIS API."""

        @util.doc(documentation.ASYNC_INIT)
        def __init__(self, endpoint: str, loop: util.OptionalLoopType = None) -> None:
            super().__init__(endpoint, loop=loop)

        @util.doc(documentation.GET_BLOCK_BY_HEIGHT)
        @util.observable
        async def get_block_by_height(self, height: int, timeout=None) -> 'BlockInfo':
            return await nis.get_block_by_height[1](self._host, height, timeout=timeout)

        #TODO(ahuszagh) Implement...
        # getBlockByHeight
        # getBlockTransactions
        # getBlocksByHeightWithLimit
        # getBlockchainHeight
        # getBlockchainScore
        # getDiagnosticStorage
        pass


    class AsyncMosaicHttp(HttpBase):
        """Mosaic client for the asynchronous NIS API."""

        @util.doc(documentation.ASYNC_INIT)
        def __init__(self, endpoint: str, loop: util.OptionalLoopType = None) -> None:
            super().__init__(endpoint, loop=loop)


    class AsyncNamespaceHttp(HttpBase):
        """Namespace client for the asynchronous NIS API."""

        @util.doc(documentation.ASYNC_INIT)
        def __init__(self, endpoint: str, loop: util.OptionalLoopType = None) -> None:
            super().__init__(endpoint, loop=loop)


    class AsyncNetworkHttp(HttpBase):
        """Network client for the asynchronous NIS API."""

        @util.doc(documentation.ASYNC_INIT)
        def __init__(self, endpoint: str, loop: util.OptionalLoopType = None) -> None:
            super().__init__(endpoint, loop=loop)

        @util.doc(documentation.GET_NETWORK_TYPE)
        @util.observable
        async def get_network_type(self, timeout=None) -> 'NetworkType':
            return await nis.get_network_type[1](self._host, timeout=timeout)

        getNetworkType = util.undoc(get_network_type)


    class AsyncTransactionHttp(HttpBase):
        """Transaction client for the asynchronous NIS API."""

        @util.doc(documentation.ASYNC_INIT)
        def __init__(self, endpoint: str, loop: util.OptionalLoopType = None) -> None:
            super().__init__(endpoint, loop=loop)


    return (
        AsyncHttp,
        AsyncAccountHttp,
        AsyncBlockchainHttp,
        AsyncMosaicHttp,
        AsyncNamespaceHttp,
        AsyncNetworkHttp,
        AsyncTransactionHttp,
    )
