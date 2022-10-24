from fastapi import Depends, Response, status
from sqlalchemy import select, delete
from typing import List
from app.schemas.companies import CompanyAdmin
from app.schemas.users import NestedUser
from app.schemas.paginations import UserPagination
from app import models
from app.services.exceptions import PermissionError, NotFoundError
from app.services.baseservice import BaseService
from log.config_log import logger
from datetime import datetime


class AdminService(BaseService):
    """Assign admins or delete admins"""

    """Get list admins"""
    async def get_admins(self, company_id: int, user_id: int) -> List[NestedUser]:
        company = await self._get_company_by_id(id=company_id)
        if company.visibility is False and user_id != company.owner_id:
            raise NotFoundError

        admins_id = await self._get_admins_by_company_id(id=company_id)
        admins = [await self._get_user_by_id(admin_id) for admin_id in admins_id]
        return admins

    """Assign an admin from the company's staff by user id"""
    async def create_admin(self, company_id: int, admin_id: int, user_id: int) -> CompanyAdmin:
        company = await self._get_company_by_id(id=company_id)
        if user_id != company.owner_id:
            raise PermissionError(
                log_detail=f"User with id:{user_id} wanted to assign admin with id:{admin_id} in"
                           f"company with id:{company_id}!"
            )
        members = await self._get_members_by_company_id(id=company_id)
        if admin_id not in staff:
            raise NotFoundError(
                detail=f"User with id:{admin_id} isn't included in the staff!"
            )
        user = await self._get_user_by_id(id=admin_id)
        await self._create_admin(company_id=company_id, user_id=admin_id)
        admin = CompanyAdmin(
            company_id=company_id,
            admin=user
        )
        logger.info(f"In company with id:{company_id} assigned admin with id:{admin_id}!")
        return admin

    """Delete status admin by id"""
    async def delete_admin(self, company_id: int, admin_id: int, user_id: int):
        company = await self._get_company_by_id(id=company_id)
        if user_id != company.owner_id:
            raise PermissionError(
                log_detail=f"User with id:{user_id} wanted to delete admin with id:{admin_id} in"
                           f"company with id:{company_id}!"
            )
        admins = await self._get_admins_by_company_id(id=company_id)
        if admin_id not in admins:
            raise NotFoundError(
                detail=f"Admin with id:{admin_id} was not found!"
            )

        await self.db.execute(delete(models.admins).filter_by(company_id=company_id, user_id=admin_id))
        await self.db.commit()
        logger.info(f"In company with id:{company_id} admin with id:{admin_id} deleted successfully!")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
