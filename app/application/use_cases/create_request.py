from app.application.dto.request_dto import CreateRequestCommand, RequestSummary
from app.application.exceptions.request_exceptions import RequestAlreadyExistsError
from app.application.ports.clock import Clock
from app.domain.entities.request import Solicitud
from app.domain.repositories.request_repository import RequestRepository
from app.domain.value_objects.request_catalogs import RequestCategory, RequestPriority


class CreateRequestUseCase:
    def __init__(self, repository: RequestRepository, clock: Clock) -> None:
        self._repository = repository
        self._clock = clock

    def execute(self, command: CreateRequestCommand) -> RequestSummary:
        existing_request = self._repository.get_by_external_identifier(command.external_identifier)
        if existing_request is not None:
            raise RequestAlreadyExistsError("request already exists")

        request = Solicitud(
            external_identifier=command.external_identifier,
            category=RequestCategory(command.category),
            requester_name=command.requester_name,
            requester_email=command.requester_email,
            description=command.description,
            priority=RequestPriority(command.priority),
        )
        request.created_at = self._clock.now()
        request.updated_at = request.created_at
        saved_request = self._repository.add(request)
        return RequestSummary(
            id=saved_request.id,
            external_identifier=saved_request.external_identifier,
            category=saved_request.category.value,
            requester_name=saved_request.requester_name,
            requester_email=saved_request.requester_email,
            description=saved_request.description,
            priority=saved_request.priority.value,
            status=saved_request.status.value,
            created_at=saved_request.created_at,
            updated_at=saved_request.updated_at,
        )
