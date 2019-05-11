from __future__ import annotations
import typing

from ... import util

__all__ = ['AccountDTO']


@util.inherit_doc
@util.dataclass(frozen=True)
class AccountDTO(util.DTO):
    """
    AccountMeta data-transfer object.

    DTO Format:
        .. code-block:: yaml

            AccountDTO:
                # Hex(Address) (50-bytes)
                address: string
                addressHeight: UInt64DTO
                # Hex(PublicKey) (64-bytes)
                publicKey: string
                publicKeyHeight: UInt64DTO
                mosaics: MosaicDTO[]
                importance: UInt64DTO
                importanceHeight: UInt64DTO
    """

    type_map: typing.ClassVar[typing.Dict[str, typing.Type]] = {
        'address': (str, util.MISSING),
        'address_height': (typing.List[int], util.MISSING),
        'public_key': (str, util.MISSING),
        'public_key_height': (typing.List[int], util.MISSING),
    }

    attribute_map: typing.ClassVar[typing.Dict[str, str]] = {
        'address': 'address',
        'address_height': 'addressHeight',
        'public_key': 'publicKey',
        'public_key_height': 'publicKeyHeight',
    }

    address: str
