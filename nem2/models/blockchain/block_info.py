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

import typing

from nem2 import util
from .network_type import NetworkType
from ..account.public_account import PublicAccount

MerkleTreeType = typing.Sequence[str]
OptionalMerkleTreeType = typing.Optional[MerkleTreeType]


class BlockInfo(util.Dto, util.Tie):
    """Basic information describing a block."""

    __slots__ = (
        '_hash',
        '_generation_hash',
        '_total_fee',
        '_num_transactions',
        '_signature',
        '_signer',
        '_network_type',
        '_version',
        '_type',
        '_height',
        '_timestamp',
        '_difficulty',
        '_previous_block_hash',
        '_block_transactions_hash',
        '_merkle_tree',
    )

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
        block_transactions_hash: str,
        merkle_tree: OptionalMerkleTreeType = None
    ) -> None:
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
        :param merkle_tree: (Optional) List of base64-encoded hashes to verify block.
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
        self._merkle_tree = merkle_tree

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

    @property
    def merkle_tree(self) -> OptionalMerkleTreeType:
        """Get optional list of base64-encoded hashes to verify block."""
        return self._merkle_tree

    merkleTree = util.undoc(merkle_tree)

    @util.doc(util.Tie.tie)
    def tie(self) -> tuple:
        return super().tie()

    @util.doc(util.Dto.to_dto)
    def to_dto(self) -> dict:
        data = {
            'meta': {
                'hash': self.hash,
                'generationHash': self.generation_hash,
                'totalFee': util.uint64_to_dto(self.total_fee),
                'numTransactions': self.num_transactions,
            },
            'block': {
                'signature': self.signature,
                'signer': self.signer.public_key,
                'version': self.version,
                'type': self.type,
                'height': util.uint64_to_dto(self.height),
                'timestamp': util.uint64_to_dto(self.timestamp),
                'difficulty': util.uint64_to_dto(self.difficulty),
                'previousBlockHash': self.previous_block_hash,
                'blockTransactionsHash': self.block_transactions_hash,
            },
        }
        if self.merkle_tree is not None:
            data['meta']['merkleTree'] = self.merkle_tree
        return data

    @util.doc(util.Dto.from_dto)
    @classmethod
    def from_dto(cls, data: dict) -> 'BlockInfo':
        meta = data['meta']
        block = data['block']
        version = block['version']
        network_type = NetworkType(version >> 8)
        return cls(
            hash=meta['hash'],
            generation_hash=meta['generationHash'],
            total_fee=util.dto_to_uint64(meta['totalFee']),
            num_transactions=meta['numTransactions'],
            signature=block['signature'],
            signer=PublicAccount.create_from_public_key(block['signer'], network_type),
            network_type=network_type,
            version=version,
            type=block['type'],
            height=util.dto_to_uint64(block['height']),
            timestamp=util.dto_to_uint64(block['timestamp']),
            difficulty=util.dto_to_uint64(block['difficulty']),
            previous_block_hash=block['previousBlockHash'],
            block_transactions_hash=block['blockTransactionsHash'],
            merkle_tree=meta.get('merkleTree')
        )
