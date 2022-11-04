import pytest
from app.main import app
from app.database import get_postgres_db
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.users import UserJWT, TokenJWT
from app.services.auth import AuthService
from app.models.companies import CompanyModel, members as MemberModel
from app.models.users import UserModel
from app.models.requests import RequestModel
from app.models.quiz import QuizModel, QuestionModel
from sqlalchemy import select, delete


@pytest.fixture
async def test_users(get_test_db) -> List[UserModel]:
    users_data = [
        {
            "email": "vladimir@gmail.com",
            "username": "vladimir",
            "password": "vladimir"
        },
        {
            "email": "karina@gmail.com",
            "username": "karina",
            "password": "karina"
        },
        {
            "email": "darya@gmail.com",
            "username": "darya",
            "password": "darya"
        },
        {
            "email": "serhii@gmail.com",
            "username": "serhii",
            "password": "serhii"
        }
    ]

    user_map = map(lambda user: UserModel(**user), users_data)
    users = list(user_map)
    get_test_db.add_all(users)
    await get_test_db.commit()

    users = await get_test_db.execute(select(UserModel))
    return users.scalars().all()


@pytest.fixture()
async def client(get_test_db) -> AsyncClient:
    async def test_db():
        try:
            yield get_test_db
        finally:
            await get_test_db.close()
    app.dependency_overrides[get_postgres_db] = test_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def token(test_users: List[UserModel]) -> TokenJWT:
    return AuthService.create_token(
        UserJWT(id=test_users[0].id, email=test_users[0].email)
    )


@pytest.fixture
async def authorized_client(client: AsyncClient, token: TokenJWT) -> AsyncClient:
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token.access_token}"
    }
    return client


@pytest.fixture
async def test_companies(test_users: List[UserModel], get_test_db: AsyncSession):
    companies_data = [
        {
            "name": "BMW",
            "descriptions": "Inform about cars",
            "visibility": True,
            "owner_id": test_users[0].id,
        },
        {
            "name": "Windows",
            "descriptions": "Inform about OS",
            "visibility": False,
            "owner_id": test_users[1].id,
        },
        {
            "name": "Meduzzen",
            "descriptions": "Inform about web development",
            "visibility": True,
            "owner_id": test_users[2].id,
        }
    ]

    company_map = map(lambda company: CompanyModel(**company), companies_data)
    companies = list(company_map)
    get_test_db.add_all(companies)
    await get_test_db.commit()

    companies = await get_test_db.execute(select(CompanyModel))
    return companies.scalars().all()


@pytest.fixture
async def test_requests(
        test_users: List[UserModel],
        test_companies: List[CompanyModel],
        get_test_db: AsyncSession
) -> List[RequestModel]:
    requests_data = [
        {
            "sender": "user",
            "status": "created",
            "company_id": test_companies[0].id,
            "user_id": test_users[1].id
        },
        {
            "sender": "company",
            "status": "created",
            "company_id": test_companies[1].id,
            "user_id": test_users[0].id
        },
        {
            "sender": "company",
            "status": "created",
            "company_id": test_companies[2].id,
            "user_id": test_users[0].id
        }
    ]

    request_map = map(lambda request: RequestModel(**request), requests_data)
    requests = list(request_map)
    get_test_db.add_all(requests)
    await get_test_db.commit()

    requests = await get_test_db.execute(select(RequestModel))
    return requests.scalars().all()


@pytest.fixture
async def test_members_for_company(
        test_users: List[UserModel],
        test_companies: List[CompanyModel],
        get_test_db: AsyncSession
) -> MemberModel:
    members_data = [
        {
            "user_id": test_users[0].id,
            "company_id": test_companies[0].id,
        },
        {
            "user_id": test_users[1].id,
            "company_id": test_companies[1].id,
        }
    ]
    members = [
        MemberModel.insert().values(
            user_id=member.get("user_id"), company_id=member.get("company_id")
        ) for member in members_data
    ]

    await get_test_db.execute(members[0])
    await get_test_db.commit()
    members = await get_test_db.execute(select(MemberModel))
    return members.scalars().all()


@pytest.fixture
async def test_quizzes(
        test_users: List[UserModel],
        test_companies: List[CompanyModel],
        get_test_db: AsyncSession
) -> List[QuizModel]:
    quizzes_data = [
        {
            "name": "Test_1",
            "descriptions": "information",
            "frequency": 7,
            "owner_id": test_users[0].id,
            "company_id": test_companies[0].id
        },
        {
            "name": "Test_2",
            "descriptions": "information",
            "frequency": 7,
            "owner_id": test_users[1].id,
            "company_id": test_companies[1].id
        },

    ]

    quiz_map = map(lambda quiz: QuizModel(**quiz), quizzes_data)
    quizzes = list(quiz_map)
    get_test_db.add_all(quizzes)
    await get_test_db.commit()

    quizzes = await get_test_db.execute(select(QuizModel))
    return quizzes.scalars().all()


@pytest.fixture
async def test_questions(get_test_db: AsyncSession) -> List[QuestionModel]:
    questions_data = [
        {
            "name": "На підприємстві в процесі виробництва утворюються особливо токсичні перероблювані "
                    "промислові відходи. Запропонуйте методутилізації та знешкодження.",
            "choice_answers": [
                "Біотермічна переробка на удосконалених звалищах.",
                "Поховання в котлованах полігонів з ізоляцією дна і стінок ущільнюючимшаром глини",
                "Використання як сировини для повторної переробки.",
                "Поховання в котлованах полігонів в контейнерному тарі.",
                "Термічна обробка."
            ],
            "correct_answers": [
                3
            ],
            "quiz_id": 1
        },
        {
            "name": "Укажіть відходи, що відносяться до рідких відходів:",
            "choice_answers": [
                "Помиї від приготування їжі, миття посуду, підлоги, прання білизни",
                "Нечистоти з вигребів туалетів",
                "Господарсько-побутові стічні води",
                "Все перераховане",
                "Промислові, зливові, міські стічні води"
            ],
            "correct_answers": [
                3
            ],
            "quiz_id": 1
        },
        {
            "name": "Назвіть ступені забруднення ґрунту:",
            "choice_answers": [
                "Чистий, слабо забруднений, забруднений, сильно забруднений",
                "Безпечний, відносно безпечний, небезпечний, надзвичайно небезпечний",
                "Чистий, забруднений, безпечний, небезпечний",
                "Чистий, відносно забруднення, забруднений, недостатньо забруднений",
                "Нижче ГДК, на рівні ГДК, вище ГДК"
            ],
            "correct_answers": [
                0
            ],
            "quiz_id": 1
        },
        {
            "name": "У сільському населеному пункті з децентралізованим водопостачанням",
            "choice_answers": [
                "фтору",
                "миш'яку",
                "стронцію",
                "свинцю",
                "йоду"
            ],
            "correct_answers": [
                2
            ],
            "quiz_id": 1
        }
    ]

    question_map = map(lambda question: QuestionModel(**question), questions_data)
    questions = list(question_map)
    get_test_db.add_all(questions)
    await get_test_db.commit()

    questions = await get_test_db.execute(select(QuestionModel))
    return questions.scalars().all()
