"""
    deadline
    ========

    Deadline of a transaction.

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

import datetime
import enum

from nem2 import util


class ChronoUnit(enum.IntEnum):
    """Enumerations for time units."""

    MICROSECONDS = 0
    MILLISECONDS = 1
    SECONDS = 2
    MINUTES = 3
    HOURS = 4

    def description(self) -> str:
        """Describe enumerated values in detail."""

        return DESCRIPTION[self]

    def to_timedelta(self, value: int) -> datetime.timedelta:
        """Get timedelta as multiple of units."""

        kw = KEYWORDS[self]
        return datetime.timedelta(**{kw: value})


DESCRIPTION = {
    ChronoUnit.MICROSECONDS: "Microseconds.",
    ChronoUnit.MILLISECONDS: "Milliseconds.",
    ChronoUnit.SECONDS: "Seconds.",
    ChronoUnit.MINUTES: "Minutes.",
    ChronoUnit.HOURS: "Hours.",
}

KEYWORDS = {
    ChronoUnit.MICROSECONDS: "microseconds",
    ChronoUnit.MILLISECONDS: "milliseconds",
    ChronoUnit.SECONDS: "seconds",
    ChronoUnit.MINUTES: "minutes",
    ChronoUnit.HOURS: "hours",
}


class Deadline(util.Dto, util.Tie):
    """
    Deadline of a transaction.

    The number of seconds since the creation of the nemesis block.
    """

    TIMESTAMP_NEMESIS_BLOCK: int = 1459468800
    _deadline: int

    def __init__(self, deadline: int) -> None:
        """
        :param deadline: Raw deadline as seconds since nemesis block.
        """
        self._deadline = deadline

    @property
    def deadline(self):
        """Get raw deadline as seconds since nemesis block."""
        return self._deadline

    def create(deadline: int = 2, unit: ChronoUnit = ChronoUnit.HOURS):
        """
        :param deadline: Time for deadline after current time.
        :param chrono_unit: Unit for created deadline.
        """

        seconds = unit.to_timedelta(deadline).total_seconds()
        day = datetime.timedelta(days=1).total_seconds()
        if seconds <= 0:
            raise ValueError(f"Deadline should be greater than 0, got {seconds}")
        elif seconds >= day:
            raise ValueError(f"Deadline should be less than 1 day, got {seconds}")

        # TODO(ahuszagh) here...
        # Shouldn't this be... network time? UTC???

        # timedelta(microseconds=-1)
        raise NotImplementedError

    @util.doc(util.Dto.to_dto)
    def to_dto(self) -> util.Uint64DtoType:
        return util.uint64_to_dto(self.deadine)

    @util.doc(util.Dto.from_dto)
    @classmethod
    def from_dto(cls, data: util.Uint64DtoType) -> 'Deadline':
        return cls(util.dto_to_uint64(data))
