"""
    documentation
    =============

    Shared docstrings between HTTP and AsyncHTTP clients.

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

# TODO(ahuszagh) Add more docstrings.

# CLIENT

INIT = """
:param endpoint: Domain name and port for the endpoint.
"""

ASYNC_INIT = """
:param endpoint: Domain name and port for the endpoint.
:param loop: (Optional) Event loop for the client.
"""

# BLOCKCHAIN

GET_BLOCK_BY_HEIGHT = """
Get block information from the block height.

:param height: Block height.
:return: Information describing block.
"""

GET_BLOCKCHAIN_HEIGHT = """
Get current blockchain height.

:return: Blockchain height.
"""

GET_BLOCKCHAIN_SCORE = """
Get current blockchain score.

:return: Blockchain score.
"""

GET_DIAGNOSTIC_STORAGE = """
Get diagnostic storage information for blockchain.

:return: Blockchain diagnostic storage information.
"""

# MOSAIC

GET_MOSAIC_NAMES = """
Get mosaic names from IDs.

:param ids: Sequence of mosaic IDs.
:return: Mosaic names for IDS.
"""

# NAMESPACE

GET_NAMESPACE = """
Get namespace information from ID.

:param id: Namespace ID.
:return: Namespace information.
"""

GET_NAMESPACES_FROM_ACCOUNT = """
Get namespaces owned by account.

:param address: Account address.
:return: List of namespace information objects.
"""

GET_NAMESPACES_FROM_ACCOUNTS = """
Get namespaces owned by accounts.

:param addresses: Sequence of account addresses.
:return: List of namespace information objects.
"""

GET_NAMESPACE_NAMES = """
Get namespace names from IDs.

:param ids: Sequence of namespace IDs.
:return: Namespace names for IDS.
"""

GET_LINKED_MOSAIC_ID = """
Get mosaic ID from linked mosaic alias.

:param id: Namespace ID.
:return: Mosaic ID.
"""

GET_LINKED_ADDRESS = """
Get address from linked address alias.

:param id: Namespace ID.
:return: Address object.
"""

# NETWORK

GET_NETWORK_TYPE = """
Get network type.

:return: Network type.
"""
