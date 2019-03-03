"""
    block_info
    ==========

    Block data and metadata pair.

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
from .network_type import NetworkType
from ..account.public_account import PublicAccount


class BlockInfo(util.Dto):
    """Basic information describing a NEM block."""

    def __init__(self,
        hash: str,
        generation_hash: str,
        total_fee: int,
        num_transactions: int,
        signature: str,
        signer: 'PublicAccount',
        network_type: 'NetworkType',
        version: int,
        type: int,
        height: int,
        timestamp: int,
        difficulty: int,
        previous_block_hash: str,
        block_transactions_hash: str
    ):
        """
        :param hash: Block hash.
        :param generation_hash: Generation hash.
        :param total_fee: Sum of all transaction fees included in block.
        :param num_transactions: The number of transactions included in block.
        :param signature: Block signature.
        :param signer: Public account of the block harvester.
        :param network_type: Network type.
        :param version: Transaction version.
        :param type: Block type.
        :param height: Height at which block was confirmed.
        :param timestamp: Seconds elapsed since nemesis block.
        :param difficulty: POI difficult to harvest block.
        :param previous_block_hash: Last block hash.
        :param block_transactions_hash: Block transaction hash.
        """
        self._hash = hash
        self._generation_hash = generation_hash
        self._total_fee = total_fee
        self._num_transactions = num_transactions
        self._signature = signature
        self._signer = signer
        self._network_type = network_type
        self._version = version
        self._type = type
        self._height = height
        self._timestamp = timestamp
        self._difficulty = difficulty
        self._previous_block_hash = previous_block_hash
        self._block_transactions_hash = block_transactions_hash

    @property
    def hash(self) -> str:
        """Get the block hash."""
        return self._hash

    @property
    def generation_hash(self) -> str:
        """Get the generation hash."""
        return self._generation_hash

    generationHash = util.undoc(generation_hash)

    @property
    def total_fee(self) -> int:
        """Get the sum of all transaction fees included in block."""
        return self._total_fee

    totalFee = util.undoc(total_fee)

    @property
    def num_transactions(self) -> int:
        """Get the number of transactions included in block."""
        return self._num_transactions

    numTransactions = util.undoc(num_transactions)

    @property
    def signature(self) -> str:
        """Get the block signature."""
        return self._signature

    @property
    def signer(self) -> 'PublicAccount':
        """Get the public account of the block harvester."""
        return self._signer

    @property
    def network_type(self) -> 'NetworkType':
        """Get the network type."""
        return self._network_type

    networkType = util.undoc(network_type)

    @property
    def version(self) -> int:
        """Get the transaction version."""
        return self._version

    @property
    def type(self) -> int:
        """Get the block type."""
        return self._type

    @property
    def height(self) -> int:
        """Get the height at which block was confirmed."""
        return self._height

    @property
    def timestamp(self) -> int:
        """Get the seconds elapsed since nemesis block."""
        return self._timestamp

    @property
    def difficulty(self) -> int:
        """Get the POI difficult to harvest block."""
        return self._difficulty

    @property
    def previous_block_hash(self) -> str:
        """Get the last block hash."""
        return self._previous_block_hash

    previousBlockHash = util.undoc(previous_block_hash)

    @property
    def block_transactions_hash(self) -> str:
        """Get the block transaction hash."""
        return self._block_transactions_hash

    blockTransactionsHash = util.undoc(block_transactions_hash)

    # TODO(ahuszagh)
    # tie
    # __repr__
    # __str__
    # __eq__

    @util.doc(util.Dto.to_dto.__doc__)
    def to_dto(self) -> dict:
        return {
            'meta': {
                'hash': self.hash,
                'generationHash': self.generation_hash,
                'totalFee': util.uint64_to_dto(self.total_fee),
                'numTransactions': self.num_transactions,
            },
            'block': {
                'signature': self.signature,
                'signer': self.signer.public_key,
                'type': self.type,
                'height': util.uint64_to_dto(self.height),
                'timestamp': util.uint64_to_dto(self.timestamp),
                'difficulty': util.uint64_to_dto(self.difficulty),
                'previousBlockHash': self.previous_block_hash,
                'blockTransactionsHash': self.block_transactions_hash,
            },
        }

    @util.doc(util.Dto.from_dto.__doc__)
    @classmethod
    def from_dto(cls, data: dict) -> 'BlockInfo':
        version = data['block']['version']
        network_type = NetworkType(version >> 8)
        return cls(
            hash=data['meta']['hash'],
            generation_hash=data['meta']['generationHash'],
            total_fee=util.dto_to_uint64(data['meta']['totalFee']),
            num_transactions=data['meta']['numTransactions'],
            signature=data['block']['signature'],
            signer=PublicAccount.create_from_public_key(data['block']['signer'], network_type),
            network_type=network_type,
            version=version,
            type=data['block']['type'],
            height=util.dto_to_uint64(data['block']['height']),
            timestamp=util.dto_to_uint64(data['block']['timestamp']),
            difficulty=util.dto_to_uint64(data['block']['difficulty']),
            previous_block_hash=data['block']['previousBlockHash'],
            block_transactions_hash=data['block']['blockTransactionsHash'],
        )
