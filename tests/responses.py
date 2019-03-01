"""
    responses
    =========

    Mocked response data for the .

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

import os

ENDPOINT = os.environ.get("NIS2_ENDPOINT", "localhost:7890")

HEARTBEAT = {
    "Ok": {
        'content': b'{"code":1,"type":2,"message":"ok"}',
        'headers': {'Content-Encoding': 'gzip', 'Content-Type': 'application/json'},
    },
}

STATUS = {
    "Local": {
        'content': b'{"code":7,"type":4,"message":"status"}',
        'headers': {'Content-Encoding': 'gzip', 'Content-Type': 'application/json'},
    },
    "Synchronized": {
        'content': b'{"code":6,"type":4,"message":"status"}',
        'headers': {'Content-Encoding': 'gzip', 'Content-Type': 'application/json'},
    },
    "Unknown": {
        'content': b'{"code":0,"type":4,"message":"status"}',
        'headers': {'Content-Encoding': 'gzip', 'Content-Type': 'application/json'},
    },
    "Error": {
        'content': b'{"code":-1,"type":4,"message":"status"}',
        'headers': {'Content-Encoding': 'gzip', 'Content-Type': 'application/json'},
    }
}
