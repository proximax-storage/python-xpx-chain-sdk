
from __future__ import annotations

from ... import util
from .config_fields import Fields

__all__ = ['Sections']


@util.inherit_doc
@util.dataclass(frozen=True)
class Sections(util.DTO):
    """
    Config sections.
    """

    sections: dict

    @classmethod
    def create_from_string(
        cls,
        data: str,
    ):
        return cls({
            bag[0]: Fields.create_from_string(bag[1]) for bag in [
                section.split(']') for section in data.strip().split('[')[1:]
            ]
        })

    def to_string(
        self,
    ) -> str:
        config = ""

        for section in self.sections:
            config += '[' + section + ']\n\n'
            config += self.sections[section].to_string() + '\n\n'

        return config
