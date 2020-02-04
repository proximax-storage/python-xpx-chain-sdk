from __future__ import annotations
import enum
from .. import util

__all__ = [
    'FeeCalculationStrategy',
    'calculate_fee'
]


@util.inherit_doc
class FeeCalculationStrategy(util.U8Mixin, util.EnumMixin, enum.IntEnum):
    """ Fee calculation strategy """

    ZERO = 0
    LOW = 25
    MEDIUM = 250
    HIGH = 2500

    def description(self) -> str:
        return DESCRIPTION[self]


DESCRIPTION = {
    FeeCalculationStrategy.ZERO: "Zero fee calculation strategy",
    FeeCalculationStrategy.LOW: "Low fee calculation strategy",
    FeeCalculationStrategy.MEDIUM: "Medium fee calculation strategy",
    FeeCalculationStrategy.HIGH: "High fee calculation strategy",
}


def calculate_fee(strategy: FeeCalculationStrategy, max_fee: int, transaction_size: int) -> int:
    return max(max_fee, strategy * transaction_size)
