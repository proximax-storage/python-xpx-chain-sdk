"""
    documentation
    =============

    Shared docstrings between HTTP and AsyncHTTP clients.
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
