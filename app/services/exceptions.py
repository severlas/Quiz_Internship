from fastapi import HTTPException, status
from log.config_log import logger


class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )
        logger.error(f'status: HTTP_404_NOT_FOUND, detail: {detail}')


class PermissionError(HTTPException):
    def __init__(
            self,
            detail: str = "Not authorized to perform requested action",
            log_detail: str = "Permission Error"
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )
        logger.error(f'status: HTTP_403_FORBIDDEN, detail: {log_detail}')


class AuthenticateError(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={'WWW-Authenticate': 'Bearer'}
        )
        logger.error(f'status: HTTP_401_UNAUTHORIZED, detail: {detail}')
