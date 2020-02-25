from ..models.transaction.transaction_status_error import TransactionStatusError
from ..models.transaction.deadline import Deadline
from ..models.account.address import Address

__all__ = ['TransactionError']


class TransactionError(Exception):

    hash: str
    status: str
    deadline: Deadline
    channel_name: str
    address: Address

    def __init__(self, tx: TransactionStatusError):
        self.hash = tx.hash
        self.status = tx.status
        self.deadline = tx.deadline
        self.channel_name = tx.channel_name
        self.address = tx.address

    def __str__(self):
        return self.status
