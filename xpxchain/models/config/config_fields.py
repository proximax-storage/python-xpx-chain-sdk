
from __future__ import annotations

from ... import util

__all__ = ['Fields']


@util.inherit_doc
@util.dataclass(frozen=True)
class Fields(util.DTO):
    """
    Config fields.
    """

    flds: dict

    @classmethod
    def create_from_string(
        cls,
        data: str,
    ):
        return cls({
            pair[0].strip(): pair[1].strip() for pair in [
                fld.split('=') for fld in data.split('\n') if fld and fld.strip()[0] != '#'
            ] if len(pair) == 2
        })

    def to_string(
        self,
    ) -> str:
        return '\n'.join(fld + ' = ' + self.flds[fld] for fld in self.flds)
