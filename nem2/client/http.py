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

from nem2 import models
from nem2 import util
from . import documentation
from . import host
from . import nis


def factory(callback):
    """Factory to create the synchronous HTTP clients."""

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

    class Http(HttpBase):
        """Main client for the synchronous NIS API."""

        def __init__(self, endpoint: str) -> None:
            """
            :param endpoint: Domain name and port for the endpoint.
            """
            super().__init__(endpoint)
            self._account = AccountHttp.from_host(self._host)
            self._blockchain = BlockchainHttp.from_host(self._host)

        @classmethod
        def from_host(cls, host: host.Host) -> 'Http':
            """
            Initialize Http directly from existing host.
            For internal use, do not use directly.

            :param host: Wrapper for the HTTP client.
            """
            http = super(Http, cls).from_host(host)
            http._account = AccountHttp.from_host(http._host)
            http._blockchain = BlockchainHttp.from_host(http._host)
            return http

        @property
        def account(self) -> 'AccountHttp':
            """Get AccountHttp to the same endpoint."""
            return self._account

        @property
        def blockchain(self) -> 'BlockchainHttp':
            """Get BlockchainHttp to the same endpoint."""
            return self._blockchain


    class AccountHttp(HttpBase):
        """Account client for the synchronous NIS API."""

        #TODO(ahuszagh) Implement...


    class BlockchainHttp(HttpBase):
        """Blockchain client for the synchronous NIS API."""

        @util.doc(documentation.GET_BLOCK_BY_HEIGHT)
        def get_block_by_height(self, height: int, timeout=None) -> 'BlockInfo':
            return nis.get_block_by_height(self._host, height, timeout=timeout)

        getBlockByHeight = util.undoc(get_block_by_height)

        #TODO(ahuszagh) Implement...
        # getBlockByHeight
        # getBlockTransactions
        # getBlocksByHeightWithLimit
        # getBlockchainHeight
        # getBlockchainScore
        # getDiagnosticStorage
        pass

    return Http, AccountHttp, BlockchainHttp
