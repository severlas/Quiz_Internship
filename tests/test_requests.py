import pytest
import json
from httpx import AsyncClient
from .database import get_test_db
from .help_to_tests import client, authorized_client, token, test_users, test_companies, test_requests
from log.config_log import logger


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_requests(client):
    response = await client.get(
        '/requests/',
    )
    logger.info(response.json())
    assert response.status_code == 200


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_create_request(authorized_client, test_users, test_companies):
    response = await authorized_client.post(
        '/requests/',
        json={
            "sender": "company",
            "status": "created",
            "company_id": test_companies[0].id,
            "user_id": test_users[1].id
        }
    )

    assert response.status_code == 201
    assert response.json() == {
        "created_at": response.json().get("created_at"),
        "updated_at": response.json().get("updated_at"),
        "sender": "company",
        "status": "created",
        "id": 1,
        "company_id": 1,
        "user_id": 2
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_request(authorized_client, test_requests):
    response = await authorized_client.get(
        f'/requests/{test_requests[1].id}',
    )
    logger.info(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "created_at": response.json().get("created_at"),
        "updated_at": response.json().get("updated_at"),
        "sender": "company",
        "status": "created",
        "id": 2,
        "company_id": 2,
        "user_id": 1
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_error_404(authorized_client):
    response = await authorized_client.get(
        f'/requests/10',
    )
    logger.info(response.json())
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Request with id:10 was not found!"
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_permission(authorized_client, test_requests):
    response = await authorized_client.put(
        f'/requests/2?status=confirmed',
    )
    assert response.status_code == 403


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_update_request(authorized_client, test_requests):
    response = await authorized_client.put(
        f'/requests/{test_requests[0].id}?status=confirmed',
    )
    assert response.status_code == 204

