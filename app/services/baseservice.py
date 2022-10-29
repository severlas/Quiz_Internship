from fastapi import Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
from app.database import get_postgres_db
from app.schemas.companies import CreateCompany, Company, UpdateCompany
from app.schemas.requests import CreateRequest, Request, RequestStatus
from app.models.users import UserModel
from app.models.requests import RequestModel
from app.models import companies
from app.services.exceptions import PermissionError, NotFoundError


class BaseService:
    def __init__(self, db: AsyncSession = Depends(get_postgres_db)):
        self.db = db

    """Protected method get user by id"""
    async def _get_user_by_id(self, id: int) -> UserModel:
        user = await self.db.execute(select(UserModel).filter_by(id=id))
        user = user.scalar()
        if not user:
            raise NotFoundError(
                detail=f'User with id:{id} was not found',
            )
        return user

    """Protected method get company by id"""
    async def _get_company_by_id(self, id: int) -> companies.CompanyModel:
        company = await self.db.execute(select(companies.CompanyModel).filter_by(id=id))
        company = company.scalar()
        if not company:
            raise NotFoundError(
                detail=f"Company with id:{id} was not found!"
            )
        return company

    """Protected method get companies by owner id"""
    async def _get_companies_by_owner_id(self, owner_id: int) -> List[companies.CompanyModel]:
        companies = await self.db.execute(select(companies.CompanyModel).filter_by(owner_id=owner_id))
        companies = companies.scalars().all()
        return companies

    """Protected method get admins by company id"""
    async def _get_admins_by_company_id(self, id: int) -> List[int]:
        admins = await self.db.execute(select(companies.admins).filter_by(company_id=id))
        admins = admins.scalars().all()
        return admins

    """Protected method get staff by company id"""
    async def _get_members_by_company_id(self, id: int) -> List[int]:
        members = await self.db.execute(select(companies.members).filter_by(company_id=id))
        members = members.scalars().all()
        return members

    """Protected method get requests by company id"""
    async def _get_requests_by_company_id(self, id: int) -> List[Request]:
        requests = await self.db.execute(select(RequestModel).filter_by(company_id=id))
        requests = requests.scalars().all()
        return requests

    """Protected method get requests by user id"""
    async def _get_requests_by_user_id(self, id: int) -> List[Request]:
        requests = await self.db.execute(select(RequestModel).filter_by(user_id=id))
        requests = requests.scalars().all()
        return requests

    """Protected method get request by id"""
    async def _get_request_by_id(self, id: int) -> Request:
        request = await self.db.execute(select(RequestModel).filter_by(id=id))
        request = request.scalar()
        if not request:
            raise NotFoundError(
                detail=f"Request with id:{id} was not found!"
            )
        return request

    """Protected method create admin"""
    async def _create_admin(self, user_id: int, company_id: int) -> companies.admins:
        admin = companies.admins.insert().values(
            user_id=user_id,
            company_id=company_id
        )
        await self.db.execute(admin)
        await self.db.commit()
        return admin

    """Protected method create staff"""
    async def _create_member(self, user_id: int, company_id: int) -> companies.members:
        member = companies.members.insert().values(
            user_id=user_id,
            company_id=company_id
        )
        await self.db.execute(member)
        await self.db.commit()
        return member

