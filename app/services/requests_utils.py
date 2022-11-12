from enum import Enum


class RequestStatus(str, Enum):
    CREATED = 'created'
    CONFIRMED = 'confirmed'
    REJECTED = 'rejected'


class RequestSender(str, Enum):
    USER = 'user'
    COMPANY = 'company'

