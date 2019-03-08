"""
    async_http
    ==========

    Asynchronous NIS client.

    The core HTTP client shares a global session, to share a connection
    pool to speed up requests.

    Example:
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

from nem2 import util
from . import documentation
from . import nis

if typing.TYPE_CHECKING:
    from nem2.models import *


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

        networkType = util.undoc(network_type)

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

        # TODO(ahuszagh)
        # getAccountInfo
        # getAccountsInfo
        # getMultisigAccountInfo
        # getMultisigAccountGraphInfo
        # transactions
        # incomingTransactions
        # outgoingTransactions
        # unconfirmedTransactions
        # aggregateBondedTransactions

    class AsyncBlockchainHttp(HttpBase):
        """Blockchain client for the asynchronous NIS API."""

        @util.doc(documentation.ASYNC_INIT)
        def __init__(self, endpoint: str, loop: util.OptionalLoopType = None) -> None:
            super().__init__(endpoint, loop=loop)

        @util.doc(documentation.GET_BLOCK_BY_HEIGHT)
        @util.observable
        async def get_block_by_height(self, height: int, timeout=None) -> 'BlockInfo':
            return await nis.get_block_by_height[1](self._host, height, timeout=timeout)

        getBlockByHeight = util.undoc(get_block_by_height)

        # TODO(ahuszagh)
        # getBlockTransactions
        # getBlocksByHeightWithLimit

        @util.doc(documentation.GET_BLOCKCHAIN_HEIGHT)
        @util.observable
        async def get_blockchain_height(self, timeout=None) -> int:
            return await nis.get_blockchain_height[1](self._host, timeout=timeout)

        getBlockchainHeight = util.undoc(get_blockchain_height)

        @util.doc(documentation.GET_BLOCKCHAIN_SCORE)
        @util.observable
        async def get_blockchain_score(self, timeout=None) -> 'BlockchainScore':
            return await nis.get_blockchain_score[1](self._host, timeout=timeout)

        getBlockchainScore = util.undoc(get_blockchain_score)

        @util.doc(documentation.GET_DIAGNOSTIC_STORAGE)
        @util.observable
        async def get_diagnostic_storage(self, timeout=None) -> 'BlockchainStorageInfo':
            return await nis.get_diagnostic_storage[1](self._host, timeout=timeout)

        getDiagnosticStorage = util.undoc(get_diagnostic_storage)

    class AsyncMosaicHttp(HttpBase):
        """Mosaic client for the asynchronous NIS API."""

        @util.doc(documentation.ASYNC_INIT)
        def __init__(self, endpoint: str, loop: util.OptionalLoopType = None) -> None:
            super().__init__(endpoint, loop=loop)

        @util.doc(documentation.GET_MOSAIC_NAMES)
        @util.observable
        async def get_mosaic_names(self, ids: typing.Sequence['MosaicId'], timeout=None) -> typing.Sequence['MosaicName']:
            return await nis.get_mosaic_names[1](self._host, ids, timeout=timeout)

        getMosaicNames = util.undoc(get_mosaic_names)

        # TODO(ahuszagh)
        # getMosaic
        # getMosaics

    class AsyncNamespaceHttp(HttpBase):
        """Namespace client for the asynchronous NIS API."""

        @util.doc(documentation.ASYNC_INIT)
        def __init__(self, endpoint: str, loop: util.OptionalLoopType = None) -> None:
            super().__init__(endpoint, loop=loop)

        @util.doc(documentation.GET_NAMESPACE)
        @util.observable
        async def get_namespace(self, namespace_id: 'NamespaceId', timeout=None) -> 'NamespaceInfo':
            return await nis.get_namespace[1](self._host, namespace_id, timeout=timeout)

        getNamespace = util.undoc(get_namespace)

        @util.doc(documentation.GET_NAMESPACES_FROM_ACCOUNT)
        @util.observable
        async def get_namespaces_from_account(self, address: 'Address', timeout=None) -> typing.Sequence['NamespaceInfo']:
            return await nis.get_namespaces_from_account[1](self._host, address, timeout=timeout)

        getNamespacesFromAccount = util.undoc(get_namespaces_from_account)

        @util.doc(documentation.GET_NAMESPACES_FROM_ACCOUNTS)
        @util.observable
        async def get_namespaces_from_accounts(self, addresses: typing.Sequence['Address'], timeout=None) -> typing.Sequence['NamespaceInfo']:
            return await nis.get_namespaces_from_accounts[1](self._host, addresses, timeout=timeout)

        getNamespacesFromAccounts = util.undoc(get_namespaces_from_accounts)

        @util.doc(documentation.GET_NAMESPACE_NAMES)
        @util.observable
        async def get_namespace_names(self, ids: typing.Sequence['NamespaceId'], timeout=None) -> typing.Sequence['NamespaceName']:
            return await nis.get_namespace_names[1](self._host, ids, timeout=timeout)

        getNamespaceNames = util.undoc(get_namespace_names)

        @util.doc(documentation.GET_LINKED_MOSAIC_ID)
        @util.observable
        async def get_linked_mosaic_id(self, namespace_id: 'NamespaceId', timeout=None) -> 'MosaicId':
            return await nis.get_linked_mosaic_id[1](self._host, namespace_id, timeout=timeout)

        getLinkedMosaicId = util.undoc(get_linked_mosaic_id)

        @util.doc(documentation.GET_LINKED_ADDRESS)
        @util.observable
        async def get_linked_address(self, namespace_id: 'NamespaceId', timeout=None) -> 'Address':
            return await nis.get_linked_address[1](self._host, namespace_id, timeout=timeout)

        getLinkedAddress = util.undoc(get_linked_address)

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

        # TODO(ahuszagh)
        # getTransaction
        # getTransactions
        # getTransactionStatus
        # getTransactionsStatuses
        # announce
        # announceAggregateBonded
        # announceAggregateBondedCosignature
        # announceSync

    return (
        AsyncHttp,
        AsyncAccountHttp,
        AsyncBlockchainHttp,
        AsyncMosaicHttp,
        AsyncNamespaceHttp,
        AsyncNetworkHttp,
        AsyncTransactionHttp,
    )
