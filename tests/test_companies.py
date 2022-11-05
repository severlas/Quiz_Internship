import pytest
from httpx import AsyncClient
from .database import get_test_db
from .help_to_tests import test_companies, client, authorized_client, token, test_users, test_requests
from log.config_log import logger


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_companies(client):
    response = await client.get(
        '/companies/',
    )
    print(authorized_client)
    assert response.status_code == 200


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_create_company(authorized_client):
    response = await authorized_client.post(
        '/companies/',
        json={
            "name": "Test company",
            "descriptions": "information",
            "visibility": True
        }
    )
    assert response.status_code == 201
    assert response.json() == {
        "created_at": response.json().get("created_at"),
        "updated_at": response.json().get("updated_at"),
        "name": "Test company",
        "descriptions": "information",
        "visibility": True,
        "id": 1,
        "owner_id": 1
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_company(authorized_client, test_companies):
    response = await authorized_client.get(
        f'/companies/{test_companies[2].id}',
    )
    logger.info(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "created_at": response.json().get("created_at"),
        "updated_at": response.json().get("updated_at"),
        "name": "Meduzzen",
        "descriptions": "Inform about web development",
        "visibility": True,
        "id": 3,
        "owner_id": 3,
        "admins": [],
        "members": [],
        "requests": []
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_update_company(authorized_client, test_companies):
    response = await authorized_client.put(
        f'/companies/{test_companies[0].id}',
        json={
            "name": "Toyota",
            "descriptions": "Information",
            "visibility": False
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "created_at": response.json().get("created_at"),
        "updated_at": response.json().get("updated_at"),
        "name": "Toyota",
        "descriptions": "Information",
        "visibility": False,
        "id": 1,
        "owner_id": 1,
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_delete_company(authorized_client, test_companies):
    response = await authorized_client.delete(
        f'/companies/{test_companies[0].id}',
    )
    assert response.status_code == 204
