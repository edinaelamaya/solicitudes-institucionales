from app.application.dto.request_dto import RequestSummary, UpdateRequestStatusCommand
from app.application.exceptions.request_exceptions import RequestNotFoundError
from app.domain.repositories.request_repository import RequestRepository
from app.domain.value_objects.request_catalogs import RequestStatus


class UpdateRequestStatusUseCase:
    def __init__(self, repository: RequestRepository) -> None:
        self._repository = repository

    def execute(self, command: UpdateRequestStatusCommand) -> RequestSummary:
        request = self._repository.get_by_id(command.request_id)
        if request is None:
            raise RequestNotFoundError("request not found")

        request.change_status(RequestStatus(command.status))
        updated_request = self._repository.update(request)
        return RequestSummary(
            id=updated_request.id,
            external_identifier=updated_request.external_identifier,
            category=updated_request.category.value,
            requester_name=updated_request.requester_name,
            requester_email=updated_request.requester_email,
            description=updated_request.description,
            priority=updated_request.priority.value,
            status=updated_request.status.value,
            created_at=updated_request.created_at,
            updated_at=updated_request.updated_at,
        )
