"""
    block_info
    ==========

    Blockchain info describing stored data.

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

from nem2 import util


# TODO(ahuszagh) Need Dto?
class BlockchainStorageInfo(util.Tie):
    """Blockchain information describing stored data."""

    __slots__ = (
        '_num_blocks',
        '_num_transactions',
        '_num_accounts',
    )

    def __init__(self, num_blocks: int, num_transactions: int, num_accounts: int):
        """
        :param num_blocks: Number of confirmed blocks.
        :param num_transactions: Number of confirmed transactions.
        :param num_accounts: Number accounts published in the blockchain.
        """
        self._num_blocks = num_blocks
        self._num_transactions = num_transactions
        self._num_accounts = num_accounts

    @property
    def num_blocks(self):
        """Get the number of confirmed blocks."""
        return self._num_blocks

    numBlocks = util.undoc(num_blocks)

    @property
    def num_transactions(self):
        """Get the number of confirmed transactions."""
        return self._num_transactions

    numTransactions = util.undoc(num_transactions)

    @property
    def num_accounts(self):
        """Get the number accounts published in the blockchain."""
        return self._num_accounts

    numAccounts = util.undoc(num_accounts)

    @util.doc(util.Tie.tie.__doc__)
    def tie(self):
        return super().tie()
