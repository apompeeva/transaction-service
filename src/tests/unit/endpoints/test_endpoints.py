from datetime import datetime

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('user_id, transaction_sum, transaction_type, expected_response', (
    pytest.param(1, 100.0, 2, 200, id='not_verified_user_deposit'),
    pytest.param(1, 10.0, 1, 200, id='not_verified_user_withdraval'),
    pytest.param(2, 100.0, 2, 200, id='verified_user_deposit'),
    pytest.param(2, 100.0, 1, 200, id='verified_user_withdraval'),
    pytest.param(3, 100.0, 1, 200, id='verified_user_extra_withdraval'),
    pytest.param(1, 1000.0, 1, 403, id='not_verified_user_extra_withdraval'),
))
async def test_create_transaction(ac: AsyncClient, user_id, transaction_sum, transaction_type, expected_response):
        transaction_data = {
            "user_id": user_id,
            "transaction_sum": transaction_sum,
            "transaction_type": transaction_type
        }

        response = await ac.post('/create_transaction', json=transaction_data)

        # Проверка статуса ответа
        assert response.status_code == expected_response

async def test_get_transactions(ac: AsyncClient):
    report_data = {
        "user_id": 1,
        "start_date": "2024-07-12 13:20:38.055",
        "end_date": "2024-07-14 13:20:38.055",
    }

    response = await ac.post('/get_report', json=report_data)

    assert response.status_code == 200

