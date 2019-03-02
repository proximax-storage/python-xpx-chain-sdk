"""
    codes
    =====

    Error and success response codes from the NEM NIS.

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

from enum import IntEnum

__all__ = [
    'Heartbeat',
    'Status',
]


class Heartbeat(IntEnum):
    """Enumerations for the status of a "/heartbeat" request."""

    UNKNOWN = 0
    OK = 1

    def description(self) -> str:
        """Describe the enumeration value."""

        return HEARTBEAT_DESCRIPTION[self]

HEARTBEAT_DESCRIPTION = {
    Heartbeat.UNKNOWN: "Unknown status.",
    Heartbeat.OK: "NIS is ok.",
}


class Status(IntEnum):
    """Enumerations for the status of a "/status" request."""

    UNKNOWN = 0
    STOPPED = 1
    STARTING = 2
    RUNNING = 3
    BOOTING = 4
    BOOTED = 5
    SYNCHRONIZED = 6
    LOCAL = 7
    LOADING = 8

    def description(self) -> str:
        """Describe the enumeration value."""

        return STATUS_DESCRIPTION[self]


STATUS_DESCRIPTION = {
    Status.UNKNOWN: "Unknown status.",
    Status.STOPPED: "NIS is stopped.",
    Status.STARTING: "NIS is starting.",
    Status.RUNNING: "NIS is running.",
    Status.BOOTING: "NIS is booting the local node (implies NIS is running).",
    Status.BOOTED: "The local node is booted (implies NIS is running).",
    Status.SYNCHRONIZED: "The local node is synchronized (implies NIS is running and the local node is booted).",
    Status.LOCAL: "NIS local node does not see any remote NIS node (implies running and booted).",
    Status.LOADING: "NIS is currently loading the block chain from the database. In this state NIS cannot serve any requests.",
}
