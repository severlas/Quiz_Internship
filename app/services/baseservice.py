from fastapi import Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
from app.database import get_postgres_db
from app.schemas.companies import CreateCompany, Company, UpdateCompany
from app.schemas.requests import CreateRequest, Request, RequestStatus
from app import models
from app.services.exceptions import PermissionError, NotFoundError


class BaseService:
    def __init__(self, db: AsyncSession = Depends(get_postgres_db)):
        self.db = db

    """Protected method get user by id"""
    async def _get_user_by_id(self, id: int) -> models.User:
        user = await self.db.execute(select(models.User).filter_by(id=id))
        user = user.scalar()
        if not user:
            raise NotFoundError(
                detail=f'User with id:{id} was not found',
            )
        return user

    """Protected method get company by id"""
    async def _get_company_by_id(self, id: int) -> models.Company:
        company = await self.db.execute(select(models.Company).filter_by(id=id))
        company = company.scalar()
        if not company:
            raise NotFoundError(
                detail=f"Company with id:{id} was not found!"
            )
        return company

    """Protected method get companies by owner id"""
    async def _get_companies_by_owner_id(self, owner_id: int) -> List[models.Company]:
        companies = await self.db.execute(select(models.Company).filter_by(owner_id=owner_id))
        companies = companies.scalars().all()
        return companies

    """Protected method get admins by company id"""
    async def _get_admins_by_company_id(self, id: int) -> List[int]:
        admins = await self.db.execute(select(models.admins).filter_by(company_id=id))
        admins = admins.scalars().all()
        return admins

    """Protected method get staff by company id"""
    async def _get_staff_by_company_id(self, id: int) -> List[int]:
        staff = await self.db.execute(select(models.staff).filter_by(company_id=id))
        staff = staff.scalars().all()
        return staff

    """Protected method get requests by company id"""
    async def _get_requests_by_company_id(self, id: int) -> List[Request]:
        requests = await self.db.execute(select(models.Request).filter_by(company_id=id))
        requests = requests.scalars().all()
        return requests

    """Protected method get requests by user id"""
    async def _get_requests_by_user_id(self, id: int) -> List[Request]:
        requests = await self.db.execute(select(models.Request).filter_by(user_id=id))
        requests = requests.scalars().all()
        return requests

    """Protected method get request by id"""
    async def _get_request_by_id(self, id: int) -> Request:
        request = await self.db.execute(select(models.Request).filter_by(id=id))
        request = request.scalar()
        if not request:
            raise NotFoundError(
                detail=f"Request with id:{id} was not found!"
            )
        return request

    """Protected method create admin"""
    async def _create_admin(self, user_id: int, company_id: int) -> models.admins:
        admin = models.admins.insert().values(
            user_id=user_id,
            company_id=company_id
        )
        await self.db.execute(admin)
        await self.db.commit()
        return admin

    """Protected method create staff"""
    async def _create_staff(self, user_id: int, company_id: int) -> models.staff:
        staff = models.staff.insert().values(
            user_id=user_id,
            company_id=company_id
        )
        await self.db.execute(staff)
        await self.db.commit()
        return staff

