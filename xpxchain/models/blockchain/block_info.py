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

from .block_type import BlockType
from .network_type import NetworkType, OptionalNetworkType
from ..account.public_account import PublicAccount
from ..transaction.transaction_version import TransactionVersion
from ... import util

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
    :param num_statements: The number of statements included in block.
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
    :param block_receipts_hash: Block receipt hash.
    :param state_hash: State hash.
    :param beneficiary: (Optional) Public account of beneficiary.

    DTO Format:
        .. code-block:: yaml

            HeightDTO:
                height: UInt64DTO

            BlockMetaDTO:
                # Hex(Hash) (64-bytes)
                hash: string
                # Hex(Hash) (64-bytes)
                generationHash: string
                totalFee: UInt64DTO
                numTransactions: integer
                # Hex(Hash)[] (64-bytes)
                subCacheMerkleRoots?: string[]

            BlockDTO:
                # Hex(Signature) (128-bytes)
                signature: string
                # Hex(PublicKey) (64-bytes)
                signer: string
                version: integer
                type: integer
                height: UInt64DTO
                timestamp: UInt64DTO
                difficulty: UInt64DTO
                feeMultiplier: integer
                # Hex(Hash) (64-bytes)
                previousBlockHash: string
                # Hex(Hash) (64-bytes)
                blockTransactionsHash: string
                # Hex(Hash) (64-bytes)
                blockReceiptsHash: string
                # Hex(Hash) (64-bytes)
                stateHash: string
                # Hex(PublicKey) (64-bytes)
                beneficiaryPublicKey: string

            BlockInfoDTO:
                meta: BlockMetaDTO
                block: BlockDTO
    """

    hash: str
    generation_hash: str
    total_fee: int
    num_transactions: int
    num_statements: int
    signature: str
    signer: PublicAccount
    network_type: NetworkType
    version: TransactionVersion
    type: BlockType
    height: int
    timestamp: int
    difficulty: int
    fee_multiplier: int
    previous_block_hash: str
    block_transactions_hash: str
    block_receipts_hash: str
    state_hash: str
    beneficiary: typing.Optional[PublicAccount]
    fee_interest: int
    fee_interest_denominator: int
    merkle_tree: OptionalMerkleTreeType

    def __init__(
        self,
        hash: typing.AnyStr,
        generation_hash: typing.AnyStr,
        total_fee: int,
        num_transactions: int,
        num_statements: int,
        signature: typing.AnyStr,
        signer: PublicAccount,
        network_type: NetworkType,
        version: TransactionVersion,
        type: BlockType,
        height: int,
        timestamp: int,
        difficulty: int,
        fee_multiplier: int,
        previous_block_hash: typing.AnyStr,
        block_transactions_hash: typing.AnyStr,
        block_receipts_hash: typing.AnyStr,
        state_hash: typing.AnyStr,
        fee_interest: int,
        fee_interest_denominator: int,
        beneficiary: typing.Optional[PublicAccount] = None,
        merkle_tree: OptionalMerkleTreeType = None,
    ) -> None:
        hash = util.encode_hex(hash)
        generation_hash = util.encode_hex(generation_hash)
        signature = util.encode_hex(signature)
        previous_block_hash = util.encode_hex(previous_block_hash)
        block_transactions_hash = util.encode_hex(block_transactions_hash)
        block_receipts_hash = util.encode_base64(block_receipts_hash)
        state_hash = util.encode_hex(state_hash)
        self._set('hash', hash)
        self._set('generation_hash', generation_hash)
        self._set('total_fee', total_fee)
        self._set('num_transactions', num_transactions)
        self._set('num_statements', num_statements)
        self._set('signature', signature)
        self._set('signer', signer)
        self._set('network_type', network_type)
        self._set('version', version)
        self._set('type', type)
        self._set('height', height)
        self._set('timestamp', timestamp)
        self._set('difficulty', difficulty)
        self._set('fee_multiplier', fee_multiplier)
        self._set('previous_block_hash', previous_block_hash)
        self._set('block_transactions_hash', block_transactions_hash)
        self._set('block_receipts_hash', block_receipts_hash)
        self._set('state_hash', state_hash)
        self._set('fee_interest', fee_interest)
        self._set('fee_interest_denominator', fee_interest_denominator)
        self._set('beneficiary', beneficiary)
        self._set('merkle_tree', merkle_tree or [])

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'meta', 'block'}
        required_l21 = {
            'hash',
            'generationHash'
            # 'subCacheMerkleRoots',
            # 'totalFee',
            # 'numTransactions',
            # 'numStatements'
        }
        required_l22 = {
            'signature',
            'signer',
            'version',
            'type',
            'height',
            'timestamp',
            'difficulty',
            'previousBlockHash',
            'blockTransactionsHash'
            # 'feeMultiplier',
            # 'blockReceiptsHash',
            # 'stateHash',
            # 'beneficiary',
            # 'feeInterest',
            # 'feeInterestDenominator'
        }

        return (
            # Level 1
            cls.validate_dto_required(data, required_l1)
            and cls.validate_dto_all(data, required_l1)
            # Level 2_1
            and cls.validate_dto_required(data['meta'], required_l21)
            # and cls.validate_dto_all(data['meta'], required_l21)
            # Level 2_2
            and cls.validate_dto_required(data['block'], required_l22)
            # and cls.validate_dto_all(data['block'], required_l22)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        meta = {
            'hash': self.hash,
            'generationHash': self.generation_hash,
            'subCacheMerkleRoots': self.merkle_tree,
            'totalFee': util.u64_to_dto(self.total_fee),
            'numTransactions': self.num_transactions,
            'numStatements': self.num_statements,
        }
        block = {
            'signature': self.signature,
            'signer': self.signer.public_key,
            'version': int(self.version) | (int(network_type) << 24),
            'type': self.type.to_dto(network_type),
            'height': util.u64_to_dto(self.height),
            'timestamp': util.u64_to_dto(self.timestamp),
            'difficulty': util.u64_to_dto(self.difficulty),
            'feeMultiplier': util.u32_to_dto(self.fee_multiplier),
            'previousBlockHash': self.previous_block_hash,
            'blockTransactionsHash': self.block_transactions_hash,
            'blockReceiptsHash': self.block_receipts_hash,
            'stateHash': self.state_hash,
            'feeInterest': self.fee_interest,
            'feeInterestDenominator': self.fee_interest_denominator
        }

        if self.beneficiary is not None:
            public_key = util.unhexlify(self.beneficiary.public_key)
            meta['beneficiary'] = util.b64encode(public_key)

        return {
            'meta': meta,
            'block': block,
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        meta = data['meta']
        block = data['block']
        version = block['version']
        network_type = NetworkType((version >> 24) & 0x000000FF)
        beneficiary = None
        if 'beneficiary' in block:
            # TODO(ahuszagh) Is base64-encoded rather than hex-encoded.
            #   Should be fixed in an upcoming version.
            beneficiary = PublicAccount.create_from_public_key(block['beneficiary'], network_type)
        return cls(
            hash=meta['hash'],
            generation_hash=meta['generationHash'],
            merkle_tree=meta.get('subCacheMerkleRoots', []),
            total_fee=util.u64_from_dto(meta.get('totalFee', [0, 0])),
            num_transactions=meta.get('numTransactions', 0),
            num_statements=meta.get('numStatements', 1),
            signature=block['signature'],
            signer=PublicAccount.create_from_public_key(block['signer'], network_type),
            version=TransactionVersion(version & 0xFFFFFF),  # Version are 3B
            type=BlockType.create_from_dto(block['type'], network_type),
            height=util.u64_from_dto(block['height']),
            timestamp=util.u64_from_dto(block['timestamp']),
            difficulty=util.u64_from_dto(block['difficulty']),
            previous_block_hash=block['previousBlockHash'],
            block_transactions_hash=block['blockTransactionsHash'],
            network_type=network_type,
            fee_multiplier=util.u32_from_dto(block.get('feeMultiplier', 0)),
            block_receipts_hash=block.get('blockReceiptsHash', ''),
            state_hash=block.get('stateHash', ''),
            beneficiary=beneficiary,
            fee_interest=block.get('feeInterest', 0),
            fee_interest_denominator=block.get('feeInterestDenominator', 0)
        )
