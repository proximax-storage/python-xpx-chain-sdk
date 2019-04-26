"""
    nis
    ===

    Free functions to abstractly wrap the NIS REST API with an abstract client.

    These functions return HTTP responses, or futures to responses, and do
    not do any formatting for the NEM response.

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
import typing

from . import client
from .. import util
from .. import models

OptionalNetworkType = typing.Optional[models.NetworkType]
TransactionType = typing.TypeVar('TransactionType', bound=models.Transaction)

# BOILERPLATE
# -----------


def synchronous_request(name, doc="", raise_for_status=True):
    """Generate wrappers for a synchronous request."""

    def f(client, network_type, *args, **kwds):
        response = REQUEST[name](client, *args, **kwds)
        if raise_for_status:
            response.raise_for_status()
        status = response.status_code
        json = response.json()
        return PROCESS[name](status, json, network_type)

    f.__name__ = name
    f.__doc__ = doc
    f.func_name = name

    return f


def asynchronous_request(name, doc="", raise_for_status=True):
    """Generate wrappers for an asynchronous request."""

    async def f(client, network_awaitable, *args, **kwds):
        # Await the network type so if an exception is thrown, we
        # don't forget to await the awaitable.
        network_type = await network_awaitable
        async with REQUEST[name](client, *args, **kwds) as response:
            if raise_for_status:
                response.raise_for_status()
            status = response.status
            json = await response.json()
            return PROCESS[name](status, json, network_type)

    f.__name__ = f"async_{name}"
    f.__doc__ = doc
    f.func_name = f"async_{name}"

    return f


def request(*args, **kwds):
    """Generate synchronous and asynchronous request wrappers."""

    s = synchronous_request(*args, **kwds)
    a = asynchronous_request(*args, **kwds)
    return s, a


# ACCOUNT HTTP
# ------------


def request_get_account_info(
    client: client.Client,
    address: models.Address,
    **kwds
):
    """
    Make "/account/{address}" request.

    :param client: Wrapper for client.
    :param address: Account address.
    :param timeout: (Optional) timeout for request (in seconds).
    """
    return client.get(f"/account/{address.address}", **kwds)


def process_get_account_info(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.AccountInfo:
    """
    Process the "/account/{address}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return models.AccountInfo.from_dto(json, network_type)


get_account_info = request("get_account_info")


def request_get_accounts_info(
    client: client.Client,
    addresses: typing.Sequence[models.Address],
    **kwds
):
    """
    Make "/account" request.

    :param client: Wrapper for client.
    :param addresses: Sequence of account addresses.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    json = {"addresses": [i.address for i in addresses]}
    return client.post(f"/account", json=json, **kwds)


def process_get_accounts_info(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.AccountInfo]:
    """
    Process the "/account" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return [models.AccountInfo.from_dto(i, network_type) for i in json]


get_accounts_info = request("get_accounts_info")


def request_get_account_property(
    client: client.Client,
    address: models.Address,
    **kwds
):
    """
    Make "/account/properties/{address}" request.

    :param client: Wrapper for client.
    :param address: Account address.
    :param timeout: (Optional) timeout for request (in seconds).
    """
    return client.get(f"/account/properties/{address.address}", **kwds)


def process_get_account_property(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> AccountPropertiesInfo:
    """
    Process the "/account/properties/{address}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return models.AccountPropertiesInfo.from_dto(json, network_type)


get_account_property = request("get_account_property")


def request_get_account_properties(
    client: client.Client,
    addresses: typing.Sequence[models.Address],
    **kwds
):
    """
    Make "/account/properties" request.

    :param client: Wrapper for client.
    :param addresses: Sequence of account addresses.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    json = {"addresses": [i.address for i in addresses]}
    return client.post(f"/account/properties", json=json, **kwds)


def process_get_account_properties(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> AccountPropertiesInfo:
    """
    Process the "/account/properties" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return models.AccountPropertiesInfo.from_dto(json, network_type)


get_account_properties = request("get_account_properties")


def request_get_multisig_account_info(
    client: client.Client,
    address: models.Address,
    **kwds
):
    """
    Make "/account/{address}/multisig" request.

    :param client: Wrapper for client.
    :param address: Account address.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/account/{address.address}/multisig", **kwds)


def process_get_multisig_account_info(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.MultisigAccountInfo:
    """
    Process the "/account/{address}/multisig" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return models.MultisigAccountInfo.from_dto(json, network_type)


get_multisig_account_info = request("get_multisig_account_info")


def request_get_multisig_account_graph_info(
    client: client.Client,
    address: models.Address,
    **kwds
):
    """
    Make "/account/{address}/multisig/graph" request.

    :param client: Wrapper for client.
    :param address: Account address.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/account/{address.address}/multisig/graph", **kwds)


def process_get_multisig_account_graph_info(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.MultisigAccountInfo:
    """
    Process the "/account/{address}/multisig/graph" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return models.MultisigAccountGraphInfo.from_dto(json, network_type)


get_multisig_account_graph_info = request("get_multisig_account_graph_info")


def request_get_account_transactions(
    client: client.Client,
    public_account: models.PublicAccount,
    **kwds
):
    """
    Make "/account/{public_key}/transactions" request.

    :param client: Wrapper for client.
    :param height: Height of block.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/account/{public_account.public_key}/transactions", **kwds)


def process_get_account_transactions(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[TransactionType]:
    """
    Process the "/account/{public_key}/transactions" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return [models.Transaction.from_dto(i, network_type) for i in json]


get_account_transactions = request("get_account_transactions")


def request_get_account_incoming_transactions(
    client: client.Client,
    public_account: models.PublicAccount,
    **kwds
):
    """
    Make "/account/{public_key}/transactions/incoming" request.

    :param client: Wrapper for client.
    :param height: Height of block.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/account/{public_account.public_key}/transactions/incoming", **kwds)


def process_get_account_incoming_transactions(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[TransactionType]:
    """
    Process the "/account/{public_key}/transactions/incoming" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return [models.Transaction.from_dto(i, network_type) for i in json]


get_account_incoming_transactions = request("get_account_incoming_transactions")


def request_get_account_outgoing_transactions(
    client: client.Client,
    public_account: models.PublicAccount,
    **kwds
):
    """
    Make "/account/{public_key}/transactions/outgoing" request.

    :param client: Wrapper for client.
    :param height: Height of block.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/account/{public_account.public_key}/transactions/outgoing", **kwds)


def process_get_account_outgoing_transactions(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[TransactionType]:
    """
    Process the "/account/{public_key}/transactions/outgoing" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return [models.Transaction.from_dto(i, network_type) for i in json]


get_account_outgoing_transactions = request("get_account_outgoing_transactions")


def request_get_account_unconfirmed_transactions(
    client: client.Client,
    public_account: models.PublicAccount,
    **kwds
):
    """
    Make "/account/{public_key}/transactions/unconfirmed" request.

    :param client: Wrapper for client.
    :param height: Height of block.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/account/{public_account.public_key}/transactions/unconfirmed", **kwds)


def process_get_account_unconfirmed_transactions(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[TransactionType]:
    """
    Process the "/account/{public_key}/transactions/unconfirmed" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return [models.Transaction.from_dto(i, network_type) for i in json]


get_account_unconfirmed_transactions = request("get_account_unconfirmed_transactions")


def request_get_account_partial_transactions(
    client: client.Client,
    public_account: models.PublicAccount,
    **kwds
):
    """
    Make "/account/{public_key}/transactions/partial" request.

    :param client: Wrapper for client.
    :param height: Height of block.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/account/{public_account.public_key}/transactions/partial", **kwds)


def process_get_account_partial_transactions(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[TransactionType]:
    """
    Process the "/account/{public_key}/transactions/partial" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return [models.Transaction.from_dto(i, network_type) for i in json]


get_account_partial_transactions = request("get_account_partial_transactions")

# BLOCKCHAIN HTTP
# ---------------


def request_get_block_by_height(
    client: client.Client,
    height: int,
    **kwds
):
    """
    Make "/block/{height}" request.

    :param client: Wrapper for client.
    :param height: Height of block.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/block/{height}", **kwds)


def process_get_block_by_height(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.BlockInfo:
    """
    Process the "/block/{height}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return models.BlockInfo.from_dto(json, network_type)


get_block_by_height = request("get_block_by_height")


def request_get_blocks_by_height_and_limit(
    client: client.Client,
    height: int,
    limit: int,
    **kwds
):
    """
    Make "/blocks/{height}/limit/{limit}" request.

    :param client: Wrapper for client.
    :param height: Height of block.
    :param limit: Maximum number of blocks to return.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/blocks/{height}/limit/{limit}", **kwds)


def process_get_blocks_by_height_and_limit(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.BlockInfo]:
    """
    Process the "/blocks/{height}/limit/{limit}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return [models.BlockInfo.from_dto(i, network_type) for i in json]


get_blocks_by_height_and_limit = request("get_blocks_by_height_and_limit")


def request_get_block_transactions(
    client: client.Client,
    height: int,
    **kwds
):
    """
    Make "/blocks/{height}/transactions" request.

    :param client: Wrapper for client.
    :param height: Height of block.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/blocks/{height}/transactions", **kwds)


def process_get_block_transactions(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[TransactionType]:
    """
    Process the "/blocks/{height}/transactions" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return [models.Transaction.from_dto(i, network_type) for i in json]


get_block_transactions = request("get_block_transactions")


def request_get_blockchain_height(client: client.Client, **kwds):
    """
    Make "/chain/height" request.

    :param client: Wrapper for client.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get("/chain/height", **kwds)


def process_get_blockchain_height(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> int:
    """
    Process the "/chain/height" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return util.u64_from_dto(json['height'])


get_blockchain_height = request("get_blockchain_height")


def request_get_blockchain_score(client: client.Client, **kwds):
    """
    Make "/chain/score" request.

    :param client: Wrapper for client.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get("/chain/score", **kwds)


def process_get_blockchain_score(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.BlockchainScore:
    """
    Process the "/chain/score" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return models.BlockchainScore.from_dto(json, network_type)


get_blockchain_score = request("get_blockchain_score")


def request_get_diagnostic_blocks_by_height_and_limit(
    client: client.Client,
    height: int,
    limit: int,
    **kwds
):
    """
    Make "/diagnostic/blocks/{height}/limit/{limit}" request.

    :param client: Wrapper for client.
    :param height: Height of block.
    :param limit: Maximum number of blocks to return.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/diagnostic/blocks/{height}/limit/{limit}", **kwds)


def process_get_diagnostic_blocks_by_height_and_limit(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.BlockInfo]:
    """
    Process the "/diagnostic/blocks/{height}/limit/{limit}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return [models.BlockInfo.from_dto(i, network_type) for i in json]


get_diagnostic_blocks_by_height_and_limit = request("get_diagnostic_blocks_by_height_and_limit")


def request_get_diagnostic_storage(client: client.Client, **kwds):
    """
    Make "/diagnostic/storage" request.

    :param client: Wrapper for client.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get("/diagnostic/storage", **kwds)


def process_get_diagnostic_storage(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.BlockchainStorageInfo:
    """
    Process the "/diagnostic/storage" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return models.BlockchainStorageInfo.from_dto(json, network_type)


get_diagnostic_storage = request("get_diagnostic_storage")

# MOSAIC HTTP
# -----------


def request_get_mosaic(
    client: client.Client,
    id: models.MosaicId,
    **kwds
):
    """
    Make "/mosaic/{id}" request.

    :param client: Wrapper for client.
    :param id: Mosaic ID to request info for.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/mosaic/{id:x}", **kwds)


def process_get_mosaic(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.MosaicName]:
    """
    Process the "/mosaic/{id}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return models.MosaicInfo.from_dto(json, network_type)


get_mosaic = request("get_mosaic")


def request_get_mosaics(
    client: client.Client,
    ids: typing.Sequence[models.MosaicId],
    **kwds
):
    """
    Make "/mosaic" request.

    :param client: Wrapper for client.
    :param ids: Mosaic IDs to request names for.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    json = {"mosaicIds": [f"{i:x}" for i in ids]}
    return client.post("/mosaic", json=json, **kwds)


def process_get_mosaics(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.MosaicName]:
    """
    Process the "/mosaic" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return [models.MosaicInfo.from_dto(i, network_type) for i in json]


get_mosaics = request("get_mosaics")


def request_get_mosaic_names(
    client: client.Client,
    ids: typing.Sequence[models.MosaicId],
    **kwds
):
    """
    Make "/mosaic/names" request.

    :param client: Wrapper for client.
    :param ids: Mosaic IDs to request names for.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    json = {"mosaicIds": [f"{i:x}" for i in ids]}
    return client.post("/mosaic/names", json=json, **kwds)


def process_get_mosaic_names(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.MosaicName]:
    """
    Process the "/mosaic/names" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return [models.MosaicName.from_dto(i, network_type) for i in json]


get_mosaic_names = request("get_mosaic_names")

# NAMESPACE HTTP
# --------------


def request_get_namespace(
    client: client.Client,
    namespace_id: models.NamespaceId,
    **kwds
):
    """
    Make "/namespace/{namespace_id}" request.

    :param client: Wrapper for client.
    :param id: Namespace ID.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/namespace/{namespace_id:x}", **kwds)


def process_get_namespace(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.NamespaceInfo:
    """
    Process the "/namespace/{namespace_id}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return models.NamespaceInfo.from_dto(json, network_type)


get_namespace = request("get_namespace")


def request_get_namespace_names(
    client: client.Client,
    ids: typing.Sequence[models.NamespaceId],
    **kwds
):
    """
    Make "/namespace/names" request.

    :param client: Wrapper for client.
    :param ids: Namespace IDs to request names for.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    json = {"namespaceIds": [f"{i:x}" for i in ids]}
    return client.post("/namespace/names", json=json, **kwds)


def process_get_namespace_names(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.NamespaceName]:
    """
    Process the "/namespace/names" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return [models.NamespaceName.from_dto(i, network_type) for i in json]


get_namespace_names = request("get_namespace_names")


def request_get_namespaces_from_account(
    client: client.Client,
    address: models.Address,
    **kwds
):
    """
    Make "/account/{address}/namespaces" request.

    :param client: Wrapper for client.
    :param address: Account address.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/account/{address.address}/namespaces", **kwds)


def process_get_namespaces_from_account(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.NamespaceInfo]:
    """
    Process the "/account/{address}/namespaces" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return [models.NamespaceInfo.from_dto(i, network_type) for i in json]


get_namespaces_from_account = request("get_namespaces_from_account")


def request_get_namespaces_from_accounts(
    client: client.Client,
    addresses: typing.Sequence[models.Address],
    **kwds
):
    """
    Make "/account/namespaces" request.

    :param client: Wrapper for client.
    :param addresses: Sequence of account addresses.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    json = {"addresses": [i.address for i in addresses]}
    return client.post("/account/namespaces", json=json, **kwds)


def process_get_namespaces_from_accounts(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.NamespaceInfo]:
    """
    Process the "/account/namespaces" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return [models.NamespaceInfo.from_dto(i, network_type) for i in json]


get_namespaces_from_accounts = request("get_namespaces_from_accounts")


def request_get_linked_mosaic_id(
    client: client.Client,
    namespace_id: models.NamespaceId,
    **kwds
):
    """
    Make "/namespace/{namespace_id}" request.

    :param client: Wrapper for client.
    :param id: Namespace ID.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return request_get_namespace(client, namespace_id, **kwds)


def process_get_linked_mosaic_id(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.MosaicId:
    """
    Process the "/namespace/{namespace_id}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    namespace_info = process_get_namespace(status, json, network_type)
    return namespace_info.alias.mosaic_id


get_linked_mosaic_id = request("get_linked_mosaic_id")


def request_get_linked_address(
    client: client.Client,
    namespace_id: models.NamespaceId,
    **kwds
):
    """
    Make "/namespace/{namespace_id}" request.

    :param client: Wrapper for client.
    :param id: Namespace ID.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return request_get_namespace(client, namespace_id, **kwds)


def process_get_linked_address(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.Address:
    """
    Process the "/namespace/{namespace_id}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    namespace_info = process_get_namespace(status, json, network_type)
    return namespace_info.alias.address


get_linked_address = request("get_linked_address")

# NETWORK HTTP
# ------------

NETWORK_TYPE = {
    # TODO(ahuszagh) Only the mijinTest variant is actually defined.
    # The rest are borrowed from an outdated SDK.
    'mijin': models.NetworkType.MIJIN,
    'mijinTest': models.NetworkType.MIJIN_TEST,
    'public': models.NetworkType.MAIN_NET,
    'publicTest': models.NetworkType.TEST_NET,
}


def request_get_network_type(client: client.Client, **kwds):
    """
    Make "/network" request.

    :param client: Wrapper for client.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get("/network", **kwds)


def process_get_network_type(
    status: int,
    json: dict,
    network_type: OptionalNetworkType,
) -> models.NetworkType:
    """
    Process the "/network" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return NETWORK_TYPE[json['name']]


get_network_type = request("get_network_type")

# TRANSACTION HTTP
# ----------------


def request_get_transaction(client: client.Client, hash: str, **kwds):
    """
    Make "/transaction/{hash}" request.

    :param client: Wrapper for client.
    :param hash: Transaction hash.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/transaction/{hash}", **kwds)


def process_get_transaction(
    status: int,
    json: dict,
    network_type: models.NetworkType,
):
    """
    Process the "/transaction/{hash}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return models.Transaction.from_dto(json, network_type)


get_transaction = request("get_transaction")


def request_get_transactions(
    client: client.Client,
    hashes: typing.Sequence[str],
    **kwds
):
    """
    Make "/transaction/{hash}" request.

    :param client: Wrapper for client.
    :param hashes: Sequence of transaction hashes.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/transaction/{hash}", **kwds)


def process_get_transactions(
    status: int,
    json: list,
    network_type: models.NetworkType,
):
    """
    Process the "/transaction/{hash}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return [models.Transaction.from_dto(i, network_type) for i in json]


get_transactions = request("get_transactions")


def request_get_transaction_status(
    client: client.Client,
    hash: str,
    **kwds
):
    """
    Make "/transaction/{hash}/status" request.

    :param client: Wrapper for client.
    :param hash: Transaction hash.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    return client.get(f"/transaction/{hash}/status", **kwds)


def process_get_transaction_status(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.TransactionStatus:
    """
    Process the "/transaction/{hash}/status" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return models.TransactionStatus.from_dto(json, network_type)


get_transaction_status = request("get_transaction_status")


def request_get_transaction_statuses(
    client: client.Client,
    hashes: typing.Sequence[str],
    **kwds
):
    """
    Make "/transaction/statuses" request.

    :param client: Wrapper for client.
    :param hashes: Sequence of transaction hashes.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    json = {'hashes': list(hashes)}
    return client.post(f"/transaction/statuses", json=json, **kwds)


def process_get_transaction_statuses(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.TransactionStatus]:
    """
    Process the "/transaction/statuses" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return [models.TransactionStatus.from_dto(i, network_type) for i in json]


get_transaction_statuses = request("get_transaction_statuses")


def request_announce(
    client: client.Client,
    transaction: models.SignedTransaction,
    **kwds
):
    """
    Make "/transaction/sync" request.

    :param client: Wrapper for client.
    :param transaction: Signed transaction data.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    json = {'payload': transaction.payload}
    return client.put(f"/transaction", json=json, **kwds)


def process_announce(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.TransactionAnnounceResponse:
    """
    Process the "/transaction/sync" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return models.TransactionAnnounceResponse.from_dto(json)


announce = request("announce")


def request_announce_sync(
    client: client.Client,
    transaction: models.SignedTransaction,
    **kwds
):
    """
    Make "/transaction/sync" request.

    :param client: Wrapper for client.
    :param transaction: Signed transaction data.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    sync = models.SyncAnnounce.create(transaction)
    json = sync.to_dto()
    return client.post(f"/transaction/sync", json=json, **kwds)


def process_announce_sync(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> typing.Union[models.Transaction, models.TransactionStatus]:
    """
    Process the "/transaction/sync" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    if 'status' in json:
        json.setdefault('group', 'failed')
        json.setdefault('height', [0, 0])
        return models.TransactionStatus.from_dto(json)
    return models.Transaction.from_dto(json)


announce_sync = request("announce_sync")

# FORWARDERS
# ----------

REQUEST = {
    # ACCOUNT
    'get_account_info': request_get_account_info,
    'get_accounts_info': request_get_accounts_info,
    'get_account_property': request_get_account_property,
    'get_account_properties': request_get_account_properties,
    'get_multisig_account_info': request_get_multisig_account_info,
    'get_multisig_account_graph_info': request_get_multisig_account_graph_info,
    'get_account_transactions': request_get_account_transactions,
    'get_account_incoming_transactions': request_get_account_incoming_transactions,
    'get_account_outgoing_transactions': request_get_account_outgoing_transactions,
    'get_account_unconfirmed_transactions': request_get_account_unconfirmed_transactions,
    'get_account_partial_transactions': request_get_account_partial_transactions,

    # BLOCKCHAIN
    'get_block_by_height': request_get_block_by_height,
    'get_blocks_by_height_and_limit': request_get_blocks_by_height_and_limit,
    'get_block_transactions': request_get_block_transactions,
    'get_blockchain_height': request_get_blockchain_height,
    'get_blockchain_score': request_get_blockchain_score,
    'get_diagnostic_blocks_by_height_and_limit': request_get_diagnostic_blocks_by_height_and_limit,
    'get_diagnostic_storage': request_get_diagnostic_storage,

    # MOSAIC
    'get_mosaic': request_get_mosaic,
    'get_mosaics': request_get_mosaics,
    'get_mosaic_names': request_get_mosaic_names,

    # NAMESPACE
    'get_namespace': request_get_namespace,
    'get_namespace_names': request_get_namespace_names,
    'get_namespaces_from_account': request_get_namespaces_from_account,
    'get_namespaces_from_accounts': request_get_namespaces_from_accounts,
    'get_linked_mosaic_id': request_get_linked_mosaic_id,
    'get_linked_address': request_get_linked_address,

    # NETWORK
    'get_network_type': request_get_network_type,

    # TRANSACTOON
    'get_transaction': request_get_transaction,
    'get_transactions': request_get_transactions,
    'get_transaction_status': request_get_transaction_status,
    'get_transaction_statuses': request_get_transaction_statuses,
    'announce': request_announce,
    'announce_sync': request_announce_sync,
}

PROCESS = {
    # ACCOUNT
    'get_account_info': process_get_account_info,
    'get_accounts_info': process_get_accounts_info,
    'get_account_property': process_get_account_property,
    'get_account_properties': process_get_account_properties,
    'get_multisig_account_info': process_get_multisig_account_info,
    'get_multisig_account_graph_info': process_get_multisig_account_graph_info,
    'get_account_transactions': process_get_account_transactions,
    'get_account_incoming_transactions': process_get_account_incoming_transactions,
    'get_account_outgoing_transactions': process_get_account_outgoing_transactions,
    'get_account_unconfirmed_transactions': process_get_account_unconfirmed_transactions,
    'get_account_partial_transactions': process_get_account_partial_transactions,

    # BLOCKCHAIN
    'get_block_by_height': process_get_block_by_height,
    'get_blocks_by_height_and_limit': process_get_blocks_by_height_and_limit,
    'get_block_transactions': process_get_block_transactions,
    'get_blockchain_height': process_get_blockchain_height,
    'get_blockchain_score': process_get_blockchain_score,
    'get_diagnostic_blocks_by_height_and_limit': process_get_diagnostic_blocks_by_height_and_limit,
    'get_diagnostic_storage': process_get_diagnostic_storage,

    # MOSAIC
    'get_mosaic': process_get_mosaic,
    'get_mosaics': process_get_mosaics,
    'get_mosaic_names': process_get_mosaic_names,

    # NAMESPACE
    'get_namespace': process_get_namespace,
    'get_namespace_names': process_get_namespace_names,
    'get_namespaces_from_account': process_get_namespaces_from_account,
    'get_namespaces_from_accounts': process_get_namespaces_from_accounts,
    'get_linked_mosaic_id': process_get_linked_mosaic_id,
    'get_linked_address': process_get_linked_address,

    # NETWORK
    'get_network_type': process_get_network_type,

    # TRANSACTOON
    'get_transaction': process_get_transaction,
    'get_transactions': process_get_transactions,
    'get_transaction_status': process_get_transaction_status,
    'get_transaction_statuses': process_get_transaction_statuses,
    'announce': process_announce,
    'announce_sync': process_announce_sync,
}
