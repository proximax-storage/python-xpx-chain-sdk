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
    LOW = 15000
    MEDIUM = 150000
    HIGH = 1500000

    def description(self) -> str:
        return DESCRIPTION[self]


DESCRIPTION = {
    FeeCalculationStrategy.ZERO: "Zero fee calculation strategy",
    FeeCalculationStrategy.LOW: "Low fee calculation strategy",
    FeeCalculationStrategy.MEDIUM: "Medium fee calculation strategy",
    FeeCalculationStrategy.HIGH: "High fee calculation strategy",
}


def calculate_fee(strategy: FeeCalculationStrategy, transaction_size: int, max_fee: int = 75000000) -> int:
    return min(max_fee, strategy * transaction_size)
