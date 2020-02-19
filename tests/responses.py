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

import json
import os

DIR = os.path.dirname(os.path.realpath(__file__))
DATADIR = os.path.join(DIR, 'data')
ENDPOINT = os.environ.get('NIS2_ENDPOINT', '//localhost:3000')


def load_response(name):
    with open(os.path.join(DATADIR, name)) as f:
        data = json.load(f)
        data['content'] = data['content'].encode('utf8')
        return data


# ACCOUNT
ACCOUNT_INFO = {
    'Ok': load_response('account_info.json'),
}

ACCOUNTS_INFO = {
    'Ok': load_response('accounts_info.json'),
}

ACCOUNT_PROPERTIES = {
    'Ok': load_response('account_properties.json'),
}

ACCOUNTS_PROPERTIES = {
    'Ok': load_response('accounts_properties.json'),
}

ACCOUNT_NAMES = {
    'Ok': load_response('account_names.json'),
}

MULTISIG_INFO = {
    'Ok': load_response('multisig_info.json'),
}

MULTISIG_GRAPH_INFO = {
    'Ok': load_response('multisig_graph_info.json'),
}

# METADATA
ACCOUNT_METADATA = {
    'Ok': load_response('account_metadata.json'),
}

MOSAIC_METADATA = {
    'Ok': load_response('mosaic_metadata.json'),
}

NAMESPACE_METADATA = {
    'Ok': load_response('namespace_metadata.json'),
}

METADATA = {
    'Ok': load_response('metadata.json'),
}

METADATAS = {
    'Ok': load_response('metadatas.json'),
}

# CONFIG
CONFIG = {
    'Ok': load_response('config.json'),
}

UPGRADE = {
    'Ok': load_response('upgrade.json'),
}

# Node
INFO = {
    'Ok': load_response('node_info.json'),
}

TIME = {
    'Ok': load_response('node_time.json'),
}

# BLOCKCHAIN
BLOCK_INFO = {
    'Ok': load_response('block_info.json'),
}

BLOCKS_INFO = {
    'Ok': load_response('blocks_info.json'),
}

BLOCK_TRANSACTIONS = {
    'Ok': load_response('block_transactions.json'),
}

BLOCK_TRANSACTION_MERKLE = {
    'Ok': load_response('block_transaction_merkle.json'),
}

BLOCK_RECEIPTS = {
    'Ok': load_response('block_receipts.json'),
}

DIAGNOSTIC_SERVER = {
    'Ok': load_response('diagnostic_server.json'),
}

CHAIN_HEIGHT = {
    'Ok': load_response('chain_height.json'),
}

CHAIN_SCORE = {
    'Ok': load_response('chain_score.json'),
}

DIAGNOSTIC_BLOCKS_INFO = {
    'Ok': load_response('diagnostic_blocks_info.json'),
}

DIAGNOSTIC_STORAGE = {
    'Ok': load_response('diagnostic_storage.json'),
}

BLOCK_RECEIPTS = {
    'Ok': load_response('block_receipts.json'),
}

# MOSAIC
MOSAIC_INFO = {
    'Ok': load_response('mosaic_info.json'),
}

MOSAICS_INFO = {
    'Ok': load_response('mosaics_info.json'),
}

MOSAICS_NAMES = {
    'Ok': load_response('mosaic_names.json'),
}

# NAMESPACE
NAMESPACE = {
    'nem': load_response('namespace.json'),
}

NAMESPACES = {
    'nem': load_response('namespaces.json'),
}

NAMESPACE_NAMES = {
    'nem': load_response('namespace_names.json'),
}

# NETWORK
NETWORK_TYPE = {
    'MIJIN_TEST': load_response('mijin_test_network.json'),
}

# TRANSACTION
TRANSACTION = {
    'Ok': load_response('transaction.json'),
}

TRANSACTIONS = {
    'Ok': load_response('transactions.json'),
}

TRANSACTION_STATUS = {
    'Ok': load_response('transaction_status.json'),
}

TRANSACTION_STATUSES = {
    'Ok': load_response('transaction_statuses.json'),
}

ANNOUNCE = {
    'Ok': load_response('announce.json'),
}

ANNOUNCE_PARTIAL = {
    'Ok': load_response('announce_partial.json'),
}

ANNOUNCE_COSIGNATURE = {
    'Ok': load_response('announce_cosignature.json'),
}
