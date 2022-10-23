from fastapi import APIRouter, Depends
from typing import List
from app.services.companies import StaffInCompanyService
from app.schemas.companies import NestedUser, CompanyAdmin
from app.services.auth import get_current_user
from app import models


router = APIRouter(
    prefix='/{id}/staff'
)


@router.get('/', response_model=List[NestedUser])
async def get_staff(
        id: int,
        service: StaffInCompanyService = Depends(),
        user: models.User = Depends(get_current_user)
) -> List[NestedUser]:
    return await service.get_staff(company_id=id, user_id=user.id)


@router.delete('/{employee_id}')
async def delete_employee(
        id: int,
        employee_id: int,
        service: StaffInCompanyService = Depends(),
        user: models.User = Depends(get_current_user)
):
    return await service.delete_employee(
        company_id=id,
        employee_id=employee_id,
        user_id=user.id
    )
