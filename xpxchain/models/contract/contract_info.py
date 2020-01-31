
from __future__ import annotations

import typing

from ..account.address import Address
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['ContractInfo']


@util.inherit_doc
@util.dataclass(frozen=True)
class ContractInfo(util.DTO):
    """

    :param contract: Contract info.

    DTO Format:
        .. code-block:: yaml

            ContractDTO:
                multisig: string
                multisigAddress: string
                start: UInt64DTO
                duration: UInt64DTO
                hash: string
                customers: string[]
                executors: string[]
                verifiers: string[]

            ContractInfoDTO:
                contract: ConfigDTO
    """

    multisig: str
    multisig_address: Address
    start: int
    duration: int
    hash: str
    customers: typing.Sequence[str]
    executors: typing.Sequence[str]
    verifiers: typing.Sequence[str]

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'contract'}
        required_l2 = {
            'multisig',
            'multisigAddress',
            'start',
            'duration',
            'hash',
            'customers',
            'executors',
            'verifiers'
        }
        return (
            # Level 1
            cls.validate_dto_required(data, required_l1)
            and cls.validate_dto_all(data, required_l1)
            # Level 2
            and cls.validate_dto_required(data['contract'], required_l2)
            and cls.validate_dto_all(data['contract'], required_l2)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        contract = {
            'multisig': self.multisig,
            'multisigAddress': util.hexlify(self.multisig_address.encoded),
            'start': util.u64_to_dto(self.start),
            'duration': util.u64_to_dto(self.duration),
            'hash': self.hash,
            'customers': self.customers,
            'executors': self.executors,
            'verifiers': self.verifiers
        }

        return {
            'contract': contract,
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        contract = data['contract']
        return cls(
            multisig=contract['multisig'],
            multisig_address=Address.create_from_encoded(contract['multisigAddress']),
            start=util.u64_from_dto(contract.get('start', [0, 0])),
            duration=util.u64_from_dto(contract.get('duration', [0, 0])),
            hash=contract['hash'],
            customers=contract['customers'],
            executors=contract['executors'],
            verifiers=contract['verifiers']
        )
