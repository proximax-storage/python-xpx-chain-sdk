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
import struct
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
class Deadline(util.Model):
    """
    Deadline of a transaction.

    The number of seconds since the creation of the nemesis block.
    The number of seconds stored in the class are in local time, and
    any conversions to or from data-transfer objects will implicitly
    convert the data to UTC.

    :param deadline: Datetime of deadline in local time.
    """

    deadline: datetime.datetime
    CATBUFFER_SIZE: typing.ClassVar[int] = 8
    TIMESTAMP_NEMESIS_BLOCK: typing.ClassVar[int] = 1459468800

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

    def to_timestamp(self) -> int:
        """Export deadline to UTC timestamp."""

        utc = self.deadline.replace(tzinfo=datetime.timezone.utc)
        return int(utc.timestamp())

    toTimestamp = util.undoc(to_timestamp)

    @classmethod
    def from_timestamp(cls, timestamp: int) -> 'Deadline':
        """
        Create deadline from UTC timestamp.

        :param timestamp: Timestamp in UTC timezone.
        """
        utc = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
        local = utc.replace(tzinfo=None)
        return cls(local)

    fromTimestamp = util.undoc(from_timestamp)

    def to_dto(self) -> util.U64DTOType:
        return util.uint64_to_dto(self.to_timestamp())

    @classmethod
    def from_dto(cls, data: util.U64DTOType) -> 'Deadline':
        return cls.from_timestamp(util.dto_to_uint64(data))

    def to_catbuffer(self) -> bytes:
        return struct.pack('<Q', self.to_timestamp())

    @classmethod
    def from_catbuffer(cls, data: bytes) -> typing.Tuple['Deadline', bytes]:
        assert len(data) >= cls.CATBUFFER_SIZE
        inst = cls.from_timestamp(struct.unpack('<Q', data[:cls.CATBUFFER_SIZE])[0])
        return inst, data[cls.CATBUFFER_SIZE:]
