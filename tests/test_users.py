import json
import pytest
from app.main import app
from log.config_log import logger
from .database import get_test_db
from .help_to_tests import client, authorized_client, test_users, token


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_users(client):
    response = await client.get("/users/")
    assert response.status_code == 200


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_create_user(client):
    response = await client.post(
        "/users/",
        json={
            "email": "user@gmail.com",
            "username": "user",
            "password": "qwerty"
        }
    )
    logger.info(response.json())
    assert response.status_code == 201
    assert response.json() == {
        "created_at": response.json().get("created_at"),
        "updated_at": response.json().get("updated_at"),
        "email": "user@gmail.com",
        "username": "user",
        "id": 1,
        "is_active": True
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_user(client, test_users):
    response = await client.get(
        f"/users/{test_users[1].id}",
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "created_at": response.json().get("created_at"),
        "updated_at": response.json().get("updated_at"),
        "email": "karina@gmail.com",
        "username": "karina",
        "id": 2,
        "is_active": True,
        "requests": []
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_error_404(client):
    response = await client.get(
        "/users/10",
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "User with id:10 was not found"
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_check_permission(authorized_client, test_users):

    response = await authorized_client.put(
        f"/users/{test_users[2].id}",
        json={
            "password": "admin",
        }
    )
    print(response.json())
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Not authorized to perform requested action"
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_update_user(authorized_client, test_users):

    response = await authorized_client.put(
        f"/users/{test_users[0].id}",
        json={
            "username": "admin",
        }
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "created_at": response.json().get("created_at"),
        "updated_at": response.json().get("updated_at"),
        "email": "vladimir@gmail.com",
        "username": "admin",
        "id": 1,
        "is_active": True
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_delete_user(authorized_client, test_users):

    response = await authorized_client.delete(
        f"/users/{test_users[0].id}",
    )
    assert response.status_code == 204
