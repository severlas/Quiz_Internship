from fastapi import APIRouter, Depends
from typing import List
from app.services.members import MemberService
from app.schemas.companies import NestedUser
from app.services.auth import get_current_user
from app.models.users import UserModel


router = APIRouter(
    prefix='/{id}/members'
)


@router.get('/', response_model=List[NestedUser])
async def get_members(
        id: int,
        service: MemberService = Depends(),
        user: UserModel = Depends(get_current_user)
) -> List[NestedUser]:
    return await service.get_members(company_id=id, user_id=user.id)


@router.delete('/{member_id}')
async def delete_member(
        id: int,
        member_id: int,
        service: MemberService = Depends(),
        user: UserModel = Depends(get_current_user)
):
    return await service.delete_member(
        company_id=id,
        member_id=member_id,
        user_id=user.id
    )
