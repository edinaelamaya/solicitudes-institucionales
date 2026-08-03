from app.application.use_cases.create_request import CreateRequestUseCase
from app.application.use_cases.get_request import GetRequestUseCase
from app.application.use_cases.get_requests import ListRequestsUseCase
from app.application.use_cases.update_request_status import UpdateRequestStatusUseCase
from app.infrastructure.repositories.sqlalchemy_request_repository import SQLAlchemyRequestRepository
from app.infrastructure.settings.clock import SystemClock


def get_request_repository() -> SQLAlchemyRequestRepository:
    return SQLAlchemyRequestRepository()


def get_clock() -> SystemClock:
    return SystemClock()


def get_create_request_use_case() -> CreateRequestUseCase:
    return CreateRequestUseCase(repository=get_request_repository(), clock=get_clock())


def get_list_requests_use_case() -> ListRequestsUseCase:
    return ListRequestsUseCase(repository=get_request_repository())


def get_get_request_use_case() -> GetRequestUseCase:
    return GetRequestUseCase(repository=get_request_repository())


def get_update_request_status_use_case() -> UpdateRequestStatusUseCase:
    return UpdateRequestStatusUseCase(repository=get_request_repository())
