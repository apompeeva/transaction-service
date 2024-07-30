from datetime import datetime
from decimal import Decimal

import pytest
from freezegun import freeze_time


@pytest.mark.parametrize('user_id, transaction_sum, transaction_type', (
    pytest.param(1, 100.0, 2, id='not_verified_user_deposit'),
    pytest.param(1, 10.0, 1, id='not_verified_user_withdraval'),
    pytest.param(2, 100.0, 2, id='verified_user_deposit'),
    pytest.param(2, 100.0, 1, id='verified_user_withdraval'),
    pytest.param(3, 100.0, 1, id='verified_user_extra_withdraval'),
))
@freeze_time('2024-07-11 03:21:34')
def test_create_transaction(transaction_service, user_id, transaction_sum, transaction_type):
    creation_time = datetime.now()

    transaction = transaction_service.create_transaction(
        user_id, Decimal(transaction_sum), transaction_type)

    assert transaction in transaction_service.transactions[user_id]
    assert transaction.user_id == user_id
    assert transaction.transaction_sum == transaction_sum
    assert transaction.transaction_type == transaction_type
    assert transaction.creation_time == creation_time


@pytest.mark.parametrize('user_id, start_date, end_date', (
    pytest.param(4, datetime(2024, 7, 10),
                 datetime(2024, 7, 14), id='no_transaction'),
    pytest.param(1, datetime(2024, 5, 10), datetime(
        2024, 5, 14), id='no_transaction_in_range'),
))
def test_get_transaction_no_transactions(transaction_service, user_id, start_date, end_date):
    transactions = transaction_service.get_transaction(
        user_id, start_date, end_date)

    assert len(transactions) == 0


def test_get_transaction(transaction_service):
    user_id = 1
    start_date = datetime(2024, 7, 10)
    end_date = datetime(2024, 7, 14)

    transactions = transaction_service.get_transaction(
        user_id, start_date, end_date)

    assert len(transactions) != 0
    for transaction in transactions:
        assert transaction.creation_time >= start_date
        assert transaction.creation_time <= end_date
