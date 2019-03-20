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

from __future__ import annotations
import typing

from nem2 import util
from .network_type import NetworkType, OptionalNetworkType
from ..account.public_account import PublicAccount

__all__ = ['BlockInfo']

MerkleTreeType = typing.Sequence[str]
OptionalMerkleTreeType = typing.Optional[MerkleTreeType]


@util.inherit_doc
@util.dataclass(frozen=True)
class BlockInfo(util.DTO):
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
    signer: PublicAccount
    network_type: NetworkType
    version: int
    type: int
    height: int
    timestamp: int
    difficulty: int
    previous_block_hash: str
    block_transactions_hash: str
    merkle_tree: OptionalMerkleTreeType

    def __init__(
        self,
        hash: typing.AnyStr,
        generation_hash: typing.AnyStr,
        total_fee: int,
        num_transactions: int,
        signature: typing.AnyStr,
        signer: PublicAccount,
        network_type: NetworkType,
        version: int,
        type: int,
        height: int,
        timestamp: int,
        difficulty: int,
        previous_block_hash: typing.AnyStr,
        block_transactions_hash: typing.AnyStr,
        merkle_tree: OptionalMerkleTreeType = None,
    ) -> None:
        hash = util.encode_hex(hash)
        generation_hash = util.encode_hex(generation_hash)
        signature = util.encode_hex(signature)
        previous_block_hash = util.encode_hex(previous_block_hash)
        block_transactions_hash = util.encode_hex(block_transactions_hash)
        self._set('hash', hash)
        self._set('generation_hash', generation_hash)
        self._set('total_fee', total_fee)
        self._set('num_transactions', num_transactions)
        self._set('signature', signature)
        self._set('signer', signer)
        self._set('network_type', network_type)
        self._set('version', version)
        self._set('type', type)
        self._set('height', height)
        self._set('timestamp', timestamp)
        self._set('difficulty', difficulty)
        self._set('previous_block_hash', previous_block_hash)
        self._set('block_transactions_hash', block_transactions_hash)
        self._set('merkle_tree', merkle_tree)

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        meta = {
            'hash': self.hash,
            'generationHash': self.generation_hash,
            'totalFee': util.u64_to_dto(self.total_fee),
            'numTransactions': self.num_transactions,
        }
        block = {
            'signature': self.signature,
            'signer': self.signer.to_dto(network_type),
            'version': self.version | (int(network_type) << 8),
            'type': self.type,
            'height': util.u64_to_dto(self.height),
            'timestamp': util.u64_to_dto(self.timestamp),
            'difficulty': util.u64_to_dto(self.difficulty),
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
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        meta = data['meta']
        block = data['block']
        version = block['version']
        network_type = NetworkType(version >> 8)
        # totalFee and merkleHash aren't provided in all interfaces,
        # such as the websockets listener.
        return cls(
            hash=meta['hash'],
            generation_hash=meta['generationHash'],
            total_fee=util.u64_from_dto(meta.get('totalFee', [0, 0])),
            num_transactions=meta.get('numTransactions', 0),
            signature=block['signature'],
            signer=PublicAccount.from_dto(block['signer'], network_type),
            network_type=network_type,
            version=version & 0xFF,
            type=block['type'],
            height=util.u64_from_dto(block['height']),
            timestamp=util.u64_from_dto(block['timestamp']),
            difficulty=util.u64_from_dto(block['difficulty']),
            previous_block_hash=block['previousBlockHash'],
            block_transactions_hash=block['blockTransactionsHash'],
            merkle_tree=meta.get('merkleTree')
        )
