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

# NAMESPACE

GET_NAMESPACE_NAMES = """
Get namespace names from IDs.

:param ids: Sequence of namespace IDs.
:return: Namespace names for IDS.
"""

# NETWORK

GET_NETWORK_TYPE = """
Get network type.

:return: Network type.
"""
