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

from . import client
from . import nis
from .. import models
from .. import util


T = typing.TypeVar('T')
MessageType = typing.Union[
    models.BlockInfo,
    models.CosignatureSignedTransaction,
    models.Transaction,
    models.TransactionStatusError,
    str,
]

# HTTP
# ----


class HTTPSharedBase(util.Object):
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

    @classmethod
    def create_from_http(cls: typing.Type[T], http) -> T:
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
    def create_from_http(cls: typing.Type[T], http) -> T:
        inst = super(AsyncHTTPBase, cls).create_from_http(http)  # type: ignore
        setattr(inst, '_loop', getattr(http, '_loop'))
        return inst  # type: ignore

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

    # @property
    # def contract(self) -> ContractHTTP:
    #    """Get ContractHTTP to the same endpoint."""
    #    raise util.AbstractMethodError

    @property
    def metadata(self) -> MetadataHTTP:
        """Get MetadataHTTP to the same endpoint."""
        raise util.AbstractMethodError

    @property
    def config(self) -> ConfigHTTP:
        """Get ConfigHTTP to the same endpoint."""
        raise util.AbstractMethodError

    @property
    def node(self) -> NodeHTTP:
        """Get NodeHTTP to the same endpoint."""
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

    def get_account_properties(
        self,
        address: models.Address,
        **kwds
    ):
        """
        Get properties information for account.

        :param address: Account address.
        :return: AccountPropertiesInfo object.
        """
        return self(nis.get_account_properties, address, **kwds)

    def get_accounts_properties(
        self,
        addresses: typing.Sequence[models.Address],
        **kwds
    ):
        """
        Get properties information for accounts.

        :param addresses: Sequence of account addresses.
        :return: AccountPropertiesInfo object.
        """
        return self(nis.get_accounts_properties, addresses, **kwds)

    def get_multisig_account_info(
        self,
        address: models.Address,
        **kwds
    ):
        """
        Get multisig account information for account.

        :param address: Account address.
        :return: MultisigAccountInfo object.
        """
        return self(nis.get_multisig_account_info, address, **kwds)

    def get_multisig_account_graph_info(
        self,
        address: models.Address,
        **kwds
    ):
        """
        Get multisig account graph information for account.

        :param address: Account address.
        :return: MultisigAccountGraphInfo object.
        """
        return self(nis.get_multisig_account_graph_info, address, **kwds)

    def transactions(
        self,
        public_account: models.PublicAccount,
        **kwds
    ):
        """
        Get all transactions for account.

        :param public_account: Public key and address for account.
        :return: List of transaction objects.
        """
        return self(nis.get_account_transactions, public_account, **kwds)

    def incoming_transactions(
        self,
        public_account: models.PublicAccount,
        **kwds
    ):
        """
        Get all incoming transactions for account.

        :param public_account: Public key and address for account.
        :return: List of incoming transaction objects.
        """
        return self(nis.get_account_incoming_transactions, public_account, **kwds)

    def outgoing_transactions(
        self,
        public_account: models.PublicAccount,
        **kwds
    ):
        """
        Get all outgoing transactions for account.

        :param public_account: Public key and address for account.
        :return: List of outgoing transaction objects.
        """
        return self(nis.get_account_outgoing_transactions, public_account, **kwds)

    def unconfirmed_transactions(
        self,
        public_account: models.PublicAccount,
        **kwds
    ):
        """
        Get all unconfirmed transactions for account.

        :param public_account: Public key and address for account.
        :return: List of unconfirmed transaction objects.
        """
        return self(nis.get_account_unconfirmed_transactions, public_account, **kwds)

    def aggregate_bonded_transactions(
        self,
        public_account: models.PublicAccount,
        **kwds
    ):
        """
        Get all aggregate bonded transactions for account.

        :param public_account: Public key and address for account.
        :return: List of aggregate bonded transaction objects.
        """
        return self(nis.get_account_partial_transactions, public_account, **kwds)
# TODO: Check when stabilized
#     def contracts(
#         self,
#         public_account: models.PublicAccount,
#         **kwds
#     ):
#         """
#         Get account contracts.
#
#         :param public_account: Public account.
#         :return: List of ContractInfo object.
#         """
#         return self(nis.get_account_contracts, public_account, **kwds)

    def get_account_names(
        self,
        addresses: typing.Sequence[models.Address],
        **kwds
    ):
        """
        Get friendly names of accounts.

        :param addresses: Sequence of account addresses.
        :return: AccountNames object.
        """
        return self(nis.get_account_names, addresses, **kwds)


class BlockchainHTTP(HTTPSharedBase):
    """Abstract base class for the blockchain HTTP client."""

    def get_block_by_height(self, height: int, **kwds):
        """
        Get block information from the block height.

        :param height: Block height.
        :return: Information describing block.
        """
        return self(nis.get_block_by_height, height, **kwds)

    def get_blocks_by_height_with_limit(self, height: int, limit: int, **kwds):
        """
        Get information for blocks between [height, height+limit].

        :param height: Block height.
        :param limit: Maximum number of blocks to return.
        :return: Sequence of information models describing blocks.
        """
        return self(nis.get_blocks_by_height_with_limit, height, limit, **kwds)

    def get_block_transactions(self, height: int, **kwds):
        """
        Get information for all transactions included in a block by height.

        :param height: Block height.
        :return: Sequence of information models describing transactions.
        """
        return self(nis.get_block_transactions, height, **kwds)

    def get_merkle_by_hash_in_block(self, height: int, hash: str, **kwds):
        """
        Get information for all transactions included in a block by height.

        :param height: Block height.
        :param hash: Transaction hash.
        :return: Sequence of information models describing transactions.
        """
        return self(nis.get_merkle_by_hash_in_block, height, hash, **kwds)

    def get_block_receipts(self, height: int, **kwds):
        """
        Get receipts for a block by height.

        :param height: Block height.
        :return: Sequence of information models describing transactions.
        """
        return self(nis.get_block_receipts, height, **kwds)

    def get_blockchain_height(self, **kwds):
        """
        Get current blockchain height.

        :return: Blockchain height.
        """
        return self(nis.get_blockchain_height, **kwds)

    def get_blockchain_score(self, **kwds):
        """
        Get current blockchain score.

        :return: Blockchain score.
        """
        return self(nis.get_blockchain_score, **kwds)

    def get_diagnostic_blocks_by_height_with_limit(self, height: int, limit: int, **kwds):
        """
        Get diagnostic information for blocks between [height, height+limit].

        :param height: Block height.
        :param limit: Maximum number of blocks to return.
        :return: Sequence of information models describing blocks.
        """
        return self(nis.get_diagnostic_blocks_by_height_with_limit, height, limit, **kwds)

    def get_diagnostic_storage(self, **kwds):
        """
        Get diagnostic storage information for blockchain.

        :return: Blockchain diagnostic storage information.
        """
        return self(nis.get_diagnostic_storage, **kwds)

    def get_diagnostic_server(self, **kwds):
        """
        Get diagnostic storage information for rest server.

        :return: Blockchain diagnostic rest server information.
        """
        return self(nis.get_diagnostic_server, **kwds)


class ContractHTTP(HTTPSharedBase):
    """Abstract base class for the Contract HTTP client."""
    pass
# TODO: Check when stabilized
#     def get_contract(
#         self,
#         contract_id: str,
#         **kwds
#     ):
#         """
#         Gets the contract for a given contractId.
#
#         :param contractId: The account identifier.
#         :return: ContractInfo.
#         """
#         return self(nis.get_contract, contract_id, **kwds)
#
#     def get_contracts(
#         self,
#         addresses: typing.Sequence[models.Address],
#         **kwds
#     ):
#         """
#         Get contracts for an array of addresses
#
#         :param height: The height of the blockchain to get config.
#         :return: Sequence of ContractInfo.
#         """
#         return self(nis.get_contracts, addresses, **kwds)


class MetadataHTTP(HTTPSharedBase):
    """Abstract base class for the Metadata HTTP client."""

    def get_account_metadata(
        self,
        public_account: models.PublicAccount,
        **kwds
    ):
        """
        Get account metadata.

        :param public_account: Public account.
        :return: List of ContractInfo object.
        """
        return self(nis.get_account_metadata, public_account, **kwds)

    def get_mosaic_metadata(
        self,
        mosaic_id: models.MosaicId,
        **kwds
    ):
        """
        Get mosaic metadata.

        :param mosaic_id: Mosaic.
        :return: List of ContractInfo object.
        """
        return self(nis.get_mosaic_metadata, mosaic_id, **kwds)

    def get_namespace_metadata(
        self,
        namespace_id: models.NamespaceId,
        **kwds
    ):
        """
        Get namespace metadata.

        :param namespace_id: Namespace ID.
        :return: Metadata for a namespace.
        """
        return self(nis.get_namespace_metadata, namespace_id, **kwds)

    def get_metadata(
        self,
        metadata_id: str,
        **kwds
    ):
        """
        Gets the metadata for a given metadataId.

        :param metadataId: The metadata identifiers.
        :return: MetadataInfo.
        """
        return self(nis.get_metadata, metadata_id, **kwds)

    def get_metadatas(
        self,
        metadata_ids: typing.Sequence[str],
        **kwds
    ):
        """
        Gets the metadatas for a given metadataIds.

        :param metadataIds: The metadata identifiers.
        :return: Sequence of MetadataInfo.
        """
        return self(nis.get_metadatas, metadata_ids, **kwds)


class ConfigHTTP(HTTPSharedBase):
    """Abstract base class for the Config HTTP client."""

    def get_config(
        self,
        height: int,
        **kwds
    ):
        """
        Gets config of network at height.

        :param height: The height of the blockchain to get config.
        :return: CatapultConfig.
        """
        return self(nis.get_config, height, **kwds)

    def get_upgrade(
        self,
        height: int,
        **kwds
    ):
        """
        Gets upgrade of network at height.

        :param height: The height of the blockchain to get upgrade.
        :return: CatapultUpgrade.
        """
        return self(nis.get_upgrade, height, **kwds)


class NodeHTTP(HTTPSharedBase):
    """Abstract base class for the Node HTTP client."""

    def get_node_info(
        self,
        **kwds
    ):
        """
        Supplies additional information about the application running on a node.

        :return: NodeInfo.
        """
        return self(nis.get_node_info, **kwds)

    def get_node_time(
        self,
        **kwds
    ):
        """
        Gets the node time at the moment the reply was sent and received.

        :return: NodeTime.
        """
        return self(nis.get_node_time, **kwds)


class MosaicHTTP(HTTPSharedBase):
    """Abstract base class for the mosaic HTTP client."""

    def get_mosaic(
        self,
        id: models.MosaicId,
        **kwds
    ):
        """
        Get mosaic info from ID.

        :param id: Mosaic ID.
        :return: Mosaic info for ID.
        """
        return self(nis.get_mosaic, id, **kwds)

    def get_mosaics(
        self,
        ids: typing.Sequence[models.MosaicId],
        **kwds
    ):
        """
        Get mosaic info from IDs.

        :param ids: Sequence of mosaic IDs.
        :return: Mosaic info list for IDS.
        """
        return self(nis.get_mosaics, ids, **kwds)

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

    def get_mosaic_richlist(
        self,
        mosaic_id: models.MosaicId,
        **kwds
    ):
        """
        Get account balances in a given Mosaic.

        :param mosaic_id: Mosaic ID.
        :return: Account balances.
        """
        return self(nis.get_mosaic_richlist, mosaic_id, **kwds)


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

    def get_namespaces_name(
        self,
        ids: typing.Sequence[models.NamespaceId],
        **kwds
    ):
        """
        Get namespace names from IDs.

        :param ids: Sequence of namespace IDs.
        :return: Namespace names for IDS.
        """
        return self(nis.get_namespaces_name, ids, **kwds)

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


class NetworkHTTP(HTTPSharedBase):
    """Abstract base class for the network HTTP client."""

    def get_network_type(self, **kwds):
        """
        Get network type.

        :return: Network type.
        """
        return self(nis.get_network_type, network_type=self._none, **kwds)


class TransactionHTTP(HTTPSharedBase):
    """Abstract base class for the transaction HTTP client."""

    def get_transaction(self, hash: str, **kwds):
        """
        Get transaction info by hash.

        :param hash: Transaction hash.
        :return: Transaction info.
        """
        return self(nis.get_transaction, hash, **kwds)

    def get_transactions(self, hashes: typing.Sequence[str], **kwds):
        """
        Get transaction info by hash.

        :param hashes: Sequence of transaction hashes.
        :return: Transaction info.
        """
        return self(nis.get_transactions, hashes, **kwds)

    def get_transaction_status(self, hash: str, **kwds):
        """
        Get transaction status by hash.

        :param hash: Transaction hash.
        :return: Transaction status.
        """
        return self(nis.get_transaction_status, hash, **kwds)

    def get_transaction_statuses(self, hashes: typing.Sequence[str], **kwds):
        """
        Get transaction status by sequence of hashes.

        :param hashes: Sequence of transaction hashes.
        :return: List of transaction statuses.
        """
        return self(nis.get_transaction_statuses, hashes, **kwds)

    # TODO(ahuszagh)
    # getTransactionEffectiveFee

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

    def announce_partial(
        self,
        transaction: models.SignedTransaction,
        **kwds
    ):
        """
        Announce partial transaction to network.

        :param transaction: Signed transaction data.
        :return: Transaction announce response.
        """
        return self(nis.announce_partial, transaction, **kwds)

    def announce_cosignature(
        self,
        transaction: models.SignedTransaction,
        **kwds
    ):
        """
        Announce cosignature transaction to network.

        :param transaction: Signed transaction data.
        :return: Transaction announce response.
        """
        return self(nis.announce_cosignature, transaction, **kwds)

# WEBSOCKET
# ---------


@util.dataclass(frozen=True)
class ListenerMessage(util.Object):
    """Message from a listener."""

    channel_name: str
    message: MessageType


@util.observable
class Listener(util.Object):
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
            # New transaction data.
            channel_name = typing.cast(str, data['meta'].pop('channelName'))
            transaction = models.Transaction.create_from_dto(data)
            return ListenerMessage(channel_name, transaction)
        elif 'block' in data:
            # New block info.
            block = models.BlockInfo.create_from_dto(data)
            return ListenerMessage('block', block)
        elif 'status' in data:
            # New transaction status error.
            error = models.TransactionStatusError.create_from_dto(data)
            return ListenerMessage('status', error)
        elif 'meta' in data:
            # New metadata.
            channel_name = typing.cast(str, data['meta']['channelName'])
            hash = typing.cast(str, data['meta']['hash'])
            return ListenerMessage(channel_name, hash)
        elif 'parentHash' in data:
            # New cosignature for transaction.
            cosignature = models.CosignatureSignedTransaction.create_from_dto(data)
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

    @util.observable
    async def confirmed_added(self, address: models.Address) -> None:
        """Emit message when new transactions are confirmed for a given address."""
        await self.confirmed(address)

    @util.observable
    async def unconfirmed_added(self, address: models.Address) -> None:
        """Emit message for unconfirmed transactions are announced."""
        await self.subscribe(f'unconfirmedAdded/{address.address}')

    @util.observable
    async def unconfirmed_removed(self, address: models.Address) -> None:
        """Emit message when unconfirmed transactions change state."""
        await self.subscribe(f'unconfirmedRemoved/{address.address}')

    @util.observable
    async def aggregate_bonded_added(self, address: models.Address) -> None:
        """Emit message when new, unconfirmed, aggregate transactions are announced."""
        await self.subscribe(f'partialAdded/{address.address}')

    @util.observable
    async def aggregate_bonded_removed(self, address: models.Address) -> None:
        """Emit message when unconfirmed, aggregate transactions change state."""
        await self.subscribe(f'partialRemoved/{address.address}')

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
