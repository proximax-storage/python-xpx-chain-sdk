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
import typing
from nem2 import util
from .public_account import PublicAccount

PublicAccountListType = typing.Sequence[PublicAccount]


@util.inherit_doc
@util.dataclass(frozen=True)
class MultisigAccountInfo:
    """
    Information describing a multisig account.

    Multisig accounts allow multiple accounts, or signatories,
    operate as an entity, requiring a certain consensus for operations.

    :param account: Multisig public account.
    :param min_approval: Min number of cosignatories required to approve a transaction.
    :param min_removal: Min number of cosignatories required to remove a cosignatory.
    :param cosignatories: List of cosignatories.
    :param multisig_accounts: List of multisig accounts this account cosigns.
    """

    account: PublicAccount
    min_approval: int
    min_removal: int
    cosignatories: PublicAccountListType
    multisig_accounts: PublicAccountListType

    def is_multisig(self) -> bool:
        """Get if account is a multisig account."""

        return self.min_removal != 0 and self.min_approval != 0

    isMultisig = util.undoc(is_multisig)

    def has_cosigner(self, account: PublicAccount) -> bool:
        """
        Check if another account is cosignatory of multisig account.

        :param account: Other account.
        """

        return account in self.cosignatories

    hasCosigner = util.undoc(has_cosigner)

    def is_cosigner_of_multisig_account(self, account: PublicAccount) -> bool:
        """
        Check if multisig account is cosignatory of another account.

        :param account: Other account.
        """

        return account in self.multisig_accounts

    isCosignerOfMultisigAccount = util.undoc(is_cosigner_of_multisig_account)
