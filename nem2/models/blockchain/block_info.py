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


@util.inherit_doc
@util.dataclass(frozen=True, merkle_tree=None)
class BlockInfo(util.Dto):
    """
    Basic information describing a block.

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

    hash: str
    generation_hash: str
    total_fee: int
    num_transactions: int
    signature: str
    signer: 'PublicAccount'
    network_type: 'NetworkType'
    version: int
    type: int
    height: int
    timestamp: int
    difficulty: int
    previous_block_hash: str
    block_transactions_hash: str
    merkle_tree: OptionalMerkleTreeType

    def to_dto(self) -> dict:
        meta = {
            'hash': self.hash,
            'generationHash': self.generation_hash,
            'totalFee': util.uint64_to_dto(self.total_fee),
            'numTransactions': self.num_transactions,
        }
        block = {
            'signature': self.signature,
            'signer': self.signer.public_key,
            'version': self.version,
            'type': self.type,
            'height': util.uint64_to_dto(self.height),
            'timestamp': util.uint64_to_dto(self.timestamp),
            'difficulty': util.uint64_to_dto(self.difficulty),
            'previousBlockHash': self.previous_block_hash,
            'blockTransactionsHash': self.block_transactions_hash,
        }

        if self.merkle_tree is not None:
            meta['merkleTree'] = self.merkle_tree

        return {
            'meta': meta,
            'block': block,
        }

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
