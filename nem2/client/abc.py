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

import json
import typing

from nem2 import models
from nem2 import util
from . import nis

if typing.TYPE_CHECKING:
    from .client import Client, WebsocketClient
    from nem2.models import *

T = typing.TypeVar('T')
MessageType = typing.Union[
    'BlockInfo',
    'CosignatureSignedTransaction',
    'TransactionStatusError',
    str
]

# HTTP
# ----


class HttpBase:
    """
    Abstract base class for HTTP clients.

    :param endpoint: Domain name and port for the endpoint.
    """

    _client: 'Client'
    _index: int
    _network_type: typing.Optional['NetworkType'] = None

    def __call__(self, cbs, *args, **kwds):
        """Invoke the NIS callback."""
        cb: Cb = cbs[self.index]
        return typing.cast(T, cb(self.client, *args, **kwds))

    @classmethod
    def from_http(cls: typing.Type[T], http) -> T:
        """
        Initialize HttpBase directly from existing HTTP client.
        For internal use, do not use directly.

        :param http: HTTP client.
        """
        inst = cls.__new__(cls)
        inst._client = http._client
        inst._index = http._index
        inst._network_type = http._network_type
        return typing.cast(T, inst)

    @property
    def client(self) -> 'Client':
        """Get client wrapper for HTTP client."""
        return self._client

    @property
    def index(self) -> int:
        """Get index for NIS callbacks."""
        return self._index

    @property
    def network_type(self):
        """Get network type for client."""

        if self._network_type is None:
            network = self.root.network
            self._network_type = network.get_network_type()
        return self._network_type

    @property
    def networkType(self):
        return self.network_type

    @property
    def root(self) -> 'Http':
        """Get Http to the same endpoint."""
        raise NotImplementedError


@util.inherit_doc
class AsyncHttpBase(HttpBase):
    """
    Abstract base class for asynchronous HTTP clients.

    :param endpoint: Domain name and port for the endpoint.
    :param loop: (Optional) Event loop for the client.
    """

    _loop: util.OptionalLoopType

    def __call__(self, cbs, *args, **kwds):
        return self.call(cbs, *args, **kwds)

    @util.observable
    async def call(self, cbs, *args, **kwds):
        """Invoke callback and wrap it in an observable."""
        return await super().__call__(cbs, *args, **kwds)

    @classmethod
    def from_http(cls: typing.Type[T], http) -> T:
        """
        Initialize AsyncHttpBase directly from existing HTTP client.
        For internal use, do not use directly.

        :param http: HTTP client.
        """
        inst = super(AsyncHttpBase, cls).from_http(http)
        setattr(inst, '_loop', getattr(http, '_loop'))
        return inst

    @property
    def loop(self):
        """Get event loop."""
        return self._loop

    @property
    async def network_type(self):
        """Get network type for client."""

        if self._network_type is None:
            network = self.root.network
            self._network_type = await network.get_network_type()
        return self._network_type


class Http(HttpBase):
    """Abstract base class for the main HTTP client."""

    @property
    def account(self) -> 'AccountHttp':
        """Get AccountHttp to the same endpoint."""
        raise NotImplementedError

    @property
    def blockchain(self) -> 'BlockchainHttp':
        """Get BlockchainHttp to the same endpoint."""
        raise NotImplementedError

    @property
    def mosaic(self) -> 'MosaicHttp':
        """Get MosaicHttp to the same endpoint."""
        raise NotImplementedError

    @property
    def namespace(self) -> 'NamespaceHttp':
        """Get NamespaceHttp to the same endpoint."""
        raise NotImplementedError

    @property
    def network(self) -> 'NetworkHttp':
        """Get NetworkHttp to the same endpoint."""
        raise NotImplementedError

    @property
    def transaction(self) -> 'TransactionHttp':
        """Get TransactionHttp to the same endpoint."""
        raise NotImplementedError


class AccountHttp(HttpBase):
    """Abstract base class for the account HTTP client."""

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


class BlockchainHttp(HttpBase):
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


class MosaicHttp(HttpBase):
    """Abstract base class for the mosaic HTTP client."""

    def get_mosaic_names(self, ids: typing.Sequence['MosaicId'], **kwds):
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


class NamespaceHttp(HttpBase):
    """Abstract base class for the namespace HTTP client."""

    def get_namespace(self, namespace_id: 'NamespaceId', **kwds):
        """
        Get namespace information from ID.

        :param id: Namespace ID.
        :return: Namespace information.
        """
        return self(nis.get_namespace, namespace_id, **kwds)

    getNamespace = util.undoc(get_namespace)

    def get_namespaces_from_account(self, address: 'Address', **kwds):
        """
        Get namespaces owned by account.

        :param address: Account address.
        :return: List of namespace information objects.
        """
        return self(nis.get_namespaces_from_account, address, **kwds)

    getNamespacesFromAccount = util.undoc(get_namespaces_from_account)

    def get_namespaces_from_accounts(self, addresses: typing.Sequence['Address'], **kwds):
        """
        Get namespaces owned by accounts.

        :param addresses: Sequence of account addresses.
        :return: List of namespace information objects.
        """
        return self(nis.get_namespaces_from_accounts, addresses, **kwds)

    getNamespacesFromAccounts = util.undoc(get_namespaces_from_accounts)

    def get_namespace_names(self, ids: typing.Sequence['NamespaceId'], **kwds):
        """
        Get namespace names from IDs.

        :param ids: Sequence of namespace IDs.
        :return: Namespace names for IDS.
        """
        return self(nis.get_namespace_names, ids, **kwds)

    getNamespaceNames = util.undoc(get_namespace_names)

    def get_linked_mosaic_id(self, namespace_id: 'NamespaceId', **kwds):
        """
        Get mosaic ID from linked mosaic alias.

        :param id: Namespace ID.
        :return: Mosaic ID.
        """
        return self(nis.get_linked_mosaic_id, namespace_id, **kwds)

    getLinkedMosaicId = util.undoc(get_linked_mosaic_id)

    def get_linked_address(self, namespace_id: 'NamespaceId', **kwds):
        """
        Get address from linked address alias.

        :param id: Namespace ID.
        :return: Address object.
        """
        return self(nis.get_linked_address, namespace_id, **kwds)

    getLinkedAddress = util.undoc(get_linked_address)


class NetworkHttp(HttpBase):
    """Abstract base class for the network HTTP client."""

    def get_network_type(self, **kwds):
        """
        Get network type.

        :return: Network type.
        """
        return self(nis.get_network_type, **kwds)

    getNetworkType = util.undoc(get_network_type)


class TransactionHttp(HttpBase):
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
    # announce
    # announceAggregateBonded
    # announceAggregateBondedCosignature
    # announceSync


# WEBSOCKET
# ---------


@util.dataclass(frozen=True)
class ListenerMessage:
    """Message from a listener."""

    channel_name: str
    message: MessageType


class Listener:
    """
    Abstract base class for the websockets-based listener.

    :param endpoint: Domain name and port for the endpoint.
    """

    _client: 'WebsocketClient'
    _loop: util.OptionalLoopType
    _uid: typing.Optional[str] = None

    def __enter__(self) -> 'Listener':
        raise TypeError("Only use async with.")

    def __exit__(self) -> None:
        pass

    async def __aenter__(self) -> 'Listener':
        return self

    async def __aexit__(self) -> None:
        return await self.close()

    async def close(self) -> None:
        """Close the client session."""
        await self._client.close()

    @property
    def closed(self) -> bool:
        """Get if client session has been closed."""
        return self._client.closed

    @property
    async def uid(self) -> str:
        """Get UUID (unique identifier) for WS requests."""

        if self._uid is None:
            self._uid = json.loads(await self._client.recv())['uid']
        return self._uid

    @util.observable
    async def __aiter__(self) -> typing.AsyncIterator[ListenerMessage]:
        """Iterate over subscribed messages."""

        async for message in self._client:
            data = json.loads(message)
            if 'uid' in data:
                # UID reset.
                self._uid = data['uid']
            elif 'transaction' in data:
                channel_name = typing.cast(str, data['meta'].pop('channelName'))
                # TODO(ahuszagh) Implement.
                # Requires implementing a general deserializer for the transaction
                raise NotImplementedError
            elif 'block' in data:
                # New block info.
                yield ListenerMessage('block', models.BlockInfo.from_dto(data))
            elif 'status' in data:
                # New transaction status error.
                yield ListenerMessage('status', models.TransactionStatusError.from_dto(data))
            elif 'meta' in data:
                channel_name = typing.cast(str, data['meta']['channelName'])
                hash = typing.cast(str, data['meta']['hash'])
                yield ListenerMessage(channel_name, hash)
            elif 'parentHash' in data:
                yield ListenerMessage('cosignature', models.CosignatureSignedTransaction.from_dto(data))
            else:
                # Unknown data information, don't pollute the message,
                # only send the information's keys.
                raise ValueError(f"Unknown message from Listener subscription, keys are {data.keys()}.")

    async def new_block(self) -> None:
        """Emit message when new blocks are added to chain."""
        await self.subscribe('block')

    async def confirmed(self, address: 'Address') -> None:
        """Emit message when new transactions are confirmed for a given address."""
        await self.subscribe(f'confirmedAdded/{address.address}')

    confirmed_added = confirmed
    confirmedAdded = util.undoc(confirmed_added)

    async def unconfirmed_added(self, address: 'Address') -> None:
        """Emit message when new, unconfirmed transactions are announced for a given address."""
        await self.subscribe(f'confirmedAdded/{address.address}')

    unconfirmedAdded = util.undoc(unconfirmed_added)

    async def unconfirmed_removed(self, address: 'Address') -> None:
        """Emit message when unconfirmed transactions change state for a given address."""
        await self.subscribe(f'unconfirmedRemoved/{address.address}')

    unconfirmedRemoved = util.undoc(unconfirmed_removed)

    async def aggregate_bonded_added(self, address: 'Address') -> None:
        """Emit message when new, unconfirmed, aggregate transactions are announced for a given address."""
        await self.subscribe(f'partialAdded/{address.address}')

    aggregateBondedAdded = util.undoc(aggregate_bonded_added)

    async def aggregate_bonded_removed(self, address: 'Address') -> None:
        """Emit message when unconfirmed, aggregate transactions change state for a given address."""
        await self.subscribe(f'partialRemoved/{address.address}')

    aggregateBondedRemoved = util.undoc(aggregate_bonded_removed)

    async def status(self, address: 'Address') -> None:
        """Emit message each time a transaction contains an error for a given address."""
        await self.subscribe(f'status/{address.address}')

    async def cosignature_added(self, address: 'Address') -> None:
        """Emit message each time a cosigner signs a message initiated by the given address."""
        await self.subscribe(f'cosignature/{address.address}')

    async def subscribe(self, channel: str) -> None:
        """Subscribe to websockets channel."""

        message = json.dumps({
            'uid': await self.uid,
            'subscribe': channel
        })
        await self._client.send(message)

    async def unsubscribe(self, channel: str) -> None:
        """Unsubscribe from websockets channel."""

        message = json.dumps({
            'uid': await self.uid,
            'unsubscribe': channel
        })
        await self._client.send(message)
