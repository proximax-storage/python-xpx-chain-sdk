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
import typing
from nem2 import util


@util.inherit_doc
class ChronoUnit(util.EnumMixin, enum.IntEnum):
    """Enumerations for time units."""

    MICROSECONDS = 0
    MILLISECONDS = 1
    SECONDS = 2
    MINUTES = 3
    HOURS = 4

    def description(self) -> str:
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


@util.inherit_doc
@util.dataclass(frozen=True)
class Deadline(util.Dto):
    """
    Deadline of a transaction.

    The number of seconds since the creation of the nemesis block.
    The number of seconds stored in the class are in local time, and
    any conversions to or from data-transfer objects will implicitly
    convert the data to UTC.

    :param deadline: Datetime of deadline in local time.
    """

    TIMESTAMP_NEMESIS_BLOCK: typing.ClassVar[int] = 1459468800
    deadline: datetime.datetime

    @classmethod
    def create(cls, deadline: int = 2, unit: ChronoUnit = ChronoUnit.HOURS):
        """
        Create deadline relative to current local time.

        :param deadline: Time for deadline after current time.
        :param chrono_unit: Unit for created deadline.
        """

        delta = unit.to_timedelta(deadline)
        day = datetime.timedelta(days=1).total_seconds()
        now = datetime.datetime.now()
        delta_seconds = delta.total_seconds()
        if delta_seconds <= 0:
            raise ValueError(f"Deadline should be greater than 0, got {delta_seconds}")
        elif delta_seconds >= day:
            raise ValueError(f"Deadline should be less than 1 day, got {delta_seconds}")

        return cls(now + delta)

    @classmethod
    def create_from_timestamp(cls, timestamp: int):
        """
        Create deadline from timestamp.

        :param timestamp: Timestamp in UTC timezone.
        """
        utc = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
        local = utc.replace(tzinfo=None)
        return cls(local)

    createFromTimestamp = util.undoc(create_from_timestamp)

    def to_dto(self) -> util.U64DTOType:
        utc = self.deadline.replace(tzinfo=datetime.timezone.utc)
        return util.uint64_to_dto(int(utc.timestamp()))

    @classmethod
    def from_dto(cls, data: util.U64DTOType) -> 'Deadline':
        return cls.create_from_timestamp(util.dto_to_uint64(data))
