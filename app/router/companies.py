from fastapi import APIRouter, Depends, status, Response
from typing import List, Optional
from app.schemas.companies import Company, CreateCompany, CompanyDetail
from app.schemas.requests import CreateRequest, Request
from app.services.companies import CompanyService
from app.services.auth import get_current_user
from app.schemas.paginations import CompanyPagination
from app import models
from app.router.admins import router as admins_router
from app.router.members import router as members_router

router = APIRouter(
    prefix='/companies',
    tags=['Company']
)


@router.get('/', response_model=List[Company])
async def get_companies(
        pagination: CompanyPagination = Depends(),
        service: CompanyService = Depends(),
        owner_id: Optional[int] = None
) -> List[Company]:
    return await service.get_companies(pagination=pagination, owner_id=owner_id)


@router.get('/{id}', response_model=CompanyDetail)
async def get_company(
        id: int,
        service: CompanyService = Depends(),
        user: models.User = Depends(get_current_user)
) -> CompanyDetail:
    return await service.get_company(id=id, user_id=user.id)


@router.post('/', response_model=Company, status_code=status.HTTP_201_CREATED)
async def create_company(
        company_data: CreateCompany,
        service: CompanyService = Depends(),
        user: models.User = Depends(get_current_user)
) -> models.Company:
    return await service.create_company(company_data=company_data, user_id=user.id)


@router.put('/{id}', response_model=Company)
async def update_company(
        id: int,
        company_data: CreateCompany,
        service: CompanyService = Depends(),
        user: models.User = Depends(get_current_user)
) -> models.Company:
    return await service.update_company(id=id, company_data=company_data, user_id=user.id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
        id: int,
        service: CompanyService = Depends(),
        user: models.User = Depends(get_current_user)
):
    return await service.delete_company(id=id, user_id=user.id)


router.include_router(members_router)
router.include_router(admins_router)
