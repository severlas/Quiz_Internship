import json
import pytest
from app.main import app
from log.config_log import logger
from .database import get_test_db
from .help_to_tests import (
    client, authorized_client, test_users, token,
    test_quiz_results, test_companies, test_quizzes, test_admins_for_company
)


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_gpa_user(client, test_users, test_quiz_results):
    response = await client.get(f"/users/{test_users[0].id}/get_gpa")
    assert response.status_code == 200
    assert response.json() == {'gpa_all': round(25 / 35, 3)}


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_gpa_by_quiz_for_user(authorized_client, test_users, test_quiz_results):
    response = await authorized_client.get(f"/users/{test_users[0].id}/get_gpa_by_quiz")
    assert response.status_code == 200
    assert response.json() == [
        {
            "quiz_id": 1,
            "gpa_over_time": [
                {
                    "gpa_by_quiz": round(7 / 10, 3),
                    "created_at": response.json()[0].get("gpa_over_time")[0].get("created_at")
                },
                {
                    "gpa_by_quiz": round(15 / 20, 3),
                    "created_at": response.json()[0].get("gpa_over_time")[1].get("created_at")
                }
            ]
        },
        {
            "quiz_id": 2,
            "gpa_over_time": [
                {
                    "gpa_by_quiz": round(10 / 15, 3),
                    "created_at": response.json()[1].get("gpa_over_time")[0].get("created_at")
                },
            ]
        }
    ]


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_time_of_last_quiz_for_user(authorized_client, test_users, test_quiz_results):
    response = await authorized_client.get(f"/users/{test_users[0].id}/get_time_of_last_quiz")
    assert response.status_code == 200
    assert response.json() == [
        {
            "quiz_id": 2,
            "created_at": response.json()[0].get("created_at")
        },
        {
            "quiz_id": 1,
            "created_at": response.json()[1].get("created_at")

        }
    ]


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_gpa_by_quiz_for_company(
        authorized_client,
        test_users,
        test_quiz_results,
        test_companies,
        test_admins_for_company
):
    response = await authorized_client.get(
        f"/companies/{test_companies[0].id}/get_gpa_by_quiz?quiz_user_id={test_users[0].id}"
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json() == [
        {
            "quiz_id": 1,
            "gpa_over_time": [
                {
                    "gpa_by_quiz": round(7 / 10, 3),
                    "created_at": response.json()[0].get("gpa_over_time")[0].get("created_at")
                },
                {
                    "gpa_by_quiz": round(15 / 20, 3),
                    "created_at": response.json()[0].get("gpa_over_time")[1].get("created_at")
                }
            ]
        },
        {
            "quiz_id": 2,
            "gpa_over_time": [
                {
                    "gpa_by_quiz": round(10 / 15, 3),
                    "created_at": response.json()[1].get("gpa_over_time")[0].get("created_at")
                },
            ]
        }
    ]


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_gpa_for_company(
        authorized_client,
        test_users,
        test_quiz_results,
        test_companies,
        test_admins_for_company
):
    response = await authorized_client.get(f"/companies/{test_companies[0].id}/get_gpa")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == [
        {
            "user_id": 1,
            "gpa_over_time": [
                {
                    "gpa_all": round(7 / 10, 3),
                    "created_at": response.json()[0].get("gpa_over_time")[0].get("created_at")
                },
                {
                    "gpa_all": round(15 / 20, 3),
                    "created_at": response.json()[0].get("gpa_over_time")[1].get("created_at")
                },
                {
                    "gpa_all": round(25 / 35, 3),
                    "created_at": response.json()[0].get("gpa_over_time")[2].get("created_at")
                }
            ]
        }
    ]


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_time_of_last_quiz_for_company(
        authorized_client,
        test_users,
        test_quiz_results,
        test_companies,
        test_admins_for_company
):
    response = await authorized_client.get(f"/companies/{test_companies[0].id}/get_time_of_last_quiz")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == [
        {
            "user_id": 1,
            "created_at": response.json()[0].get("created_at")

        }
    ]
