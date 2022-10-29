from fastapi import Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Optional
from app.database import get_postgres_db
from app.schemas.companies import CreateCompany, Company, CompanyDetail, UpdateCompany, CompanyAdmin
from app.schemas.requests import CreateRequest, Request, RequestStatus
from app.schemas.users import NestedUser
from app.schemas.paginations import CompanyPagination
from app.models.companies import CompanyModel
from app.services.exceptions import PermissionError, NotFoundError
from app.services.baseservice import BaseService
from log.config_log import logger
from datetime import datetime


class CompanyService(BaseService):
    """Company CRUD"""

    """Get list companies"""
    async def get_companies(
            self,
            pagination: CompanyPagination,
            owner_id: Optional[int] = None
    ) -> List[Company]:
        query = (
            select(CompanyModel).
            limit(pagination.limit).offset(pagination.skip).
            filter_by(visibility=True)
        )
        if owner_id:
            query = query.filter_by(owner_id=owner_id)
        companies = await self.db.execute(query)
        companies = companies.scalars().all()
        return companies

    """Get company by id"""
    async def get_company(self, id: int, user_id: int) -> CompanyDetail:
        company = await self._get_company_by_id(id)
        if not company.visibility and company.owner_id != user_id:
            raise PermissionError

        admins = await self._get_admins_by_company_id(id)
        members = await self._get_members_by_company_id(id)
        requests = await self._get_requests_by_company_id(id)
        company_data = CompanyDetail(
            **company.__dict__,
            admins=[{"id": admin_id} for admin_id in admins],
            members=[{"id": member_id} for member_id in members],
            requests=requests
        )

        return company_data

    """Create company"""
    async def create_company(self, user_id: int, company_data: CreateCompany) -> CompanyModel:
        company = CompanyModel(
            **company_data.dict(),
            owner_id=user_id,
        )
        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)

        await self._create_admin(user_id=user_id, company_id=company.id)
        await self._create_member(user_id=user_id, company_id=company.id)
        logger.info(f"Company created successfully! 'data': {company_data.dict()}")
        return company

    """Update company by id"""
    async def update_company(self, id: int, user_id: int, company_data: UpdateCompany) -> CompanyModel:
        company = await self._get_company_by_id(id)

        if user_id != company.owner_id:
            raise PermissionError(
                log_detail=f"User with id:{user_id} wanted to update company data with id:{id}!"
            )
        for field, value in company_data:
            if value != None:
                setattr(company, field, value)

        company.updated_at = datetime.now()
        await self.db.commit()
        await self.db.refresh(company)
        logger.info(f"Company with id:{id} updated successfully! 'data': {company_data.dict(exclude_unset=True)}")
        return company

    """Delete company by id"""
    async def delete_company(self, id: int, user_id: int) -> Response:
        company = await self._get_company_by_id(id)
        if not company:
            raise NotFoundError(
                detail=f"Company with id:{id} was not found!"
            )
        if user_id != company.owner_id:
            raise PermissionError(
                log_detail=f"User with id:{user_id} wanted to delete company with id:{id}!"
            )

        await self.db.execute(delete(CompanyModel).where(CompanyModel.id == id))
        await self.db.commit()
        logger.info(f"Company with id:{id} deleted successfully!")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
