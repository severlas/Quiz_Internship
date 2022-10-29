from fastapi import Depends, Response, status as status_code
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Optional
from app.database import get_postgres_db
from app.schemas.companies import Company
from app.schemas.requests import CreateRequest, Request, RequestStatus, RequestSender
from app.models.requests import RequestModel
from app.models.companies import CompanyModel
from app.services.exceptions import PermissionError, NotFoundError
from app.services.baseservice import BaseService
from app.schemas.paginations import RequestPagination
from log.config_log import logger
from datetime import datetime


class RequestInCompanyService(BaseService):
    """Operation with requests"""

    """Check permission for create and edit request"""
    @classmethod
    async def _check_permission_for_send_request(
            cls,
            user_id: int,
            company: CompanyModel,
            request_data: CreateRequest,

    ) -> bool:
        if (user_id != request_data.user_id and user_id != company.owner_id) or (
            user_id == request_data.user_id and (not company.visibility or request_data.sender == 'company')
        ) or (user_id == company.owner_id and request_data.sender == 'user'):
            raise PermissionError
        return True

    @classmethod
    async def _check_permission_for_edit_status(
            cls,
            user_id: int,
            company: CompanyModel,
            request_data: CreateRequest,

    ) -> bool:
        if (user_id != request_data.user_id and user_id != company.owner_id) or (
                user_id == request_data.user_id and (not company.visibility or request_data.sender == 'user')
        ) or (user_id == company.owner_id and request_data.sender == 'company'):
            raise PermissionError
        return True

    """Get list requests"""
    async def get_requests(
            self,
            pagination: RequestPagination,
            status: Optional[RequestStatus] = None,
            sender: Optional[RequestSender] = None,
            company_id: Optional[int] = None
    ) -> List[Request]:
        companies = await self.db.execute(select(CompanyModel).filter_by(visibility=True))
        companies = companies.scalars().all()

        query = (
            select(RequestModel).
            limit(pagination.limit).offset(pagination.skip).
            filter(RequestModel.company_id.in_([company.id for company in companies]))
        )

        if company_id:
            query = query.filter_by(company_id=company_id)
        if status:
            query = query.filter_by(status=status)
        if sender:
            query = query.filter_by(sender=sender)

        requests = await self.db.execute(query)
        requests = requests.scalars().all()
        return requests

    """Get request by id"""
    async def get_request(self, id: int, user_id: int) -> RequestModel:
        request = await self._get_request_by_id(id)
        company = await self._get_company_by_id(id=request.company_id)
        if not company.visibility and user_id != request.user_id and user_id != company.owner_id:
            raise PermissionError
        return request

    """Send a request to join the company"""
    async def send_request(self, user_id: int, request_data: CreateRequest) -> RequestModel:
        company = await self._get_company_by_id(id=request_data.company_id)
        if await self._check_permission_for_send_request(user_id=user_id, company=company, request_data=request_data):
            request = RequestModel(**request_data.dict())
            self.db.add(request)
            await self.db.commit()
            await self.db.refresh(request)
            logger.info(f"Request created successfully! 'data': {request_data.dict()}")
            return request

    """Update request status"""
    async def update_request(self, id: int, user_id: int, status: RequestStatus) -> Response:
        request = await self.get_request(id=id, user_id=user_id)
        company = await self._get_company_by_id(id=request.company_id)
        if await self._check_permission_for_edit_status(user_id=user_id, company=company, request_data=request):
            request.status = status
            request.updated_at = datetime.now()
            if status == 'confirmed':
                await self._create_member(user_id=request.user_id, company_id=request.company_id)
                logger.info(f"Member with id:{request.user_id} added to company with id:{request.company_id}")
            if status != 'created':
                await self.db.execute(delete(RequestModel).filter_by(id=id))
                await self.db.commit()
            logger.info(f"Request with id:{id} status updated and request deleted successfully! 'status':{status}")
            return Response(status_code=status_code.HTTP_204_NO_CONTENT)
