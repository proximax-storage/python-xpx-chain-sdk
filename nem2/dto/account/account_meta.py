from __future__ import annotations
import typing

from ... import util

__all__ = ['AccountMetaDTO']


@util.inherit_doc
@util.dataclass(frozen=True)
class AccountMetaDTO(util.DTO):
    """
    AccountMeta data-transfer object.

    DTO Format:
        .. code-block:: yaml

            AccountMetaDTO: {}
    """

    type_map: typing.ClassVar[util.TypeMap] = {}
    attribute_map: typing.ClassVar[util.AttributeMap] = {}
