from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import pytest

from app.application.dto.request_dto import CreateRequestCommand, UpdateRequestStatusCommand
from app.application.exceptions.request_exceptions import RequestAlreadyExistsError, RequestNotFoundError
from app.application.use_cases.create_request import CreateRequestUseCase
from app.application.use_cases.get_request import GetRequestUseCase
from app.application.use_cases.update_request_status import UpdateRequestStatusUseCase
from app.domain.entities.request import Solicitud
from app.domain.value_objects.request_catalogs import RequestCategory, RequestPriority, RequestStatus


@dataclass
class FakeClock:
    now_value: datetime

    def now(self) -> datetime:
        return self.now_value


class FakeRequestRepository:
    def __init__(self) -> None:
        self.storage: dict[int, Solicitud] = {}
        self.next_id = 1

    def add(self, request: Solicitud) -> Solicitud:
        request.id = self.next_id
        self.next_id += 1
        self.storage[request.id] = request
        return request

    def get_by_id(self, request_id: int) -> Solicitud | None:
        return self.storage.get(request_id)

    def get_by_external_identifier(self, external_identifier: str) -> Solicitud | None:
        for request in self.storage.values():
            if request.external_identifier == external_identifier:
                return request
        return None

    def list(self, *, status=None, category=None, priority=None):
        results = list(self.storage.values())
        if status is not None:
            results = [request for request in results if request.status == status]
        if category is not None:
            results = [request for request in results if request.category == category]
        if priority is not None:
            results = [request for request in results if request.priority == priority]
        return results

    def update(self, request: Solicitud) -> Solicitud:
        self.storage[request.id] = request
        return request


def test_create_request_use_case_creates_request() -> None:
    repository = FakeRequestRepository()
    clock = FakeClock(datetime(2026, 8, 2, 12, 0, tzinfo=timezone.utc))
    use_case = CreateRequestUseCase(repository=repository, clock=clock)

    result = use_case.execute(
        CreateRequestCommand(
            external_identifier="EXT-001",
            category="soporte técnico",
            requester_name="Ana Perez",
            requester_email="ana@example.com",
            description="No puedo entrar",
            priority="alta",
        )
    )

    assert result.id == 1
    assert result.external_identifier == "EXT-001"
    assert result.status == "recibida"
    assert result.created_at == clock.now_value


def test_create_request_use_case_rejects_duplicates() -> None:
    repository = FakeRequestRepository()
    clock = FakeClock(datetime(2026, 8, 2, 12, 0, tzinfo=timezone.utc))
    use_case = CreateRequestUseCase(repository=repository, clock=clock)
    repository.add(
        Solicitud(
            external_identifier="EXT-001",
            category=RequestCategory.TECH_SUPPORT,
            requester_name="Ana Perez",
            requester_email="ana@example.com",
            description="No puedo entrar",
            priority=RequestPriority.HIGH,
        )
    )

    with pytest.raises(RequestAlreadyExistsError):
        use_case.execute(
            CreateRequestCommand(
                external_identifier="EXT-001",
                category="soporte técnico",
                requester_name="Ana Perez",
                requester_email="ana@example.com",
                description="Duplicado",
                priority="alta",
            )
        )


def test_get_request_use_case_returns_request() -> None:
    repository = FakeRequestRepository()
    request = repository.add(
        Solicitud(
            external_identifier="EXT-002",
            category=RequestCategory.ADMINISTRATIVE,
            requester_name="Luis Gomez",
            requester_email="luis@example.com",
            description="Certificado",
            priority=RequestPriority.MEDIUM,
        )
    )
    use_case = GetRequestUseCase(repository=repository)

    result = use_case.execute(request.id or 1)

    assert result.id == request.id
    assert result.status == "recibida"


def test_get_request_use_case_raises_when_missing() -> None:
    use_case = GetRequestUseCase(repository=FakeRequestRepository())

    with pytest.raises(RequestNotFoundError):
        use_case.execute(999)


def test_update_request_status_use_case_updates_status() -> None:
    repository = FakeRequestRepository()
    request = repository.add(
        Solicitud(
            external_identifier="EXT-003",
            category=RequestCategory.ACADEMIC,
            requester_name="Maria Lopez",
            requester_email="maria@example.com",
            description="Inscripcion",
            priority=RequestPriority.LOW,
        )
    )
    use_case = UpdateRequestStatusUseCase(repository=repository)

    result = use_case.execute(UpdateRequestStatusCommand(request_id=request.id or 1, status="en proceso"))

    assert result.status == "en proceso"


def test_update_request_status_use_case_raises_when_missing() -> None:
    use_case = UpdateRequestStatusUseCase(repository=FakeRequestRepository())

    with pytest.raises(RequestNotFoundError):
        use_case.execute(UpdateRequestStatusCommand(request_id=999, status="en proceso"))
