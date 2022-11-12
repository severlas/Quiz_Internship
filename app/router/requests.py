from fastapi import APIRouter, Depends, status as status_code, Response
from typing import List, Optional
from app.schemas.requests import CreateRequest, Request, RequestStatus, RequestSender
from app.services.companies import CompanyService
from app.services.requests import RequestInCompanyService
from app.services.auth import get_current_user
from app.models.requests import RequestModel
from app.models.users import UserModel
from app.schemas.paginations import RequestPagination


router = APIRouter(
    prefix='/requests',
    tags=['Request']
)


@router.get('/', response_model=List[Request])
async def get_requests(
        pagination: RequestPagination = Depends(),
        service: RequestInCompanyService = Depends(),
        status: Optional[RequestStatus] = None,
        sender: Optional[RequestSender] = None,
        company_id: Optional[int] = None
) -> List[Request]:
    return await service.get_requests(
        pagination=pagination,
        status=status,
        sender=sender,
        company_id=company_id
    )


@router.get('/{id}', response_model=Request)
async def get_request(
        id: int,
        service: RequestInCompanyService = Depends(),
        user: UserModel = Depends(get_current_user)
) -> Request:
    return await service.get_request(id=id, user_id=user.id)


@router.post('/', response_model=Request, status_code=status_code.HTTP_201_CREATED)
async def send_request(
        request_data: CreateRequest,
        service: RequestInCompanyService = Depends(),
        user: UserModel = Depends(get_current_user)

) -> RequestModel:
    return await service.send_request(request_data=request_data, user_id=user.id)


@router.put('/{id}', status_code=status_code.HTTP_204_NO_CONTENT)
async def update_request(
        id: int,
        status: RequestStatus,
        service: RequestInCompanyService = Depends(),
        user: UserModel = Depends(get_current_user)

):
    return await service.update_request(id=id, user_id=user.id, status=status)
