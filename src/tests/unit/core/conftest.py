from datetime import datetime

import pytest
from freezegun import freeze_time

from app.core.service import Transaction, TransactionService, TransactionType


@freeze_time('2024-07-12 03:21:34')
@pytest.fixture(scope='session')
def transaction_service():
    transaction_service = TransactionService()
    transaction = Transaction(
        1, 100, TransactionType.withdrawal, datetime.now())
    transaction_service.transactions[1] = [transaction]
    transaction_service.users.add_user(1, False)
    transaction_service.users.add_user(2, True)
    transaction_service.users.add_user(3, True)
    transaction_service.users.add_user(4, True)
    return transaction_service
