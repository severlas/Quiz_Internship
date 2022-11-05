import json
import pytest
from app.main import app
from log.config_log import logger
from .database import get_test_db
from .help_to_tests import client, authorized_client, test_users, token


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_sign_in(client, test_users):
    response = await client.post(
        "/auth/sign-in",
        json={
            "email": "vladimir@gmail.com",
            "password": "vladimir"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "access_token": response.json().get("access_token"),
        "token_type": "bearer"
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_error_authorize(client, test_users):
    response = await client.post(
        "/auth/sign-in",
        json={
            "email": "vladimir@gmail.com",
            "password": "vladimi"
        }
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Could not validate credentials"
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_validation_email(client, test_users):
    response = await client.post(
        "/auth/sign-in",
        json={
            "email": "vladimir@gmailcom",
            "password": "vladimir"
        }
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "value is not a valid email address",
                "type": "value_error.email"
            }
        ]
    }
