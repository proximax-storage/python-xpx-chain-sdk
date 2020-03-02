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
import typing

from . import abc
from . import client
from .. import util
from ..models.blockchain.network_type import NetworkType

__all__ = [
    # Synchronous
    'HTTP',
    'AccountHTTP',
    'BlockchainHTTP',
    'ContractHTTP',
    'MetadataHTTP',
    'ConfigHTTP',
    'NodeHTTP',
    'MosaicHTTP',
    'NamespaceHTTP',
    'NetworkHTTP',
    'TransactionHTTP',

    # Asynchronous
    'AsyncHTTP',
    'AsyncAccountHTTP',
    'AsyncBlockchainHTTP',
    'AsyncContractHTTP',
    'AsyncMetadataHTTP',
    'AsyncConfigHTTP',
    'AsyncNodeHTTP',
    'AsyncMosaicHTTP',
    'AsyncNamespaceHTTP',
    'AsyncNetworkHTTP',
    'AsyncTransactionHTTP',

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
class HTTPBase(abc.HTTPBase):
    """Abstract base class for synchronous HTTP clients."""

    def __init__(self, endpoint: str, network_type: typing.Optional[NetworkType] = None) -> None:
        self._endpoint = endpoint
        self._index = 0
        self._network_type = network_type

    def __enter__(self) -> HTTPBase:
        self._client = client.Client(requests.Session(), self._endpoint)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    @property
    def root(self) -> HTTP:
        return HTTP.create_from_http(self)


@util.inherit_doc
class HTTP(HTTPBase, abc.HTTP):
    """Main client for the synchronous NIS API."""

    @property
    def account(self) -> AccountHTTP:
        return AccountHTTP.create_from_http(self)

    @property
    def blockchain(self) -> BlockchainHTTP:
        return BlockchainHTTP.create_from_http(self)

    @property
    def contract(self) -> ContractHTTP:
        return ContractHTTP.create_from_http(self)

    @property
    def metadata(self) -> MetadataHTTP:
        return MetadataHTTP.create_from_http(self)

    @property
    def config(self) -> ConfigHTTP:
        return ConfigHTTP.create_from_http(self)

    @property
    def node(self) -> NodeHTTP:
        return NodeHTTP.create_from_http(self)

    @property
    def mosaic(self) -> MosaicHTTP:
        return MosaicHTTP.create_from_http(self)

    @property
    def namespace(self) -> NamespaceHTTP:
        return NamespaceHTTP.create_from_http(self)

    @property
    def network(self) -> NetworkHTTP:
        return NetworkHTTP.create_from_http(self)

    @property
    def transaction(self) -> TransactionHTTP:
        return TransactionHTTP.create_from_http(self)


@util.inherit_doc
class AccountHTTP(HTTPBase, abc.AccountHTTP):
    """Account client for the synchronous NIS API."""


@util.inherit_doc
class BlockchainHTTP(HTTPBase, abc.BlockchainHTTP):
    """Blockchain client for the synchronous NIS API."""


@util.inherit_doc
class ContractHTTP(HTTPBase, abc.ContractHTTP):
    """Contract client for the synchronous NIS API."""


@util.inherit_doc
class MetadataHTTP(HTTPBase, abc.MetadataHTTP):
    """Metadata client for the synchronous NIS API."""


@util.inherit_doc
class ConfigHTTP(HTTPBase, abc.ConfigHTTP):
    """Config client for the synchronous NIS API."""


@util.inherit_doc
class NodeHTTP(HTTPBase, abc.NodeHTTP):
    """Node client for the synchronous NIS API."""


@util.inherit_doc
class MosaicHTTP(HTTPBase, abc.MosaicHTTP):
    """Mosaic client for the synchronous NIS API."""


@util.inherit_doc
class NamespaceHTTP(HTTPBase, abc.NamespaceHTTP):
    """Namespace client for the synchronous NIS API."""


@util.inherit_doc
class NetworkHTTP(HTTPBase, abc.NetworkHTTP):
    """Network client for the synchronous NIS API."""


@util.inherit_doc
class TransactionHTTP(HTTPBase, abc.TransactionHTTP):
    """Transaction client for the synchronous NIS API."""


# ASYNCHRONOUS


@util.inherit_doc
class AsyncHTTPBase(abc.AsyncHTTPBase):
    """Abstract base class for synchronous HTTP clients."""

    def __init__(
        self,
        endpoint: str,
        loop: util.OptionalLoopType = None,
        network_type: typing.Optional[NetworkType] = None,
    ) -> None:
        self._endpoint = endpoint
        self._index = 1
        self._loop = loop
        self._session = aiohttp.ClientSession(loop=loop)
        self._network_type = network_type

    async def __aenter__(self) -> AsyncHTTPBase:
        self._client = client.AsyncClient(self._session, self._endpoint)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    @property
    def root(self) -> AsyncHTTP:
        return AsyncHTTP.create_from_http(self)


@util.inherit_doc
class AsyncHTTP(AsyncHTTPBase, abc.HTTP):
    """Main client for the synchronous NIS API."""

    @property
    def account(self) -> AsyncAccountHTTP:
        return AsyncAccountHTTP.create_from_http(self)

    @property
    def blockchain(self) -> AsyncBlockchainHTTP:
        return AsyncBlockchainHTTP.create_from_http(self)

    @property
    def contract(self) -> AsyncContractHTTP:
        return AsyncContractHTTP.create_from_http(self)

    @property
    def metadata(self) -> AsyncMetadataHTTP:
        return AsyncMetadataHTTP.create_from_http(self)

    @property
    def config(self) -> AsyncConfigHTTP:
        return AsyncConfigHTTP.create_from_http(self)

    @property
    def node(self) -> AsyncNodeHTTP:
        return AsyncNodeHTTP.create_from_http(self)

    @property
    def mosaic(self) -> AsyncMosaicHTTP:
        return AsyncMosaicHTTP.create_from_http(self)

    @property
    def namespace(self) -> AsyncNamespaceHTTP:
        return AsyncNamespaceHTTP.create_from_http(self)

    @property
    def network(self) -> AsyncNetworkHTTP:
        return AsyncNetworkHTTP.create_from_http(self)

    @property
    def transaction(self) -> AsyncTransactionHTTP:
        return AsyncTransactionHTTP.create_from_http(self)


@util.inherit_doc
class AsyncAccountHTTP(AsyncHTTPBase, abc.AccountHTTP):
    """Account client for the asynchronous NIS API."""


@util.inherit_doc
class AsyncBlockchainHTTP(AsyncHTTPBase, abc.BlockchainHTTP):
    """Blockchain client for the asynchronous NIS API."""


@util.inherit_doc
class AsyncContractHTTP(AsyncHTTPBase, abc.ContractHTTP):
    """Contract client for the asynchronous NIS API."""


@util.inherit_doc
class AsyncMetadataHTTP(AsyncHTTPBase, abc.MetadataHTTP):
    """Metadata client for the asynchronous NIS API."""


@util.inherit_doc
class AsyncConfigHTTP(AsyncHTTPBase, abc.ConfigHTTP):
    """Config client for the asynchronous NIS API."""


@util.inherit_doc
class AsyncNodeHTTP(AsyncHTTPBase, abc.NodeHTTP):
    """Node client for the asynchronous NIS API."""


@util.inherit_doc
class AsyncMosaicHTTP(AsyncHTTPBase, abc.MosaicHTTP):
    """Mosaic client for the asynchronous NIS API."""


@util.inherit_doc
class AsyncNamespaceHTTP(AsyncHTTPBase, abc.NamespaceHTTP):
    """Namespace client for the asynchronous NIS API."""


@util.inherit_doc
class AsyncNetworkHTTP(AsyncHTTPBase, abc.NetworkHTTP):
    """Network client for the asynchronous NIS API."""


@util.inherit_doc
class AsyncTransactionHTTP(AsyncHTTPBase, abc.TransactionHTTP):
    """Transaction client for the asynchronous NIS API."""


# WEBSOCKETS


@util.inherit_doc
class Listener(abc.Listener):
    """Asynchronous websockets-based listener."""

    def __init__(
        self,
        endpoint: str,
        loop: util.OptionalLoopType = None,
        network_type: typing.Optional[NetworkType] = None,
    ) -> None:
        url = client.parse_ws_url(endpoint)
        self._loop = loop
        self._conn = websockets.connect(url.url, loop=loop)
        self._network_type = network_type

    async def __aenter__(self) -> Listener:
        self._session = await self._conn.__aenter__()
        self._client = client.WebsocketClient(self._session)
        self._iter_ = self._client.__aiter__()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self._conn.__aexit__(None, None, None)
