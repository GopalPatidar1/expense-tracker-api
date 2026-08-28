
# pip install pytest pytest-asyncio httpx
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch, MagicMock
from app.main import app

mock_response = {
    'result': [
        {
            'id': 1,
            'description': 'buying a clothes',
            'amount': 200,
            'payment_method': 'upi',
            'user': {
                'firstname': 'gopal',
                'lastname': 'patidar'
            },
            'category': {
                'id': 1,
                'category': 'cloths'
            }
        }
    ],
    'next_cursor': None,
    'avail_next': False
}


@pytest.mark.asyncio
async def test_get_expense_list(authenticated_client):
    with patch(
        "app.repository.expense.get_expense_list",
        new_callable=AsyncMock,
        return_value=mock_response
    ) as mock_service:

            response = await authenticated_client.get(
                "/expense/",
                params={
                    'limit': 20,
                    'next_cursor': 15
                },
            )

    assert response.status_code == 200
    assert response.json() == mock_response

    # mock_service.assert_awaited_once() direct check for once if call multiple time than check below ways
    mock_service.assert_awaited()
    assert mock_service.await_count == 1
    kwargs = mock_service.call_args.kwargs
    assert kwargs['limit'] == 20
    assert kwargs['db'] is not None
    assert kwargs['date_filter'] is None
    assert kwargs['next_cursor'] == 15


# test with invalida path params
@pytest.mark.asyncio
async def test_get_expense_list(authenticated_client):
    with patch(
        "app.repository.expense.get_expense_list",
        new_callable=AsyncMock,
        return_value=mock_response
    ) as mock_service:

            response = await authenticated_client.post(
                "/expense/",
                json={
                    'limit': 20,
                    'offset': 1
                },
            )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_add_expense_item(authenticated_client):
    expense_data = {
        'category_id': '9',
        'amount': 2100,
        'description': 'I bought a single new shous',
        'payment_method': 'upi'
    }

    mock_response = {
        'id': None,
        'amount': 2100,
        'description': 'I bought a single new shous'
    }

    with patch(
        "app.repository.expense.add_expenses",
        new_callable=AsyncMock,
        return_value=mock_response
    ) as mock_service:

        response = await authenticated_client.post(
                "/expense/",
                json=expense_data
            )

    assert response.status_code == 201
    assert response.json() == mock_response
    mock_service.assert_awaited_once()
    args = mock_service.call_args.args
    db = args[0]
    assert db is not None

@pytest.mark.asyncio
async def test_update_expense_item(authenticated_client):
    expense_data = {
        'description': 'Updated Lunch',
        'amount': 300
    }

    mock_response = {
        'id': 1,
        'description': 'Updated Lunch',
        'amount': 300
    }

    with patch(
        "app.repository.expense.update_expense",
        new_callable=AsyncMock,
        return_value=mock_response
    ) as mock_service:
          response = await authenticated_client.put(
                "/expense/1",
                json=expense_data
            )

    assert response.status_code == 200
    assert response.json() == mock_response

    mock_service.assert_awaited_once()
    kwargs = mock_service.call_args.kwargs

    assert kwargs['db'] is not None
    assert kwargs['user_id'] is not None
    assert kwargs["data"].amount == 300

@pytest.mark.asyncio
async def test_delete_expense_item(authenticated_client):
    mock_response = {
        'success': True
    }

    mock_result = MagicMock()
    mock_result.rowcount = 1

    with patch(
        "app.repository.expense.delete_expense",
        new_callable=AsyncMock,
        return_value=mock_result
    ) as mock_service:
        response = await authenticated_client.delete("/expense/1")

    assert response.status_code == 200
    assert response.json() == mock_response
    mock_service.assert_awaited_once()