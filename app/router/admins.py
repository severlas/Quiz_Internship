from fastapi import APIRouter, Depends
from typing import List
from app.services.admins import AdminService
from app.schemas.companies import NestedUser, CompanyAdmin
from app.services.auth import get_current_user
from app import models


router = APIRouter(
    prefix='/{id}/admins'
)


@router.get('/', response_model=List[NestedUser])
async def get_admins(
        id: int,
        service: AdminService = Depends(),
        user: models.User = Depends(get_current_user)
) -> List[NestedUser]:
    return await service.get_admins(company_id=id, user_id=user.id)


@router.post('/', response_model=CompanyAdmin)
async def create_admin(
        id: int,
        admin_id: int,
        service: AdminService = Depends(),
        user: models.User = Depends(get_current_user)
):
    return await service.create_admin(company_id=id, admin_id=admin_id, user_id=user.id)


@router.delete('/{admin_id}')
async def delete_admin(
        id: int,
        admin_id: int,
        service: AdminService = Depends(),
        user: models.User = Depends(get_current_user)
):
    return await service.delete_admin(company_id=id, admin_id=admin_id, user_id=user.id)
