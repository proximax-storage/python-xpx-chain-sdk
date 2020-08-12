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

# BOILERPLATE
# -----------


def synchronous_request(name, doc="", raise_for_status=True):
    """Generate wrappers for a synchronous request."""

    def f(client, network_type, *args, **kwds):
        request, process = CLIENT_CB[name]
        response = request(client, *args, **kwds)
        if raise_for_status:
            response.raise_for_status()
        status = response.status_code
        json = response.json()
        return process(status, json, network_type)

    f.__name__ = name
    f.__doc__ = doc
    f.func_name = name

    return f


def asynchronous_request(name, doc="", raise_for_status=True):
    """Generate wrappers for an asynchronous request."""

    async def f(client, network_awaitable, *args, **kwds):
        # Await the network type so if an exception is thrown, we
        # don't forget to await the awaitable.
        request, process = CLIENT_CB[name]
        network_type = await network_awaitable
        async with request(client, *args, **kwds) as response:
            if raise_for_status:
                response.raise_for_status()
            status = response.status
            json = await response.json()
            return process(status, json, network_type)

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

    url = f"/account/{address.address}"
    return client.get(url, **kwds)


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
    return models.AccountInfo.create_from_dto(json, network_type)


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

    url = "/account"
    json = {"addresses": [i.address for i in addresses]}
    return client.post(url, json=json, **kwds)


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
    return [models.AccountInfo.create_from_dto(i, network_type) for i in json]


get_accounts_info = request("get_accounts_info")


def request_get_account_properties(
    client: client.Client,
    address: models.Address,
    **kwds
):
    """
    Make "/account/{address}/properties" request.

    :param client: Wrapper for client.
    :param address: Account address.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = f"/account/{address.address}/properties"
    return client.get(url, **kwds)


def process_get_account_properties(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.AccountProperties:
    """
    Process the "/account/{address}/properties" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return models.AccountProperties.create_from_dto(json, network_type)


get_account_properties = request("get_account_properties")


def request_get_accounts_properties(
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

    url = "/account/properties"
    json = {"addresses": [i.address for i in addresses]}
    return client.post(url, json=json, **kwds)


def process_get_accounts_properties(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> typing.Sequence[models.AccountProperties]:
    """
    Process the "/account/properties" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return [models.AccountProperties.create_from_dto(i, network_type) for i in json]


get_accounts_properties = request("get_accounts_properties")


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

    url = f"/account/{address.address}/multisig"
    return client.get(url, **kwds)


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
    return models.MultisigAccountInfo.create_from_dto(json, network_type)


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

    url = f"/account/{address.address}/multisig/graph"
    return client.get(url, **kwds)


def process_get_multisig_account_graph_info(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> models.MultisigAccountInfo:
    """
    Process the "/account/{address}/multisig/graph" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return models.MultisigAccountGraphInfo.create_from_dto(json, network_type)


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

    url = f"/account/{public_account.public_key}/transactions"
    return client.get(url, **kwds)


def process_get_account_transactions(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.Transaction]:
    """
    Process the "/account/{public_key}/transactions" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return [models.Transaction.create_from_dto(i, network_type) for i in json]


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

    url = f"/account/{public_account.public_key}/transactions/incoming"
    return client.get(url, **kwds)


def process_get_account_incoming_transactions(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.Transaction]:
    """
    Process the "/account/{public_key}/transactions/incoming" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return [models.Transaction.create_from_dto(i, network_type) for i in json]


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

    url = f"/account/{public_account.public_key}/transactions/outgoing"
    return client.get(url, **kwds)


def process_get_account_outgoing_transactions(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.Transaction]:
    """
    Process the "/account/{public_key}/transactions/outgoing" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return [models.Transaction.create_from_dto(i, network_type) for i in json]


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

    url = f"/account/{public_account.public_key}/transactions/unconfirmed"
    return client.get(url, **kwds)


def process_get_account_unconfirmed_transactions(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.Transaction]:
    """
    Process the "/account/{public_key}/transactions/unconfirmed" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return [models.Transaction.create_from_dto(i, network_type) for i in json]


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

    url = f"/account/{public_account.public_key}/transactions/partial"
    return client.get(url, **kwds)


def process_get_account_partial_transactions(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.Transaction]:
    """
    Process the "/account/{public_key}/transactions/partial" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return [models.Transaction.create_from_dto(i, network_type) for i in json]


get_account_partial_transactions = request("get_account_partial_transactions")
# TODO: Check when stabilized
#
#
# def request_get_account_contracts(
#     client: client.Client,
#     public_account: models.PublicAccount,
#     **kwds
# ):
#     """
#     Make "/account/{public_key}/contracts" request.
#
#     :param client: Wrapper for client.
#     :param public_account: Public account.
#     :param timeout: (Optional) timeout for request (in seconds).
#     """
#
#     url = f"/account/{public_account.public_key}/contracts"
#     return client.get(url, **kwds)
#
#
# def process_get_account_contracts(
#     status: int,
#     json: list,
#     network_type: models.NetworkType,
# ) -> typing.Sequence[models.Transaction]:
#     """
#     Process the "/account/{public_key}/contracts" HTTP response.
#
#     :param status: Status code for HTTP response.
#     :param json: JSON data for response message.
#     :param network_type: Network type..
#     """
#
#     assert status == 200
#     return [models.ContractInfo.create_from_dto(i, network_type) for i in json]
#
#
# get_account_contracts = request("get_account_contracts")


def request_get_account_names(
    client: client.Client,
    addresses: typing.Sequence[models.Address],
    **kwds
):
    """
    Make "/account/names" request.

    :param client: Wrapper for client.
    :param addresses: Sequence of account addresses.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = "/account/names"
    json = {"addresses": [i.address for i in addresses]}
    return client.post(url, json=json, **kwds)


def process_get_account_names(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> typing.Sequence[models.AccountNames]:
    """
    Process the "/account/names" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return [models.AccountNames.create_from_dto(i, network_type) for i in json]


get_account_names = request("get_account_names")


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

    url = f"/block/{height}"
    return client.get(url, **kwds)


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
    return models.BlockInfo.create_from_dto(json, network_type)


get_block_by_height = request("get_block_by_height")


def request_get_blocks_by_height_with_limit(
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

    url = f"/blocks/{height}/limit/{limit}"
    return client.get(url, **kwds)


def process_get_blocks_by_height_with_limit(
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
    return [models.BlockInfo.create_from_dto(i, network_type) for i in json]


get_blocks_by_height_with_limit = request("get_blocks_by_height_with_limit")


def request_get_block_transactions(
    client: client.Client,
    height: int,
    **kwds
):
    """
    Make "/block/{height}/transactions" request.

    :param client: Wrapper for client.
    :param height: Height of block.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = f"/block/{height}/transactions"
    return client.get(url, **kwds)


def process_get_block_transactions(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.Transaction]:
    """
    Process the "/block/{height}/transactions" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return [models.Transaction.create_from_dto(i, network_type) for i in json]


get_block_transactions = request("get_block_transactions")


def request_get_merkle_by_hash_in_block(
    client: client.Client,
    height: int,
    hash: str,
    **kwds
):
    """
    Make "/block/{height}/transaction/{hash}/merkle" request.

    :param client: Wrapper for client.
    :param height: Height of block.
    :param hash: Transaction hash included in block.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = f"/block/{height}/transaction/{hash}/merkle"
    return client.get(url, **kwds)


def process_get_merkle_by_hash_in_block(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.MerkleProofInfo:
    """
    Process the "/block/{height}/transaction/{hash}/merkle" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return models.MerkleProofInfo.create_from_dto(json, network_type)


get_merkle_by_hash_in_block = request("get_merkle_by_hash_in_block")


def request_get_block_receipts(
    client: client.Client,
    height: int,
    **kwds
):
    """
    Make "/block/{height}/receipts" request.

    :param client: Wrapper for client.
    :param height: Height of block.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = f"/block/{height}/receipts"
    return client.get(url, **kwds)


def process_get_block_receipts(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.Statements:
    """
    Process the "/block/{height}/receipts" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return models.Statements.create_from_dto(json, network_type)


get_block_receipts = request("get_block_receipts")


def request_get_blockchain_height(client: client.Client, **kwds):
    """
    Make "/chain/height" request.

    :param client: Wrapper for client.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = "/chain/height"
    return client.get(url, **kwds)


def process_get_blockchain_height(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> int:
    """
    Process the "/chain/height" HTTP response.

    Note: The data-transfer object format for the `HeightDTO` is in
    the description for `BlockInfo`.

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

    url = "/chain/score"
    return client.get(url, **kwds)


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
    return models.BlockchainScore.create_from_dto(json, network_type)


get_blockchain_score = request("get_blockchain_score")


def request_get_diagnostic_blocks_by_height_with_limit(
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

    url = f"/diagnostic/blocks/{height}/limit/{limit}"
    return client.get(url, **kwds)


def process_get_diagnostic_blocks_by_height_with_limit(
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
    return [models.BlockInfo.create_from_dto(i, network_type) for i in json]


get_diagnostic_blocks_by_height_with_limit = request(
    "get_diagnostic_blocks_by_height_with_limit"
)


def request_get_diagnostic_storage(client: client.Client, **kwds):
    """
    Make "/diagnostic/storage" request.

    :param client: Wrapper for client.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = "/diagnostic/storage"
    return client.get(url, **kwds)


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
    return models.BlockchainStorageInfo.create_from_dto(json, network_type)


get_diagnostic_storage = request("get_diagnostic_storage")


def request_get_diagnostic_server(client: client.Client, **kwds):
    """
    Make "/diagnostic/server" request.

    :param client: Wrapper for client.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = "/diagnostic/server"
    return client.get(url, **kwds)


def process_get_diagnostic_server(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.BlockchainServerInfo:
    """
    Process the "/diagnostic/server" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return models.BlockchainServerInfo.create_from_dto(json, network_type)


get_diagnostic_server = request("get_diagnostic_server")


# TODO: Check when stabilized
# CONTRACT HTTP
# -----------
#
#
# def request_get_contracts(
#     client: client.Client,
#     addresses: typing.Sequence[models.Address],
#     **kwds
# ):
#     """
#     Make "/contract" request.
#
#     :param addresses: Sequence of account addresses.
#     """
#
#     url = f"/contract"
#     json = {"addresses": [i.address for i in addresses]}
#     return client.post(url, json=json, **kwds)
#
#
# def process_get_contracts(
#     status: int,
#     json: list,
#     network_type: models.NetworkType,
# ) -> typing.Sequence[models.ContractInfo]:
#     """
#     Process the "/contract" HTTP response.
#
#     :param status: Status code for HTTP response.
#     :param json: JSON data for response message.
#     :param network_type: Network type.
#     """
#
#     assert status == 200
#     return [models.ContractInfo.create_from_dto(i, network_type) for i in json]
#
#
# get_contracts = request("get_contracts")
#
#
# def request_get_contract(
#     client: client.Client,
#     contract_id: str,
#     **kwds
# ):
#     """
#     Make "/contract/{contract_id}" request.
#
#     :param contract_id: The account identifier.
#     """
#
#     url = f"/contract/{contract_id}"
#     return client.get(url, **kwds)
#
#
# def process_get_contract(
#     status: int,
#     json: dict,
#     network_type: models.NetworkType,
# ) -> models.ContractInfo:
#     """
#     Process the "/contract/{contract_id}" HTTP response.
#
#     :param status: Status code for HTTP response.
#     :param json: JSON data for response message.
#     :param network_type: Network type.
#     """
#
#     assert status == 200
#     return models.ContractInfo.create_from_dto(json, network_type)
#
#
# get_contract = request("get_contract")
#
#
# METADATA HTTP
# -----------


def request_get_account_metadata(
    client: client.Client,
    public_account: models.PublicAccount,
    **kwds
):
    """
    Make "/account/{public_key}/metadata" request.

    :param client: Wrapper for client.
    :param public_account: Public account.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = f"/account/{public_account.public_key}/metadata"
    return client.get(url, **kwds)


def process_get_account_metadata(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.AddressMetadataInfo:
    """
    Process the "/account/{public_key}/metadata" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return models.AddressMetadataInfo.create_from_dto(json)


get_account_metadata = request("get_account_metadata")


def request_get_mosaic_metadata(
    client: client.Client,
    mosaic_id: models.MosaicId,
    **kwds
):
    """
    Make "/mosaic/{mosaic_id}/metadata" request.

    :param client: Wrapper for client.
    :param mosaic_id: Mosaic ID.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = f"/mosaic/{mosaic_id:016x}/metadata"
    return client.get(url, **kwds)


def process_get_mosaic_metadata(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.MosaicMetadataInfo:
    """
    Process the "/mosaic/{mosaic_id}/metadata" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type..
    """

    assert status == 200
    return models.MosaicMetadataInfo.create_from_dto(json)


get_mosaic_metadata = request("get_mosaic_metadata")


def request_get_namespace_metadata(
    client: client.Client,
    namespace_id: models.NamespaceId,
    **kwds
):
    """
    Make "/namespace/{namespace_id}/metadata" request.

    :param client: Wrapper for client.
    :param id: Namespace ID.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = f"/namespace/{namespace_id:016x}/metadata"
    return client.get(url, **kwds)


def process_get_namespace_metadata(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.NamespaceMetadataInfo:
    """
    Process the "/namespace/{namespace_id}/metadata" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return models.NamespaceMetadataInfo.create_from_dto(json, network_type)


get_namespace_metadata = request("get_namespace_metadata")


def request_get_metadata(
    client: client.Client,
    metadata_id: str,
    **kwds
):
    """
    Make "/metadata/{metadata_id}" request.

    :param metadata_id: ID of metadata.
    """

    url = f"/metadata/{metadata_id}"
    return client.get(url, **kwds)


def process_get_metadata(
    status: int,
    json: dict,
    network_type: models.NetworkType,
):
    """
    Process the "/metadata/{metadata_id}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return models.MetadataInfo.create_from_dto(json)


get_metadata = request("get_metadata")


def request_get_metadatas(
    client: client.Client,
    metadata_ids: typing.Sequence[str],
    **kwds
):
    """
    Make "/metadata" request.

    """

    url = "/metadata"
    json = {"metadataIds": metadata_ids}
    return client.post(url, json=json, **kwds)


def process_get_metadatas(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.MetadataInfo]:
    """
    Process the "/metadata" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return [models.MetadataInfo.create_from_dto(i, network_type) for i in json]


get_metadatas = request("get_metadatas")


# CONFIG HTTP
# -----------


def request_get_config(
    client: client.Client,
    height: int,
    **kwds
):
    """
    Make "/config/{height}" request.

    :param height: The height of the blockchain to get config.
    """

    url = f"/config/{height}"
    return client.get(url, **kwds)


def process_get_config(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.CatapultConfig:
    """
    Process the "/config/{height}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return models.CatapultConfig.create_from_dto(json, network_type)


get_config = request("get_config")


def request_get_upgrade(
    client: client.Client,
    height: int,
    **kwds
):
    """
    Make "/upgrade/{height}" request.

    :param height: The height of the blockchain to get upgrade.
    """

    url = f"/upgrade/{height}"
    return client.get(url, **kwds)


def process_get_upgrade(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.CatapultUpgrade:
    """
    Process the "/upgrade/{height}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return models.CatapultUpgrade.create_from_dto(json, network_type)


get_upgrade = request("get_upgrade")


# NODE HTTP
# -----------


def request_get_node_info(
    client: client.Client,
    **kwds
):
    """
    Make "/node/info" request.

    """

    url = "/node/info"
    return client.get(url, **kwds)


def process_get_node_info(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.NodeInfo:
    """
    Process the "/node/info" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return models.NodeInfo.create_from_dto(json, network_type)


get_node_info = request("get_node_info")


def request_get_node_time(
    client: client.Client,
    **kwds
):
    """
    Make "/node/time" request.

    """

    url = "/node/time"
    return client.get(url, **kwds)


def process_get_node_time(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.NodeTime:
    """
    Process the "/node/time" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    :param network_type: Network type.
    """

    assert status == 200
    return models.NodeTime.create_from_dto(json, network_type)


get_node_time = request("get_node_time")


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

    url = f"/mosaic/{id:016x}"
    return client.get(url, **kwds)


def process_get_mosaic(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> typing.Sequence[models.MosaicName]:
    """
    Process the "/mosaic/{id}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return models.MosaicInfo.create_from_dto(json, network_type)


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

    url = "/mosaic"
    json = {"mosaicIds": [f"{i:016x}" for i in ids]}
    return client.post(url, json=json, **kwds)


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
    return [models.MosaicInfo.create_from_dto(i, network_type) for i in json]


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

    url = "/mosaic/names"
    json = {"mosaicIds": [f"{i:016x}" for i in ids]}
    return client.post(url, json=json, **kwds)


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
    return [models.MosaicName.create_from_dto(i, network_type) for i in json]


get_mosaic_names = request("get_mosaic_names")


def request_get_mosaic_richlist(
    client: client.Client,
    mosaic_id: str,
    **kwds
):
    """
    Make "/mosaic/{mosaic_id}/richlist" request.

    :param client: Wrapper for client.
    :param mosaic_id: Mosaic IDs to request richlist for.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = f"/mosaic/{mosaic_id}/richlist"
    return client.get(url, **kwds)


def process_get_mosaic_richlist(
    status: int,
    json: list,
    network_type: models.NetworkType,
) -> typing.Sequence[models.AccountBalance]:
    """
    Process the "/mosaic/{mosaic_id}/richlist" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return [models.AccountBalance.create_from_dto(i, network_type) for i in json]


get_mosaic_richlist = request("get_mosaic_richlist")

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

    url = f"/namespace/{namespace_id:016x}"
    return client.get(url, **kwds)


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
    return models.NamespaceInfo.create_from_dto(json, network_type)


get_namespace = request("get_namespace")


def request_get_namespaces_name(
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

    url = "/namespace/names"
    json = {"namespaceIds": [f"{i:016x}" for i in ids]}
    return client.post(url, json=json, **kwds)


def process_get_namespaces_name(
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
    return [models.NamespaceName.create_from_dto(i, network_type) for i in json]


get_namespaces_name = request("get_namespaces_name")


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

    url = f"/account/{address.address}/namespaces"
    return client.get(url, **kwds)


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
    return [models.NamespaceInfo.create_from_dto(i, network_type) for i in json]


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

    url = "/account/namespaces"
    json = {"addresses": [i.address for i in addresses]}
    return client.post(url, json=json, **kwds)


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
    return [models.NamespaceInfo.create_from_dto(i, network_type) for i in json]


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
    'mijin': models.NetworkType.MIJIN,
    'mijinTest': models.NetworkType.MIJIN_TEST,
    'public': models.NetworkType.MAIN_NET,
    'publicTest': models.NetworkType.TEST_NET,
}


def request_get_network_type(client: client.Client, **kwds):
    """
    Make "/network" request.

    Note: The data-transfer object format for the `NetworkTypeDTO` is in
    the description for `NetworkType`.

    :param client: Wrapper for client.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = "/network"
    return client.get(url, **kwds)


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

    url = f"/transaction/{hash}"
    return client.get(url, **kwds)


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
    return models.Transaction.create_from_dto(json, network_type)


get_transaction = request("get_transaction")


def request_get_transactions(
    client: client.Client,
    hashes: typing.Sequence[str],
    **kwds
):
    """
    Make "/transaction" request.

    :param client: Wrapper for client.
    :param hashes: Sequence of transaction hashes.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = "/transaction"
    json = {'transactionIds': list(hashes)}
    return client.post(url, json=json, **kwds)


def process_get_transactions(
    status: int,
    json: list,
    network_type: models.NetworkType,
):
    """
    Process the "/transaction" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return [models.Transaction.create_from_dto(i, network_type) for i in json]


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

    url = f"/transaction/{hash}/status"
    return client.get(url, **kwds)


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
    return models.TransactionStatus.create_from_dto(json, network_type)


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

    url = "/transaction/statuses"
    json = {'hashes': list(hashes)}
    return client.post(url, json=json, **kwds)


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
    return [models.TransactionStatus.create_from_dto(i, network_type) for i in json]


get_transaction_statuses = request("get_transaction_statuses")


def request_announce(
    client: client.Client,
    transaction: models.SignedTransaction,
    **kwds
):
    """
    Make "/transaction" request.

    :param client: Wrapper for client.
    :param transaction: Signed transaction data.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = "/transaction"
    json = {'payload': transaction.payload}
    return client.put(url, json=json, **kwds)


def process_announce(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.TransactionAnnounceResponse:
    """
    Process the "/transaction" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert ((status == 200) | (status == 202))
    return models.TransactionAnnounceResponse.create_from_dto(json)


announce = request("announce")


def request_announce_partial(
    client: client.Client,
    transaction: models.SignedTransaction,
    **kwds
):
    """
    Make "/transaction/partial" request.

    :param client: Wrapper for client.
    :param transaction: Signed transaction data.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = "/transaction/partial"
    json = {'payload': transaction.payload}
    return client.put(url, json=json, **kwds)


def process_announce_partial(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.TransactionAnnounceResponse:
    """
    Process the "/transaction/partial" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert ((status == 200) | (status == 202))
    return models.TransactionAnnounceResponse.create_from_dto(json)


announce_partial = request("announce_partial")


def request_announce_cosignature(
    client: client.Client,
    transaction: models.CosignatureSignedTransaction,
    **kwds
):
    """
    Make "/transaction/cosignature" request.

    :param client: Wrapper for client.
    :param transaction: Signed transaction data.
    :param timeout: (Optional) timeout for request (in seconds).
    """

    url = "/transaction/cosignature"
    json = transaction.to_dto()
    return client.put(url, json=json, **kwds)


def process_announce_cosignature(
    status: int,
    json: dict,
    network_type: models.NetworkType,
) -> models.TransactionAnnounceResponse:
    """
    Process the "/transaction/cosignature" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert ((status == 200) | (status == 202))
    return models.TransactionAnnounceResponse.create_from_dto(json)


announce_cosignature = request("announce_cosignature")


# FORWARDERS
# ----------

CLIENT_CB = {
    # ACCOUNT
    'get_account_info': (
        request_get_account_info,
        process_get_account_info,
    ),
    'get_accounts_info': (
        request_get_accounts_info,
        process_get_accounts_info,
    ),
    'get_account_properties': (
        request_get_account_properties,
        process_get_account_properties,
    ),
    'get_accounts_properties': (
        request_get_accounts_properties,
        process_get_accounts_properties,
    ),
    'get_multisig_account_info': (
        request_get_multisig_account_info,
        process_get_multisig_account_info,
    ),
    'get_multisig_account_graph_info': (
        request_get_multisig_account_graph_info,
        process_get_multisig_account_graph_info,
    ),
    'get_account_transactions': (
        request_get_account_transactions,
        process_get_account_transactions,
    ),
    'get_account_incoming_transactions': (
        request_get_account_incoming_transactions,
        process_get_account_incoming_transactions,
    ),
    'get_account_outgoing_transactions': (
        request_get_account_outgoing_transactions,
        process_get_account_outgoing_transactions,
    ),
    'get_account_unconfirmed_transactions': (
        request_get_account_unconfirmed_transactions,
        process_get_account_unconfirmed_transactions,
    ),
    'get_account_partial_transactions': (
        request_get_account_partial_transactions,
        process_get_account_partial_transactions,
    ),
    # 'get_account_contracts': (
    #   request_get_account_contracts,
    #   process_get_account_contracts,
    # ),
    'get_account_names': (
        request_get_account_names,
        process_get_account_names,
    ),

    # BLOCKCHAIN
    'get_block_by_height': (
        request_get_block_by_height,
        process_get_block_by_height,
    ),
    'get_blocks_by_height_with_limit': (
        request_get_blocks_by_height_with_limit,
        process_get_blocks_by_height_with_limit,
    ),
    'get_block_transactions': (
        request_get_block_transactions,
        process_get_block_transactions,
    ),
    'get_merkle_by_hash_in_block': (
        request_get_merkle_by_hash_in_block,
        process_get_merkle_by_hash_in_block,
    ),
    'get_block_receipts': (
        request_get_block_receipts,
        process_get_block_receipts,
    ),
    'get_blockchain_height': (
        request_get_blockchain_height,
        process_get_blockchain_height,
    ),
    'get_blockchain_score': (
        request_get_blockchain_score,
        process_get_blockchain_score,
    ),
    'get_diagnostic_blocks_by_height_with_limit': (
        request_get_diagnostic_blocks_by_height_with_limit,
        process_get_diagnostic_blocks_by_height_with_limit,
    ),
    'get_diagnostic_storage': (
        request_get_diagnostic_storage,
        process_get_diagnostic_storage,
    ),
    'get_diagnostic_server': (
        request_get_diagnostic_server,
        process_get_diagnostic_server,
    ),

    # CONTRACT
    # 'get_contract': (
    #    request_get_contract,
    #    process_get_contract,
    # ),
    # 'get_contracts': (
    #    request_get_contracts,
    #    process_get_contracts,
    # ),

    # METADATA
    'get_account_metadata': (
        request_get_account_metadata,
        process_get_account_metadata,
    ),
    'get_mosaic_metadata': (
        request_get_mosaic_metadata,
        process_get_mosaic_metadata,
    ),
    'get_namespace_metadata': (
        request_get_namespace_metadata,
        process_get_namespace_metadata,
    ),
    'get_metadata': (
        request_get_metadata,
        process_get_metadata,
    ),
    'get_metadatas': (
        request_get_metadatas,
        process_get_metadatas,
    ),

    # CONFIG
    'get_config': (
        request_get_config,
        process_get_config,
    ),
    'get_upgrade': (
        request_get_upgrade,
        process_get_upgrade,
    ),

    # NODE
    'get_node_info': (
        request_get_node_info,
        process_get_node_info,
    ),
    'get_node_time': (
        request_get_node_time,
        process_get_node_time,
    ),

    # MOSAIC
    'get_mosaic': (
        request_get_mosaic,
        process_get_mosaic,
    ),
    'get_mosaics': (
        request_get_mosaics,
        process_get_mosaics,
    ),
    'get_mosaic_names': (
        request_get_mosaic_names,
        process_get_mosaic_names,
    ),
    'get_mosaic_richlist': (
        request_get_mosaic_richlist,
        process_get_mosaic_richlist,
    ),

    # NAMESPACE
    'get_namespace': (
        request_get_namespace,
        process_get_namespace,
    ),
    'get_namespaces_name': (
        request_get_namespaces_name,
        process_get_namespaces_name,
    ),
    'get_namespaces_from_account': (
        request_get_namespaces_from_account,
        process_get_namespaces_from_account,
    ),
    'get_namespaces_from_accounts': (
        request_get_namespaces_from_accounts,
        process_get_namespaces_from_accounts,
    ),
    'get_linked_mosaic_id': (
        request_get_linked_mosaic_id,
        process_get_linked_mosaic_id,
    ),
    'get_linked_address': (
        request_get_linked_address,
        process_get_linked_address,
    ),

    # NETWORK
    'get_network_type': (
        request_get_network_type,
        process_get_network_type,
    ),

    # TRANSACTOON
    'get_transaction': (
        request_get_transaction,
        process_get_transaction,
    ),
    'get_transactions': (
        request_get_transactions,
        process_get_transactions,
    ),
    'get_transaction_status': (
        request_get_transaction_status,
        process_get_transaction_status,
    ),
    'get_transaction_statuses': (
        request_get_transaction_statuses,
        process_get_transaction_statuses,
    ),
    'announce': (
        request_announce,
        process_announce,
    ),
    'announce_partial': (
        request_announce_partial,
        process_announce_partial,
    ),
    'announce_cosignature': (
        request_announce_cosignature,
        process_announce_cosignature,
    ),
}
