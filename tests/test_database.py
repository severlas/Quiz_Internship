import json
import pytest
from app.main import app
from log.config_log import logger
from .database import get_test_db
from .help_to_tests import client, authorized_client, test_companies, token, test_users


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_database_data(client, test_companies):
    response = await client.get("/companies/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "created_at": response.json()[0].get("created_at"),
            "updated_at": response.json()[0].get("updated_at"),
            "name": "BMW",
            "descriptions": "Inform about cars",
            "visibility": True,
            "id": 1,
            "owner_id": 1
        },
        {
            "created_at": response.json()[1].get("created_at"),
            "updated_at": response.json()[1].get("updated_at"),
            "name": "Meduzzen",
            "descriptions": "Inform about web development",
            "visibility": True,
            "id": 3,
            "owner_id": 3
        }
    ]
