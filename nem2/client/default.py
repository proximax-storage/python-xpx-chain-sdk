"""
    default
    =======

    Synchronous and asynchronous NIS client using the default backend.

    The core HTTP client shares a global session, to share a connection
    pool to speed up requests.

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
import aiohttp
import requests
import websockets

from nem2 import util
from . import abc
from . import client

__all__ = [
    # Synchronous
    'Http',
    'AccountHttp',
    'BlockchainHttp',
    'MosaicHttp',
    'NamespaceHttp',
    'NetworkHttp',
    'TransactionHttp',

    # Asynchronous
    'AsyncHttp',
    'AsyncAccountHttp',
    'AsyncBlockchainHttp',
    'AsyncMosaicHttp',
    'AsyncNamespaceHttp',
    'AsyncNetworkHttp',
    'AsyncTransactionHttp',

    # Websockets
    'Listener',

    # Exceptions
    'HTTPError',
    'AsyncHTTPError',
]

# EXCEPTIONS

HTTPError = requests.HTTPError
AsyncHTTPError = aiohttp.ClientResponseError

# SYNCHRONOUS


@util.inherit_doc
class HttpBase(abc.HttpBase):
    """Abstract base class for synchronous HTTP clients."""

    def __init__(self, endpoint: str) -> None:
        self._endpoint = endpoint
        self._index = 0

    def __enter__(self):
        self._client = client.Client(requests.Session(), self._endpoint)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    @property
    def root(self):
        return Http.from_http(self)


@util.inherit_doc
class Http(HttpBase, abc.Http):
    """Main client for the synchronous NIS API."""

    @property
    def account(self) -> AccountHttp:
        return AccountHttp.from_http(self)

    @property
    def blockchain(self) -> BlockchainHttp:
        return BlockchainHttp.from_http(self)

    @property
    def mosaic(self) -> MosaicHttp:
        return MosaicHttp.from_http(self)

    @property
    def namespace(self) -> NamespaceHttp:
        return NamespaceHttp.from_http(self)

    @property
    def network(self) -> NetworkHttp:
        return NetworkHttp.from_http(self)

    @property
    def transaction(self) -> TransactionHttp:
        return TransactionHttp.from_http(self)


@util.inherit_doc
class AccountHttp(HttpBase, abc.AccountHttp):
    """Account client for the synchronous NIS API."""


@util.inherit_doc
class BlockchainHttp(HttpBase, abc.BlockchainHttp):
    """Blockchain client for the synchronous NIS API."""


@util.inherit_doc
class MosaicHttp(HttpBase, abc.MosaicHttp):
    """Mosaic client for the synchronous NIS API."""


@util.inherit_doc
class NamespaceHttp(HttpBase, abc.NamespaceHttp):
    """Namespace client for the synchronous NIS API."""


@util.inherit_doc
class NetworkHttp(HttpBase, abc.NetworkHttp):
    """Network client for the synchronous NIS API."""


@util.inherit_doc
class TransactionHttp(HttpBase, abc.TransactionHttp):
    """Transaction client for the synchronous NIS API."""


# ASYNCHRONOUS


@util.inherit_doc
class AsyncHttpBase(abc.AsyncHttpBase):
    """Abstract base class for synchronous HTTP clients."""

    def __init__(self, endpoint: str, loop: util.OptionalLoopType = None) -> None:
        self._endpoint = endpoint
        self._index = 1
        self._loop = loop
        self._session = aiohttp.ClientSession(loop=loop)

    async def __aenter__(self):
        self._client = client.AsyncClient(self._session, self._endpoint)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    @property
    def root(self):
        return AsyncHttp.from_http(self)


@util.inherit_doc
class AsyncHttp(AsyncHttpBase, abc.Http):
    """Main client for the synchronous NIS API."""

    @property
    def account(self) -> AsyncAccountHttp:
        return AsyncAccountHttp.from_http(self)

    @property
    def blockchain(self) -> AsyncBlockchainHttp:
        return AsyncBlockchainHttp.from_http(self)

    @property
    def mosaic(self) -> AsyncMosaicHttp:
        return AsyncMosaicHttp.from_http(self)

    @property
    def namespace(self) -> AsyncNamespaceHttp:
        return AsyncNamespaceHttp.from_http(self)

    @property
    def network(self) -> AsyncNetworkHttp:
        return AsyncNetworkHttp.from_http(self)

    @property
    def transaction(self) -> AsyncTransactionHttp:
        return AsyncTransactionHttp.from_http(self)


@util.inherit_doc
class AsyncAccountHttp(AsyncHttpBase, abc.AccountHttp):
    """Account client for the asynchronous NIS API."""


@util.inherit_doc
class AsyncBlockchainHttp(AsyncHttpBase, abc.BlockchainHttp):
    """Blockchain client for the asynchronous NIS API."""


@util.inherit_doc
class AsyncMosaicHttp(AsyncHttpBase, abc.MosaicHttp):
    """Mosaic client for the asynchronous NIS API."""


@util.inherit_doc
class AsyncNamespaceHttp(AsyncHttpBase, abc.NamespaceHttp):
    """Namespace client for the asynchronous NIS API."""


@util.inherit_doc
class AsyncNetworkHttp(AsyncHttpBase, abc.NetworkHttp):
    """Network client for the asynchronous NIS API."""


@util.inherit_doc
class AsyncTransactionHttp(AsyncHttpBase, abc.TransactionHttp):
    """Transaction client for the asynchronous NIS API."""


# WEBSOCKETS


@util.inherit_doc
class Listener(abc.Listener):
    """Asynchronous websockets-based listener."""

    def __init__(self, endpoint: str, loop: util.OptionalLoopType = None) -> None:
        url = client.parse_ws_url(endpoint)
        self._loop = loop
        self._conn = websockets.connect(url.url, loop=loop)

    async def __aenter__(self) -> Listener:
        self._session = await self._conn.__aenter__()
        self._client = client.WebsocketClient(self._session)
        self._iter_ = self._client.__aiter__()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self._conn.__aexit__(None, None, None)
