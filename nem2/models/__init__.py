"""
    models
    ======

    High-level models for the NEM2 SDK.

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

# Do not import any of these models into the in the
# __init__ of the subdirectories, since there is a
# complicated web of inter-dependencies within models.
# Just use glob imports at the models level.
# Since we shadow `account`, `mosaic`, and `transaction` with
# imports, MyPy complains, so silence MyPy.

# Account
from .account.account import *
from .account.account_info import *
from .account.address import *
from .account.multisig_account_graph_info import *
from .account.multisig_account_info import *
from .account.public_account import *
from .account import *      # type: ignore

# Blockchain
from .blockchain.block_info import *
from .blockchain.blockchain_score import *
from .blockchain.blockchain_storage_info import *
from .blockchain.network_type import *
from .blockchain import *

# Mosaic
from .mosaic.mosaic import *
from .mosaic.mosaic_id import *
from .mosaic.mosaic_info import *
from .mosaic.mosaic_levy import *
from .mosaic.mosaic_levy_type import *
from .mosaic.mosaic_name import *
from .mosaic.mosaic_nonce import *
from .mosaic.mosaic_properties import *
from .mosaic.mosaic_supply_type import *
from .mosaic.network_currency_mosaic import *
from .mosaic.network_harvest_mosaic import *
from .mosaic import *       # type: ignore

# Namespace
from .namespace.address_alias import *
from .namespace.alias import *
from .namespace.alias_action_type import *
from .namespace.alias_type import *
from .namespace.empty_alias import *
from .namespace.mosaic_alias import *
from .namespace.namespace_id import *
from .namespace.namespace_info import *
from .namespace.namespace_name import *
from .namespace.namespace_type import *
from .namespace import *

# Transaction
from .transaction.address_alias_transaction import *
from .transaction.aggregate_transaction_cosignature import *
from .transaction.aggregate_transaction_info import *
from .transaction.alias_transaction import *
from .transaction.cosignature_signed_transaction import *
from .transaction.deadline import *
from .transaction.hash_type import *
from .transaction.inner_transaction import *
from .transaction.message import *
from .transaction.message_type import *
from .transaction.mosaic_alias_transaction import *
from .transaction.multisig_cosignatory_modification_type import *
from .transaction.plain_message import *
from .transaction.secret_proof_transaction import *
from .transaction.signed_transaction import *
from .transaction.transaction import *
from .transaction.transaction_announce_response import *
from .transaction.transaction_info import *
from .transaction.transaction_status import *
from .transaction.transaction_status_error import *
from .transaction.transaction_status_group import *
from .transaction.transaction_type import *
from .transaction.transaction_version import *
from .transaction.transfer_transaction import *
from .transaction import *  # type: ignore

__all__ = (
    # Account
    account.__all__         # type: ignore
    + account_info.__all__
    + address.__all__
    + multisig_account_graph_info.__all__
    + multisig_account_info.__all__
    + public_account.__all__

    # Blockchain
    + block_info.__all__
    + blockchain_score.__all__
    + blockchain_storage_info.__all__
    + network_type.__all__

    # Mosaic
    + mosaic.__all__        # type: ignore
    + mosaic_id.__all__
    + mosaic_info.__all__
    + mosaic_levy.__all__
    + mosaic_levy_type.__all__
    + mosaic_name.__all__
    + mosaic_nonce.__all__
    + mosaic_properties.__all__
    + mosaic_supply_type.__all__
    + network_currency_mosaic.__all__
    + network_harvest_mosaic.__all__

    # Namespace
    + address_alias.__all__
    + alias.__all__
    + alias_action_type.__all__
    + alias_type.__all__
    + empty_alias.__all__
    + mosaic_alias.__all__
    + namespace_id.__all__
    + namespace_info.__all__
    + namespace_name.__all__
    + namespace_type.__all__

    # Transaction
    + address_alias_transaction.__all__
    + aggregate_transaction_cosignature.__all__
    + aggregate_transaction_info.__all__
    + alias_transaction.__all__
    + cosignature_signed_transaction.__all__
    + deadline.__all__
    + hash_type.__all__
    + inner_transaction.__all__
    + message.__all__
    + message_type.__all__
    + mosaic_alias_transaction.__all__
    + multisig_cosignatory_modification_type.__all__
    + plain_message.__all__
    + secret_proof_transaction.__all__
    + signed_transaction.__all__
    + transaction.__all__   # type: ignore
    + transaction_announce_response.__all__
    + transaction_info.__all__
    + transaction_status.__all__
    + transaction_status_error.__all__
    + transaction_status_group.__all__
    + transaction_type.__all__
    + transaction_version.__all__
    + transfer_transaction.__all__
)
