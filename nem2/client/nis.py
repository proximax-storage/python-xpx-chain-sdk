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

import inspect
import typing

from nem2 import models

# BOILERPLATE
# -----------

def synchronous_request(name, doc, raise_for_status=False):
    """Generate wrappers for a synchronous request."""

    def f(*args, **kwds):
        response = REQUEST[name](*args, **kwds)
        if raise_for_status:
            response.raise_for_status()
        status = response.status_code
        json = response.json()
        return PROCESS[name](status, json)

    f.__name__= name
    f.__doc__= doc
    f.func_name = name

    return f

def asynchronous_request(name, doc, raise_for_status=False):
    """Generate wrappers for an asynchronous request."""

    async def f(*args, **kwds):
        async with REQUEST[name](*args, **kwds) as response:
            if raise_for_status:
                response.raise_for_status()
            status = response.status
            json = await response.json()
            return PROCESS[name](status, json)

    f.__name__= "async_{}".format(name)
    f.__doc__= doc
    f.func_name = "async_{}".format(name)

    return f


def request(*args, **kwds):
    """Generate synchronous and asynchronous request wrappers."""

    s = synchronous_request(*args, **kwds)
    a = asynchronous_request(*args, **kwds)
    return s, a


# BLOCKCHAIN HTTP
# ---------------

def request_get_block_by_height(host: 'Host', height: int, timeout=None):
    """
    Make "/block/{height}" request.

    :param host: Host wrapper for client.
    :param height: Height of block.
    :param timeout: (optional) Timeout for request (in seconds).
    """

    return host.get("/block/{}".format(height), timeout=timeout)


def process_get_block_by_height(status: int, json: dict) -> 'BlockInfo':
    """
    Process the "/block/{height}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return models.BlockInfo.from_dto(json)


get_block_by_height = request("get_block_by_height", "", True)

# chain/height

# MOSAIC HTTP
# -----------

# NAMESPACE HTTP
# --------------


def request_get_namespace(host: 'Host', namespace_id: 'NamespaceId', timeout=None):
    """
    Make "/namespace/{namespace_id}" request.

    :param host: Host wrapper for client.
    :param id: Namespace ID.
    :param timeout: (optional) Timeout for request (in seconds).
    """

    return host.get("/namespace/{:x}".format(namespace_id), timeout=timeout)


def process_get_namespace(status: int, json: dict) -> 'NamespaceInfo':
    """
    Process the "/namespace/{namespace_id}" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return models.NamespaceInfo.from_dto(json)


get_namespace = request("get_namespace", "", True)


def request_get_namespace_names(host: 'Host', ids: typing.Sequence['NamespaceId'], timeout=None):
    """
    Make "/namespace/names" request.

    :param host: Host wrapper for client.
    :param ids: Namespace IDs to request names for.
    :param timeout: (optional) Timeout for request (in seconds).
    """

    json = {"namespaceIds": ["{:x}".format(i) for i in ids]}
    return host.post("/namespace/names", json=json, timeout=timeout)


def process_get_namespace_names(status: int, json: list) -> typing.Sequence['NamespaceName']:
    """
    Process the "/namespace/names" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return [models.NamespaceName.from_dto(i) for i in json]


get_namespace_names = request("get_namespace_names", "", True)

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

def request_get_network_type(host: 'Host', timeout=None):
    """
    Make "/network" request.

    :param host: Host wrapper for client.
    :param timeout: (optional) Timeout for request (in seconds).
    """

    return host.get("/network", timeout=timeout)


def process_get_network_type(status: int, json: dict) -> 'NetworkType':
    """
    Process the "/network" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    assert status == 200
    return NETWORK_TYPE[json['name']]


get_network_type = request("get_network_type", "", True)

# FORWARDERS
# ----------

REQUEST = {
    # BLOCKCHAIN
    'get_block_by_height': request_get_block_by_height,

    # NAMESPACE
    'get_namespace_names': request_get_namespace_names,
    'get_namespace': request_get_namespace,

    # NETWORK
    'get_network_type': request_get_network_type,
}

PROCESS = {
    # BLOCKCHAIN
    'get_block_by_height': process_get_block_by_height,

    # NAMESPACE
    'get_namespace_names': process_get_namespace_names,
    'get_namespace': process_get_namespace,

    # NETWORK
    'get_network_type': process_get_network_type,
}
