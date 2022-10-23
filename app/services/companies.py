from fastapi import Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Optional
from app.database import get_postgres_db
from app.schemas.companies import CreateCompany, Company, CompanyDetail, UpdateCompany, CompanyAdmin
from app.schemas.requests import CreateRequest, Request, RequestStatus
from app.schemas.users import NestedUser
from app.schemas.paginations import CompanyPagination
from app import models
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
            select(models.Company).
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
        staff = await self._get_staff_by_company_id(id)
        requests = await self._get_requests_by_company_id(id)
        company_data = CompanyDetail(
            **company.__dict__,
            admins=[{"id": admin_id} for admin_id in admins],
            staff=[{"id": s_id} for s_id in staff],
            requests=requests
        )

        return company_data

    """Create company"""
    async def create_company(self, user_id: int, company_data: CreateCompany) -> models.Company:
        company = models.Company(
            **company_data.dict(),
            owner_id=user_id,
        )
        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)

        await self._create_admin(user_id=user_id, company_id=company.id)
        await self._create_staff(user_id=user_id, company_id=company.id)
        logger.info(f"Company created successfully! 'data': {company_data.dict()}")
        return company

    """Update company by id"""
    async def update_company(self, id: int, user_id: int, company_data: UpdateCompany) -> models.Company:
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
    async def delete_company(self, id: int, user_id: int):
        company = await self._get_company_by_id(id)
        if not company:
            raise NotFoundError(
                detail=f"Company with id:{id} was not found!"
            )
        if user_id != company.owner_id:
            raise PermissionError(
                log_detail=f"User with id:{user_id} wanted to delete company with id:{id}!"
            )

        await self.db.execute(delete(models.Company).where(models.Company.id == id))
        await self.db.commit()
        logger.info(f"Company with id:{id} deleted successfully!")
        return Response(status_code=status.HTTP_204_NO_CONTENT)


class CompanyAdminService(BaseService):
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
        staff = await self._get_staff_by_company_id(id=company_id)
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


class StaffInCompanyService(BaseService):
    """Get staff or delete staff"""

    """Get list staff"""
    async def get_staff(self, company_id: int, user_id: int) -> List[NestedUser]:
        company = await self._get_company_by_id(id=company_id)
        if company.visibility is False and user_id != company.owner_id:
            raise NotFoundError
        staff_id = await self._get_staff_by_company_id(id=company_id)
        staff = [await self._get_user_by_id(id) for id in staff_id]
        return staff

    """Delete employee by id"""
    async def delete_employee(self, company_id: int, employee_id: int, user_id: int):
        company = await self._get_company_by_id(id=company_id)

        if user_id != company.owner_id:
            raise PermissionError(
                log_detail=f"User with id:{user_id} wanted to delete employee with id:{employee_id} in"
                           f"company with id:{company_id}!"
            )
        staff = await self._get_staff_by_company_id(id=company_id)
        if employee_id not in staff:
            raise NotFoundError(
                detail=f"Employee with id:{employee_id} was not found!"
            )

        await self.db.execute(delete(models.staff).filter_by(company_id=company_id, user_id=employee_id))
        await self.db.commit()
        logger.info(f"In company with id:{company_id} employee with id:{employee_id} deleted successfully!")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
