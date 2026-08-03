from app.application.dto.request_dto import RequestSummary
from app.domain.repositories.request_repository import RequestRepository
from app.domain.value_objects.request_catalogs import RequestCategory, RequestPriority, RequestStatus


class ListRequestsUseCase:
    def __init__(self, repository: RequestRepository) -> None:
        self._repository = repository

    def execute(
        self,
        *,
        status: str | None = None,
        category: str | None = None,
        priority: str | None = None,
    ) -> list[RequestSummary]:
        requests = self._repository.list(
            status=RequestStatus(status) if status else None,
            category=RequestCategory(category) if category else None,
            priority=RequestPriority(priority) if priority else None,
        )
        return [
            RequestSummary(
                id=request.id,
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
            for request in requests
        ]
