from app.application.dto.request_dto import RequestSummary
from app.application.exceptions.request_exceptions import RequestNotFoundError
from app.domain.repositories.request_repository import RequestRepository


class GetRequestUseCase:
    def __init__(self, repository: RequestRepository) -> None:
        self._repository = repository

    def execute(self, request_id: int) -> RequestSummary:
        request = self._repository.get_by_id(request_id)
        if request is None:
            raise RequestNotFoundError("request not found")

        return RequestSummary(
            id=request.id if request.id is not None else request_id,
            external_identifier=request.external_identifier,
            category=request.category.value,
            requester_name=request.requester_name,
            requester_email=request.requester_email,
            description=request.description,
            priority=request.priority.value,
            status=request.status.value,
            created_at=request.created_at,
            updated_at=request.updated_at,
        )
