from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.users import User, SignInRequestModel, TokenJWT
from app.services.users import UserService

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/sign-in')
def sign_in(
        user_data: SignInRequestModel,
        service: UserService = Depends()
):
    return service.sign_in(user_data)
