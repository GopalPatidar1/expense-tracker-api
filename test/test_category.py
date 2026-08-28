
# pip install pytest pytest-asyncio httpx
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch, MagicMock
from app.main import app

mock_response = {
    'id': 1,
    'category': 'clothing'
}


@pytest.mark.asyncio
async def test_get_category(authenticated_client):
    with patch(
        "app.repository.category.get_category",
        new_callable=AsyncMock,
        return_value=mock_response
    ) as mock_service:

            response = await authenticated_client.get(
                "/category/",
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
    args = mock_service.call_args.args
    assert args[0] is not None


@pytest.mark.asyncio
async def test_create_category(authenticated_client):
    category_data = {
        'category': 'clothing'
    }

    mock_response = {
        'id': None, # none because is not generating in test case TODO fix in feature 
    }

    with patch(
        "app.repository.category.create_category",
        new_callable=AsyncMock,
        return_value=mock_response
    ) as mock_service:

        response = await authenticated_client.post(
                "/category/",
                json=category_data
            )

    assert response.status_code == 201
    assert response.json() == mock_response
    mock_service.assert_awaited_once()
    kwargs = mock_service.call_args.kwargs

    assert kwargs["db"] is not None
    assert kwargs["data"].category == "clothing"

@pytest.mark.asyncio
async def test_update_category(authenticated_client):
    category_data = {
        'category': 'clothing'
    }

    mock_response = {
        'category': 'clothing'
    }

    with patch(
        "app.repository.category.update_category",
        new_callable=AsyncMock,
        return_value=mock_response
    ) as mock_service:
          response = await authenticated_client.put(
                "/category/1",
                json=category_data
            )

    assert response.status_code == 200
    assert response.json() == mock_response

    mock_service.assert_awaited_once()
    kwargs = mock_service.call_args.kwargs
    assert kwargs['db'] is not None
    assert kwargs['id'] == 1


@pytest.mark.asyncio
async def test_delete_category(authenticated_client):
    mock_result = MagicMock()
    mock_result.rowcount = 1

    deleteRes ={
        'message': 'Category deleted successfully'
    }

    with patch(
        "app.repository.category.delete_category",
        new_callable=AsyncMock,
        return_value=mock_result
    ) as mock_service:
        response = await authenticated_client.delete("/category/1")

    assert response.status_code == 200
    assert response.json() == deleteRes
    mock_service.assert_awaited_once()