"""
    abc
    ===

    Abstract base classes for HTTP clients.

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
from . import nis

if typing.TYPE_CHECKING:
    from .host import Host
    from nem2.models import *

T = typing.TypeVar('T')
Cb = typing.Callable[..., T]
Cbs = typing.Tuple[Cb, Cb]


class HttpBase:
    """
    Abstract base class for HTTP clients.

    :param endpoint: Domain name and port for the endpoint.
    """

    _host: 'Host'
    _index: int
    _network_type: typing.Optional['NetworkType'] = None

    def __init__(self, endpoint: str) -> None:
        raise NotImplementedError

    def __call__(self, cbs: Cbs, *args, **kwds) -> T:
        """Invoke the NIS callback."""
        cb: Cb = cbs[self.index]
        return typing.cast(T, cb(self.host, *args, **kwds))

    @classmethod
    def from_http(cls: typing.Type[T], http) -> T:
        """
        Initialize HttpBase directly from existing HTTP client.
        For internal use, do not use directly.

        :param http: HTTP client.
        """
        inst = cls.__new__(cls)
        inst._host = http._host
        inst._index = http._index
        inst._network_type = http._network_type
        return typing.cast(T, inst)

    @property
    def host(self) -> 'Host':
        """Get host for HTTP client."""
        return self._host

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

    def __init__(self, endpoint: str, loop: util.OptionalLoopType = None) -> None:
        raise NotImplementedError

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

    def get_block_by_height(self, height: int, **kwds) -> 'BlockInfo':
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

    # TODO(ahuszagh)
    # getTransaction
    # getTransactions
    # getTransactionStatus
    # getTransactionsStatuses
    # announce
    # announceAggregateBonded
    # announceAggregateBondedCosignature
    # announceSync
