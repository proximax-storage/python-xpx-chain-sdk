"""
    async_http
    ==========

    Asynchronous NIS client.

    The core HTTP client shares a global session, to share a connection
    pool to speed up requests.

    Example
    -------

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

from nem2 import models, util
from . import codes
from . import nis
from .host import Host


def factory(callback):
    """Factory to create the asynchronous HTTP clients."""

    class AsyncHttp:
        """Main client for the asynchronous NIS API."""

        def __init__(self, endpoint: str) -> None:
            """
            :param endpoint: Domain name and port for the endpoint.
            """
            self._host = callback(endpoint)
            self._account = AsyncAccountHttp.from_host(self._host)

        @classmethod
        def from_host(cls, host: Host) -> 'AsyncHttp':
            """
            Initialize AsyncHttp directly from existing host.
            For internal use, do not use directly.

            :param host: Wrapper for the HTTP client.
            """
            http = cls.__new__(cls)
            http._host = host
            http.account = AsyncAccountHttp.from_host(self._host)
            return http

        @property
        def account(self) -> 'AsyncAccountHttp':
            """Get AsyncAccountHttp to the same endpoint."""
            return self._account

        @util.observable
        async def heartbeat(self, timeout=None) -> codes.Heartbeat:
            """
            Determines if NIS is up and responsive.

            :param timeout: (optional) Timeout for request (in seconds).
            """

            return await nis.async_heartbeat(self._host, timeout=timeout)

        @util.observable
        async def status(self, timeout=None) -> codes.Status:
            """
            Determines the status of NIS.

            :param timeout: (optional) Timeout for request (in seconds).
            """

            return await nis.async_status(self._host, timeout=timeout)

    class AsyncAccountHttp:
        """Account client for the asynchronous NIS API."""

        def __init__(self, endpoint: str) -> None:
            """
            :param endpoint: Domain name and port for the endpoint.
            """
            self._host = callback(endpoint)

        @classmethod
        def from_host(cls, host: Host) -> 'AsyncAccountHttp':
            """
            Initialize AsyncAccountHttp directly from existing host.
            For internal use, do not use directly.

            :param host: Wrapper for the HTTP client.
            """
            account = cls.__new__(cls)
            account._host = host
            return account

        def generate(self, timeout=None):
            raise NotImplementedError

        def get(self, address, timeout=None):
            """
            Gets an AccountMetaDataPair for an account.

            :param address: The address of the account (`Address` or `str`).
            :param timeout: (optional) Timeout for request (in seconds).
            """
            if isinstance(address, str):
                address = models.Address.create_from_raw_address(address)
            plain = address.plain()
            return nis.async_account_get(self._host, plain, timeout=timeout)

    return AsyncHttp, AsyncAccountHttp
