from __future__ import annotations
import typing

from .account_meta import AccountMetaDTO
from .account import AccountDTO
from ... import util

__all__ = ['AccountInfoDTO']


@util.inherit_doc
@util.dataclass(frozen=True)
class AccountInfoDTO(util.DTO):
    """
    AccountInfo data-transfer object.

    DTO Format:
        .. code-block:: yaml

            AccountInfoDTO:
                meta: AccountMetaDTO
                account: AccountDTO
    """

    type_map: typing.ClassVar[util.TypeMap] = {
        'meta': (AccountMetaDTO, util.MISSING),
        'account': (AccountDTO, util.MISSING),
    }

    attribute_map: typing.ClassVar[util.AttributeMap] = {
        'meta': 'meta',
        'account': 'account',
    }

    meta: AccountMetaDTO
    account: AccountDTO
