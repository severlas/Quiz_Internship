import pytest
from httpx import AsyncClient
from .database import get_test_db
from .help_to_tests import (test_companies, client, authorized_client,
    token, test_users, test_requests, test_quizzes, test_members_for_company, test_questions, test_quiz_results)
from . import help_to_tests_data


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_get_quizzes(authorized_client, test_companies, test_members_for_company):
    response = await authorized_client.get(
        f'companies/{test_companies[0].id}/quiz/',
    )
    assert response.status_code == 200


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_create_quiz(authorized_client, test_companies):
    response = await authorized_client.post(
        f'companies/{test_companies[0].id}/quiz/',
        json={
          "name": "Test",
          "descriptions": "string",
          "frequency": 5
        }
    )
    assert response.status_code == 201
    assert response.json() == {
        "created_at": response.json().get("created_at"),
        "updated_at": response.json().get("updated_at"),
        "name": "Test",
        "descriptions": "string",
        "frequency": 5,
        "id": 1,
        "owner_id": 1
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_create_question(authorized_client, test_companies, test_quizzes):
    response = await authorized_client.post(
        f'companies/{test_companies[0].id}/quiz/{test_quizzes[0].id}/questions/',
        json={
            "name": "Have are you?",
            "choice_answers": [
                "good",
                "fine",
                "bad"
            ],
            "correct_answers": [
                0
            ]
        }
    )
    assert response.status_code == 201
    assert response.json() == {
            "name": "Have are you?",
            "choice_answers": [
                "good",
                "fine",
                "bad"
            ],
            "correct_answers": [
                0
            ],
            "id": 1,
            "quiz_id": 1
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_update_quiz(authorized_client, test_companies, test_quizzes):
    response = await authorized_client.put(
        f'companies/{test_companies[0].id}/quiz/{test_quizzes[0].id}',
        json={
          "name": "Test",
          "descriptions": "string",
          "frequency": 7
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "created_at": response.json().get("created_at"),
        "updated_at": response.json().get("updated_at"),
        "name": "Test",
        "descriptions": "string",
        "frequency": 7,
        "id": 1,
        "owner_id": 1
    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_take_to_quiz(authorized_client, test_companies, test_quizzes, test_questions, test_members_for_company):
    response = await authorized_client.post(
        f'companies/{test_companies[0].id}/quiz/{test_quizzes[0].id}/take_quiz',
        json=help_to_tests_data.answers_1
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "user_id": 1,
        "quiz_id": 1,
        "company_id": 1,
        "number_of_questions": 4,
        "number_of_correct_answers": 2,
        "sum_all_questions": 4,
        "sum_all_correct_answers": 2,
        "gpa": 0.5,
        "gpa_all": 0.5,
        "created_at": response.json().get("created_at")

    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_check_update_gpa(
        authorized_client,
        test_companies,
        test_quizzes,
        test_questions,
        test_members_for_company,
        test_quiz_results
):
    response = await authorized_client.post(
        f'companies/{test_companies[0].id}/quiz/{test_quizzes[0].id}/take_quiz',
        json=help_to_tests_data.answers_2
    )
    print(response.json())
    assert response.status_code == 201
    assert response.json() == {
        "id": 4,
        "user_id": 1,
        "quiz_id": 1,
        "company_id": 1,
        "number_of_questions": 4,
        "number_of_correct_answers": 4,
        "sum_all_questions": test_quiz_results[-1].sum_all_questions + 4,
        "sum_all_correct_answers": test_quiz_results[-1].sum_all_correct_answers + 4,
        "gpa": round(4 / 4, 3),
        "gpa_all": round((test_quiz_results[-1].sum_all_correct_answers + 4) /
                         (test_quiz_results[-1].sum_all_questions + 4), 3),
        "created_at": response.json().get("created_at")

    }


@pytest.mark.anyio
@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_delete_quiz(authorized_client, test_companies, test_quizzes):
    response = await authorized_client.delete(
        f'companies/{test_companies[0].id}/quiz/{test_quizzes[0].id}',
    )
    assert response.status_code == 204
