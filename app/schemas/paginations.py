from pydantic import BaseModel


class BasePagination(BaseModel):
    limit: int = 5
    skip: int = 0


class UserPagination(BasePagination):
    pass


class CompanyPagination(BasePagination):
    pass


class RequestPagination(BasePagination):
    pass
