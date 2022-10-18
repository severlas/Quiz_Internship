from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import AuthService
from app.schemas.users import SignInRequestModel

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/sign-in')
def sign_in(
        user_data: SignInRequestModel = Depends(),
        service: AuthService = Depends()
):
    return service.sign_in(user_data)
