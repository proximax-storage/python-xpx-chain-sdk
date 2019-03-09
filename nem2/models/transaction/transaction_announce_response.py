"""
    transaction_announce_response
    =============================

    Response from announcing a transaction.

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

from nem2 import util


@util.inherit_doc
@util.dataclass(frozen=True)
class TransactionAnnounceResponse(util.Dto):
    """Response from announcing a transaction."""

    message: str

    def to_dto(self) -> dict:
        return {
            'message': self.message,
        }

    @classmethod
    def from_dto(cls, data: dict) -> 'TransactionAnnounceResponse':
        return cls(data['message'])
