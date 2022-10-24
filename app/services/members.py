from fastapi import Depends, Response, status
from sqlalchemy import select, delete
from typing import List
from app.schemas.users import NestedUser
from app.schemas.paginations import UserPagination
from app import models
from app.services.exceptions import PermissionError, NotFoundError
from app.services.baseservice import BaseService
from log.config_log import logger
from datetime import datetime


class MemberService(BaseService):
    """Get member or delete member"""

    """Get list members"""
    async def get_members(self, company_id: int, user_id: int) -> List[NestedUser]:
        company = await self._get_company_by_id(id=company_id)
        if company.visibility is False and user_id != company.owner_id:
            raise NotFoundError
        members_id = await self._get_members_by_company_id(id=company_id)
        members = [await self._get_user_by_id(member_id) for member_id in members_id]
        return members

    """Delete member by id"""
    async def delete_member(self, company_id: int, member_id: int, user_id: int):
        company = await self._get_company_by_id(id=company_id)

        if user_id != company.owner_id:
            raise PermissionError(
                log_detail=f"User with id:{user_id} wanted to delete member with id:{member_id} in"
                           f"company with id:{company_id}!"
            )
        members = await self._get_members_by_company_id(id=company_id)
        if member_id not in members:
            raise NotFoundError(
                detail=f"Member with id:{member_id} was not found!"
            )

        await self.db.execute(delete(models.members).filter_by(company_id=company_id, user_id=member_id))
        await self.db.commit()
        logger.info(f"In company with id:{company_id} member with id:{member_id} deleted successfully!")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
