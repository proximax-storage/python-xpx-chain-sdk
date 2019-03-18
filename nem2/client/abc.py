"""
    abc
    ===

    Abstract base classes for HTTP and websocket clients.

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
import json
import typing

from nem2 import models
from nem2 import util
from . import client
from . import nis

T = typing.TypeVar('T')
MessageType = typing.Union[
    models.BlockInfo,
    models.CosignatureSignedTransaction,
    models.TransactionStatusError,
    str
]

# HTTP
# ----


class HTTPSharedBase:
    """Shared, abstract base class for sync and async HTTP clients."""

    _endpoint: str
    _client: client.ClientSharedBase
    _index: int
    _network_type: typing.Optional[models.NetworkType] = None

    @property
    def index(self) -> int:
        """Get index for NIS callbacks."""
        return self._index

    @property
    def raw(self) -> client.ClientSharedBase:
        """Get client wrapper for HTTP client."""
        raise util.AbstractMethodError

    @property
    def root(self) -> HTTP:
        """Get HTTP to the same endpoint."""
        raise util.AbstractMethodError

    @property
    def network_type(self):
        """Get network type for client."""
        raise util.AbstractMethodError

    @property
    def networkType(self):
        return self.network_type

    @classmethod
    def from_http(cls: typing.Type[T], http) -> T:
        """
        Initialize HTTPBase directly from existing HTTP client.
        For internal use, do not use directly.

        :param http: HTTP client.
        """
        inst = cls.__new__(cls)
        inst._client = http._client
        inst._index = http._index
        inst._network_type = http._network_type
        return typing.cast(T, inst)

    def close(self):
        """Close the client session."""
        raise util.AbstractMethodError

    def __call__(self, cbs, *args, **kwds):
        """Invoke the NIS callback."""
        cb = cbs[self.index]
        # Force self.network_type to be executed on a different logical
        # block. Otherwise, we lead to infinite recursion when calling
        # get_network_type().
        try:
            network_type = kwds.pop('network_type')
        except KeyError:
            network_type = self.network_type
        return typing.cast(T, cb(self.raw, network_type, *args, **kwds))

    @property
    def _none(self):
        """Generate `None` with same evaluation as `network_type`."""
        raise util.AbstractMethodError


@util.inherit_doc
class HTTPBase(HTTPSharedBase):
    """Abstract base class for HTTP clients."""

    def __enter__(self) -> HTTPBase:
        raise util.AbstractMethodError

    def __exit__(self, exc_type, exc, tb) -> None:
        raise util.AbstractMethodError

    def close(self) -> None:
        self.raw.close()

    @property
    def raw(self) -> client.Client:
        try:
            return typing.cast(client.Client, self._client)
        except AttributeError:
            raise RuntimeError('Must be used inside `with` block.')

    @property
    def network_type(self) -> models.NetworkType:
        if self._network_type is None:
            network = self.root.network
            self._network_type = network.get_network_type()
        return self._network_type

    @property
    def _none(self) -> None:
        return None


@util.inherit_doc
class AsyncHTTPBase(HTTPSharedBase):
    """
    Abstract base class for asynchronous HTTP clients.

    :param endpoint: Domain name and port for the endpoint.
    :param loop: (Optional) Event loop for the client.
    """

    _loop: util.OptionalLoopType

    def __enter__(self) -> AsyncHTTPBase:
        raise TypeError("Only use async with.")

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    async def __aenter__(self) -> AsyncHTTPBase:
        raise util.AbstractMethodError

    async def __aexit__(self, exc_type, exc, tb) -> None:
        raise util.AbstractMethodError

    async def close(self) -> None:
        await self.raw.close()

    @property
    def raw(self) -> client.AsyncClient:
        try:
            return typing.cast(client.AsyncClient, self._client)
        except AttributeError:
            raise RuntimeError('Must be used inside `async with` block.')

    def __call__(self, cbs, *args, **kwds):
        return self.call(cbs, *args, **kwds)

    @util.observable
    async def call(self, cbs, *args, **kwds):
        return await super().__call__(cbs, *args, **kwds)

    @classmethod
    def from_http(cls: typing.Type[T], http) -> T:
        inst = super(AsyncHTTPBase, cls).from_http(http)
        setattr(inst, '_loop', getattr(http, '_loop'))
        return inst

    @property
    def loop(self) -> util.OptionalLoopType:
        """Get event loop."""
        return self._loop

    @property
    async def network_type(self) -> models.NetworkType:
        if self._network_type is None:
            network = self.root.network
            self._network_type = await network.get_network_type()
        return self._network_type

    @property
    async def _none(self) -> None:
        return None


class HTTP(HTTPSharedBase):
    """Abstract base class for the main HTTP client."""

    @property
    def account(self) -> AccountHTTP:
        """Get AccountHTTP to the same endpoint."""
        raise util.AbstractMethodError

    @property
    def blockchain(self) -> BlockchainHTTP:
        """Get BlockchainHTTP to the same endpoint."""
        raise util.AbstractMethodError

    @property
    def mosaic(self) -> MosaicHTTP:
        """Get MosaicHTTP to the same endpoint."""
        raise util.AbstractMethodError

    @property
    def namespace(self) -> NamespaceHTTP:
        """Get NamespaceHTTP to the same endpoint."""
        raise util.AbstractMethodError

    @property
    def network(self) -> NetworkHTTP:
        """Get NetworkHTTP to the same endpoint."""
        raise util.AbstractMethodError

    @property
    def transaction(self) -> TransactionHTTP:
        """Get TransactionHTTP to the same endpoint."""
        raise util.AbstractMethodError


class AccountHTTP(HTTPSharedBase):
    """Abstract base class for the account HTTP client."""

    def get_account_info(
        self,
        address: models.Address,
        **kwds
    ):
        """
        Get info for account.

        :param address: Account address.
        :return: Account info object.
        """
        return self(nis.get_account_info, address, **kwds)

    getAccountInfo = util.undoc(get_account_info)

    def get_accounts_info(
        self,
        addresses: typing.Sequence[models.Address],
        **kwds
    ):
        """
        Get info for accounts.

        :param addresses: Sequence of account addresses.
        :return: List of account info objects.
        """
        return self(nis.get_accounts_info, addresses, **kwds)

    getAccountsInfo = util.undoc(get_accounts_info)

    # TODO(ahuszagh)
    # getMultisigAccountInfo
    # getMultisigAccountGraphInfo
    # transactions
    # incomingTransactions
    # outgoingTransactions
    # unconfirmedTransactions
    # aggregateBondedTransactions


class BlockchainHTTP(HTTPSharedBase):
    """Abstract base class for the blockchain HTTP client."""

    def get_block_by_height(self, height: int, **kwds):
        """
        Get block information from the block height.

        :param height: Block height.
        :return: Information describing block.
        """
        return self(nis.get_block_by_height, height, **kwds)

    getBlockByHeight = util.undoc(get_block_by_height)

    # TODO(ahuszagh)
    # getBlockTransactions
    # getBlocksByHeightWithLimit

    def get_blockchain_height(self, **kwds):
        """
        Get current blockchain height.

        :return: Blockchain height.
        """
        return self(nis.get_blockchain_height, **kwds)

    getBlockchainHeight = util.undoc(get_blockchain_height)

    def get_blockchain_score(self, **kwds):
        """
        Get current blockchain score.

        :return: Blockchain score.
        """
        return self(nis.get_blockchain_score, **kwds)

    getBlockchainScore = util.undoc(get_blockchain_score)

    def get_diagnostic_storage(self, **kwds):
        """
        Get diagnostic storage information for blockchain.

        :return: Blockchain diagnostic storage information.
        """
        return self(nis.get_diagnostic_storage, **kwds)

    getDiagnosticStorage = util.undoc(get_diagnostic_storage)


class MosaicHTTP(HTTPSharedBase):
    """Abstract base class for the mosaic HTTP client."""

    def get_mosaic_names(
        self,
        ids: typing.Sequence[models.MosaicId],
        **kwds
    ):
        """
        Get mosaic names from IDs.

        :param ids: Sequence of mosaic IDs.
        :return: Mosaic names for IDS.
        """
        return self(nis.get_mosaic_names, ids, **kwds)

    getMosaicNames = util.undoc(get_mosaic_names)

    # TODO(ahuszagh)
    # getMosaic
    # getMosaics


class NamespaceHTTP(HTTPSharedBase):
    """Abstract base class for the namespace HTTP client."""

    def get_namespace(
        self,
        namespace_id: models.NamespaceId,
        **kwds
    ):
        """
        Get namespace information from ID.

        :param id: Namespace ID.
        :return: Namespace information.
        """
        return self(nis.get_namespace, namespace_id, **kwds)

    getNamespace = util.undoc(get_namespace)

    def get_namespaces_from_account(
        self,
        address: models.Address,
        **kwds
    ):
        """
        Get namespaces owned by account.

        :param address: Account address.
        :return: List of namespace information objects.
        """
        return self(nis.get_namespaces_from_account, address, **kwds)

    getNamespacesFromAccount = util.undoc(get_namespaces_from_account)

    def get_namespaces_from_accounts(
        self,
        addresses: typing.Sequence[models.Address],
        **kwds
    ):
        """
        Get namespaces owned by accounts.

        :param addresses: Sequence of account addresses.
        :return: List of namespace information objects.
        """
        return self(nis.get_namespaces_from_accounts, addresses, **kwds)

    getNamespacesFromAccounts = util.undoc(get_namespaces_from_accounts)

    def get_namespace_names(
        self,
        ids: typing.Sequence[models.NamespaceId],
        **kwds
    ):
        """
        Get namespace names from IDs.

        :param ids: Sequence of namespace IDs.
        :return: Namespace names for IDS.
        """
        return self(nis.get_namespace_names, ids, **kwds)

    getNamespaceNames = util.undoc(get_namespace_names)

    def get_linked_mosaic_id(
        self,
        namespace_id: models.NamespaceId,
        **kwds
    ):
        """
        Get mosaic ID from linked mosaic alias.

        :param id: Namespace ID.
        :return: Mosaic ID.
        """
        return self(nis.get_linked_mosaic_id, namespace_id, **kwds)

    getLinkedMosaicId = util.undoc(get_linked_mosaic_id)

    def get_linked_address(
        self,
        namespace_id: models.NamespaceId,
        **kwds
    ):
        """
        Get address from linked address alias.

        :param id: Namespace ID.
        :return: Address object.
        """
        return self(nis.get_linked_address, namespace_id, **kwds)

    getLinkedAddress = util.undoc(get_linked_address)


class NetworkHTTP(HTTPSharedBase):
    """Abstract base class for the network HTTP client."""

    def get_network_type(self, **kwds):
        """
        Get network type.

        :return: Network type.
        """
        return self(nis.get_network_type, network_type=self._none, **kwds)

    getNetworkType = util.undoc(get_network_type)


class TransactionHTTP(HTTPSharedBase):
    """Abstract base class for the transaction HTTP client."""

    def get_transaction(self, hash: str, **kwds):
        """
        Get transaction info by hash.

        :param hash: Transaction hash.
        :return: Transaction info.
        """
        return self(nis.get_transaction, hash, **kwds)

    getTransaction = util.undoc(get_transaction)

    def get_transactions(self, hashes: typing.Sequence[str], **kwds):
        """
        Get transaction info by hash.

        :param hashes: Sequence of transaction hashes.
        :return: Transaction info.
        """
        return self(nis.get_transactions, hashes, **kwds)

    getTransactions = util.undoc(get_transactions)

    def get_transaction_status(self, hash: str, **kwds):
        """
        Get transaction status by hash.

        :param hash: Transaction hash.
        :return: Transaction status.
        """
        return self(nis.get_transaction_status, hash, **kwds)

    getTransactionStatus = util.undoc(get_transaction_status)

    def get_transaction_statuses(self, hashes: typing.Sequence[str], **kwds):
        """
        Get transaction status by sequence of hashes.

        :param hashes: Sequence of transaction hashes.
        :return: List of transaction statuses.
        """
        return self(nis.get_transaction_statuses, hashes, **kwds)

    getTransactionStatuses = util.undoc(get_transaction_statuses)

    # TODO(ahuszagh)
    # announceAggregateBonded
    # announceAggregateBondedCosignature

    def announce(
        self,
        transaction: models.SignedTransaction,
        **kwds
    ):
        """
        Announce transaction to network.

        :param transaction: Signed transaction data.
        :return: Transaction announce response.
        """
        return self(nis.announce, transaction, **kwds)

    def announce_sync(
        self,
        transaction: models.SignedTransaction,
        **kwds
    ):
        """
        Announce and get synchronization message for transaction.

        :param transaction: Signed transaction data.
        :return: Transaction status or object.
        """
        return self(nis.announce_sync, transaction, **kwds)

    announceSync = util.undoc(announce_sync)


# WEBSOCKET
# ---------


@util.dataclass(frozen=True)
class ListenerMessage:
    """Message from a listener."""

    channel_name: str
    message: MessageType


@util.observable
class Listener:
    """
    Abstract base class for the websockets-based listener.

    :param endpoint: Domain name and port for the endpoint.
    """

    _client: client.WebsocketClient
    _iter_: typing.AsyncIterator[bytes]
    _conn: typing.AsyncContextManager
    _loop: util.OptionalLoopType
    _uid: typing.Optional[str] = None

    def __enter__(self) -> Listener:
        raise TypeError("Only use async with.")

    def __exit__(self, exc_type, exc, tb) -> None:
        pass

    async def __aenter__(self):
        raise util.AbstractMethodError

    async def __aexit__(self, exc_type, exc, tb) -> None:
        raise util.AbstractMethodError

    @property
    def raw(self) -> client.WebsocketClient:
        try:
            return self._client
        except AttributeError:
            raise RuntimeError('Must be used inside `async with` block.')

    @property
    def _iter(self) -> typing.AsyncIterator[bytes]:
        try:
            return self._iter_
        except AttributeError:
            raise RuntimeError('Must be used inside `async with` block.')

    @property
    def closed(self) -> bool:
        """Get if client session has been closed."""
        return self.raw.closed

    @property
    async def uid(self) -> str:
        """Get UUID (unique identifier) for WS requests."""

        if self._uid is None:
            self._uid = json.loads(await self.raw.recv())['uid']
        return self._uid

    def __aiter__(self) -> Listener:
        return self

    async def __anext__(self) -> typing.Optional[ListenerMessage]:
        """Iterate over subscribed messages."""

        message: bytes = await self._iter.__anext__()
        data = json.loads(message)
        if 'transaction' in data:
            channel_name = typing.cast(str, data['meta'].pop('channelName'))
            # TODO(ahuszagh) Implement.
            # Requires implementing a general deserializer for the transaction
            raise NotImplementedError
        elif 'block' in data:
            # New block info.
            block = models.BlockInfo.from_dto(data)
            return ListenerMessage('block', block)
        elif 'status' in data:
            # New transaction status error.
            error = models.TransactionStatusError.from_dto(data)
            return ListenerMessage('status', error)
        elif 'meta' in data:
            channel_name = typing.cast(str, data['meta']['channelName'])
            hash = typing.cast(str, data['meta']['hash'])
            return ListenerMessage(channel_name, hash)
        elif 'parentHash' in data:
            cosignature = models.CosignatureSignedTransaction.from_dto(data)
            return ListenerMessage('cosignature', cosignature)
        else:
            # Unknown data information, don't pollute the message,
            # only send the information's keys.
            msg = f"Unknown message from Listener subscription, keys are {data.keys()}."
            raise ValueError(msg)

    @util.observable
    async def new_block(self) -> None:
        """Emit message when new blocks are added to chain."""
        await self.subscribe('block')

    @util.observable
    async def confirmed(self, address: models.Address) -> None:
        """Emit message when new transactions are confirmed for a given address."""
        await self.subscribe(f'confirmedAdded/{address.address}')

    confirmed_added = confirmed
    confirmedAdded = util.undoc(confirmed_added)

    @util.observable
    async def unconfirmed_added(self, address: models.Address) -> None:
        """Emit message for unconfirmed transactions are announced."""
        await self.subscribe(f'confirmedAdded/{address.address}')

    unconfirmedAdded = util.undoc(unconfirmed_added)

    @util.observable
    async def unconfirmed_removed(self, address: models.Address) -> None:
        """Emit message when unconfirmed transactions change state."""
        await self.subscribe(f'unconfirmedRemoved/{address.address}')

    unconfirmedRemoved = util.undoc(unconfirmed_removed)

    @util.observable
    async def aggregate_bonded_added(self, address: models.Address) -> None:
        """Emit message when new, unconfirmed, aggregate transactions are announced."""
        await self.subscribe(f'partialAdded/{address.address}')

    aggregateBondedAdded = util.undoc(aggregate_bonded_added)

    @util.observable
    async def aggregate_bonded_removed(self, address: models.Address) -> None:
        """Emit message when unconfirmed, aggregate transactions change state."""
        await self.subscribe(f'partialRemoved/{address.address}')

    aggregateBondedRemoved = util.undoc(aggregate_bonded_removed)

    @util.observable
    async def status(self, address: models.Address) -> None:
        """Emit message each time a transaction contains an error."""
        await self.subscribe(f'status/{address.address}')

    @util.observable
    async def cosignature_added(self, address: models.Address) -> None:
        """Emit message each time a cosigner signs a message"""
        await self.subscribe(f'cosignature/{address.address}')

    async def subscribe(self, channel: str) -> None:
        """Subscribe to websockets channel."""

        message = json.dumps({
            'uid': await self.uid,
            'subscribe': channel
        })
        await self.raw.send(message)

    async def unsubscribe(self, channel: str) -> None:
        """Unsubscribe from websockets channel."""

        message = json.dumps({
            'uid': await self.uid,
            'unsubscribe': channel
        })
        await self.raw.send(message)
