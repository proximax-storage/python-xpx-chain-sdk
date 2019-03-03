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

from nem2 import models
from nem2 import util
from . import documentation
from . import host
from . import nis


def factory(callback):
    """Factory to create the asynchronous HTTP clients."""

    class HttpBase:
        """Base class for HTTP clients."""

        def __init__(self, endpoint: str) -> None:
            """
            :param endpoint: Domain name and port for the endpoint.
            """
            self._host = callback(endpoint)

        @classmethod
        def from_host(cls, host: host.Host):
            """
            Initialize AsyncHttp directly from existing host.
            For internal use, do not use directly.

            :param host: Wrapper for the HTTP client.
            """
            http = cls.__new__(cls)
            http._host = host
            return http

    class AsyncHttp(HttpBase):
        """Main client for the asynchronous NIS API."""

        def __init__(self, endpoint: str) -> None:
            """
            :param endpoint: Domain name and port for the endpoint.
            """
            super().__init__(endpoint)
            self._account = AsyncAccountHttp.from_host(self._host)
            self._blockchain = AsyncBlockchainHttp.from_host(self._host)

        @classmethod
        def from_host(cls, host: host.Host) -> 'AsyncHttp':
            """
            Initialize AsyncHttp directly from existing host.
            For internal use, do not use directly.

            :param host: Wrapper for the HTTP client.
            """
            http = super(AsyncHttp, cls).from_host(host)
            http._account = AsyncAccountHttp.from_host(http._host)
            http._blockchain = AsyncBlockchainHttp.from_host(http._host)
            return http

        @property
        def account(self) -> 'AsyncAccountHttp':
            """Get AsyncAccountHttp to the same endpoint."""
            return self._account

        @property
        def blockchain(self) -> 'AsyncBlockchainHttp':
            """Get AsyncBlockchainHttp to the same endpoint."""
            return self._blockchain


    class AsyncAccountHttp(HttpBase):
        """Account client for the asynchronous NIS API."""

        #TODO(ahuszagh) Implement...


    class AsyncBlockchainHttp(HttpBase):
        """Blockchain client for the asynchronous NIS API."""

        @util.doc(documentation.GET_BLOCK_BY_HEIGHT)
        @util.observable
        async def get_block_by_height(self, height: int, timeout=None) -> 'BlockInfo':
            return await nis.async_get_block_by_height(self._host, height, timeout=timeout)

        #TODO(ahuszagh) Implement...
        # getBlockByHeight
        # getBlockTransactions
        # getBlocksByHeightWithLimit
        # getBlockchainHeight
        # getBlockchainScore
        # getDiagnosticStorage
        pass

    return AsyncHttp, AsyncAccountHttp, AsyncBlockchainHttp
