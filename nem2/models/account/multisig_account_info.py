"""
    multisig_account_info
    =====================

    Describes multisig account and the levels the account is involved in.

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

from .address import Address
from .public_account import PublicAccount, PublicAccountList
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['MultisigAccountInfo']


@util.inherit_doc
@util.dataclass(frozen=True)
class MultisigAccountInfo(util.DTO):
    """
    Information describing a multisig account.

    Multisig accounts allow multiple accounts, or signatories,
    operate as an entity, requiring a certain consensus for operations.

    :param account: Multisig public account.
    :param min_approval: Min number of cosignatories required to approve a transaction.
    :param min_removal: Min number of cosignatories required to remove a cosignatory.
    :param cosignatories: List of cosignatories.
    :param multisig_accounts: List of multisig accounts this account cosigns.


    DTO Format:
        .. code-block:: yaml

            MultisigDTO:
                # Hex(PublicKey) (64-bytes)
                account: string
                # Hex(Address) (50-bytes)
                accountAddress: string
                minApproval: integer
                minRemoval: integer
                # Hex(PublicKey)[] (64-bytes)
                cosignatories: string[]
                # Hex(PublicKey)[] (64-bytes)
                multisigAccounts: string[]

            MultisigAccountInfoDTO:
                multisig: MultisigDTO
    """

    account: PublicAccount
    min_approval: int
    min_removal: int
    cosignatories: PublicAccountList
    multisig_accounts: PublicAccountList

    def is_multisig(self) -> bool:
        """Get if account is a multisig account."""

        return self.min_removal != 0 and self.min_approval != 0

    def has_cosigner(self, account: PublicAccount) -> bool:
        """
        Check if another account is cosignatory of multisig account.

        :param account: Other account.
        """

        return account in self.cosignatories

    def is_cosigner_of_multisig_account(self, account: PublicAccount) -> bool:
        """
        Check if multisig account is cosignatory of another account.

        :param account: Other account.
        """

        return account in self.multisig_accounts

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'multisig'}
        required_l2 = {
            'account',
            'accountAddress',
            'minApproval',
            'minRemoval',
            'cosignatories',
            'multisigAccounts',
        }
        return (
            # Level 1
            cls.validate_dto_required(data, required_l1)
            and cls.validate_dto_all(data, required_l1)
            # Level 2
            and cls.validate_dto_required(data['multisig'], required_l2)
            and cls.validate_dto_all(data['multisig'], required_l2)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        cosignatories = [i.public_key for i in self.cosignatories]
        multisig_accounts = [i.public_key for i in self.multisig_accounts]
        return {
            'multisig': {
                'account': self.account.public_key,
                'accountAddress': util.hexlify(self.account.address.encoded),
                'minApproval': util.u32_to_dto(self.min_approval),
                'minRemoval': util.u32_to_dto(self.min_removal),
                'cosignatories': cosignatories,
                'multisigAccounts': multisig_accounts,
            }
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        # Normalize the network type if it's not provided.
        if network_type is None and 'accountAddress' in data:
            network_type = Address(data['accountAddress']).network_type
        assert network_type is not None

        multisig = data['multisig']
        create_account = lambda x: PublicAccount.create_from_public_key(x, network_type)
        cosignatories = [create_account(i) for i in multisig['cosignatories']]
        multisig_accounts = [create_account(i) for i in multisig['multisigAccounts']]
        return cls(
            account=create_account(multisig['account']),
            min_approval=util.u32_from_dto(multisig['minApproval']),
            min_removal=util.u32_from_dto(multisig['minRemoval']),
            cosignatories=cosignatories,
            multisig_accounts=multisig_accounts
        )
