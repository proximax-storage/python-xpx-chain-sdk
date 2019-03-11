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

import asyncio
import atexit
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

SYNC_SESSION = requests.Session()
atexit.register(SYNC_SESSION.close)


@util.inherit_doc
class HttpBase(abc.HttpBase):
    """Abstract base class for synchronous HTTP clients."""

    def __init__(self, endpoint: str) -> None:
        self._client = client.Client(SYNC_SESSION, endpoint)
        self._index = 0

    @property
    def root(self):
        return Http.from_http(self)


@util.inherit_doc
class Http(HttpBase, abc.Http):
    """Main client for the synchronous NIS API."""

    @property
    def account(self) -> 'AccountHttp':
        return AccountHttp.from_http(self)

    @property
    def blockchain(self) -> 'BlockchainHttp':
        return BlockchainHttp.from_http(self)

    @property
    def mosaic(self) -> 'MosaicHttp':
        return MosaicHttp.from_http(self)

    @property
    def namespace(self) -> 'NamespaceHttp':
        return NamespaceHttp.from_http(self)

    @property
    def network(self) -> 'NetworkHttp':
        return NetworkHttp.from_http(self)

    @property
    def transaction(self) -> 'TransactionHttp':
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

ASYNC_SESSION = aiohttp.ClientSession()


@atexit.register
def close_sessions() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ASYNC_SESSION.close())


@util.inherit_doc
class AsyncHttpBase(abc.AsyncHttpBase):
    """Abstract base class for synchronous HTTP clients."""

    def __init__(self, endpoint: str, loop: util.OptionalLoopType = None) -> None:
        self._index = 1
        self._loop = loop
        if loop is None:
            self._client = client.AsyncClient(ASYNC_SESSION, endpoint)
        else:
            session = aiohttp.ClientSession(loop=loop)
            self._client = client.AsyncClient(session, endpoint, loop=loop)

    @property
    def root(self):
        return AsyncHttp.from_http(self)


@util.inherit_doc
class AsyncHttp(AsyncHttpBase, abc.Http):
    """Main client for the synchronous NIS API."""

    @property
    def account(self) -> 'AsyncAccountHttp':
        return AsyncAccountHttp.from_http(self)

    @property
    def blockchain(self) -> 'AsyncBlockchainHttp':
        return AsyncBlockchainHttp.from_http(self)

    @property
    def mosaic(self) -> 'AsyncMosaicHttp':
        return AsyncMosaicHttp.from_http(self)

    @property
    def namespace(self) -> 'AsyncNamespaceHttp':
        return AsyncNamespaceHttp.from_http(self)

    @property
    def network(self) -> 'AsyncNetworkHttp':
        return AsyncNetworkHttp.from_http(self)

    @property
    def transaction(self) -> 'AsyncTransactionHttp':
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
        self._loop = loop
        url = client.parse_ws_url(endpoint)
        session = websockets.WebSocketClientProtocol(
            host=url.host,
            port=url.port,
            loop=loop,
            secure=url.scheme == 'wss',
        )
        session.path = url.path or '/'
        self._client = client.WebsocketClient(session, loop=loop)
