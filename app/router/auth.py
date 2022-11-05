from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import AuthService
from app.schemas.users import SignInRequestModel, TokenJWT


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/sign-in')
async def sign_in(
        user_data: SignInRequestModel,
        service: AuthService = Depends()
) -> TokenJWT:
    return await service.sign_in(user_data=user_data)
