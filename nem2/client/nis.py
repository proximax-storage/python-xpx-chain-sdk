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
from enum import IntEnum

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

# HTTP
# ----

# HEARTBEAT

class Heartbeat(IntEnum):
    """Enumerations for the status of a "/heartbeat" request."""

    UNKNOWN = 0
    OK = 1

    def description(self) -> str:
        """Describe the enumeration value."""

        return HEARTBEAT_DESCRIPTION[self]

HEARTBEAT_DESCRIPTION = {
    Heartbeat.UNKNOWN: "Unknown status.",
    Heartbeat.OK: "NIS is ok.",
}


def request_heartbeat(host, timeout=None):
    """
    Make "/heartbeat" request.

    :param host: Host wrapper for client.
    :param timeout: (optional) Timeout for request (in seconds).
    """

    return host.get("/heartbeat", timeout=timeout)


def process_heartbeat(status, json):
    """
    Process the "/heartbeat" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    # /heartbeat always succeeds if the node is up.
    # If we get any other status code, return an unknown status: the node
    # is accepting requests but doesn't seem to recognize the request.
    if status == 200:
        return Heartbeat.OK
    else:
        return Heartbeat.UNKNOWN


HEARTBEAT_DOC = """
Determines if NIS is up and responsive.

:param host: Host wrapper for client.
:param timeout: (optional) Timeout for request (in seconds).
"""

heartbeat, async_heartbeat = request("heartbeat", HEARTBEAT_DOC)

# STATUS

class Status(IntEnum):
    """Enumerations for the status of a "/status" request."""

    UNKNOWN = 0
    STOPPED = 1
    STARTING = 2
    RUNNING = 3
    BOOTING = 4
    BOOTED = 5
    SYNCHRONIZED = 6
    LOCAL = 7
    LOADING = 8

    def description(self) -> str:
        """Describe the enumeration value."""

        return STATUS_DESCRIPTION[self]


STATUS_DESCRIPTION = {
    Status.UNKNOWN: "Unknown status.",
    Status.STOPPED: "NIS is stopped.",
    Status.STARTING: "NIS is starting.",
    Status.RUNNING: "NIS is running.",
    Status.BOOTING: "NIS is booting the local node (implies NIS is running).",
    Status.BOOTED: "The local node is booted (implies NIS is running).",
    Status.SYNCHRONIZED: "The local node is synchronized (implies NIS is running and the local node is booted).",
    Status.LOCAL: "NIS local node does not see any remote NIS node (implies running and booted).",
    Status.LOADING: "NIS is currently loading the block chain from the database. In this state NIS cannot serve any requests.",
}


def request_status(host, timeout=None):
    """
    Make "/status" request.

    :param host: Host wrapper for client.
    :param timeout: (optional) Timeout for request (in seconds).
    """

    return host.get("/status", timeout=timeout)


def process_status(status, json):
    """
    Process the "/status" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    # /status always succeeds if the node is up and serving requests.
    # If we get any other status code, return an unknown status: the node
    # is accepting requests but doesn't seem to recognize the request.
    if status == 200:
        return Status(json['code'])
    else:
        return Status.UNKNOWN


STATUS_DOC = """
Determines the status of NIS.

:param host: Host wrapper for client.
:param timeout: (optional) Timeout for request (in seconds).
"""

status, async_status = request("status", STATUS_DOC)

# ACCOUNT HTTP
# -------------

def request_account_get(host, address, timeout=None):
    """
    Make "/account/get" request.

    :param host: Host wrapper for client.
    :param address: Plain base32-encoded address of account.
    :param timeout: (optional) Timeout for request (in seconds).
    """

    payload = {'address': address}
    return host.get("/account/get",
        params=payload,
        timeout=timeout
    )


def process_account_get(status, json):
    """
    Process the "/account/get" HTTP response.

    :param status: Status code for HTTP response.
    :param json: JSON data for response message.
    """

    import pdb; pdb.set_trace()
    # TODO(ahuszagh) Method succeeded, since we raise for error.
    # Need AccountInfo struct.
    raise NotImplementedError


ACCOUNT_GET_DOC = """
Gets an AccountMetaDataPair for an account..

:param host: Host wrapper for client.
:param address: Plain base32-encoded address of account.
:param timeout: (optional) Timeout for request (in seconds).
"""

account_get, async_account_get = request("account_get", ACCOUNT_GET_DOC, True)

# FORWARDERS
# ----------

REQUEST = {
    'heartbeat': request_heartbeat,
    'status': request_status,
    'account_get': request_account_get,
}

PROCESS = {
    'heartbeat': process_heartbeat,
    'status': process_status,
    'account_get': process_account_get,
}
