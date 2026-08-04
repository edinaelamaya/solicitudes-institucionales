from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import pytest

from app.application.dto.request_dto import RequestSummary
from app.application.exceptions.request_exceptions import RequestAlreadyExistsError, RequestNotFoundError
from app.interfaces.api.dependencies import (
    get_create_request_use_case,
    get_get_request_use_case,
    get_list_requests_use_case,
    get_update_request_status_use_case,
)


@dataclass
class FakeCreateUseCase:
    result: RequestSummary | None = None
    error: Exception | None = None

    def execute(self, command):
        if self.error is not None:
            raise self.error
        assert command.external_identifier
        return self.result


@dataclass
class FakeGetUseCase:
    result: RequestSummary | None = None
    error: Exception | None = None

    def execute(self, request_id: int):
        if self.error is not None:
            raise self.error
        assert request_id > 0
        return self.result


@dataclass
class FakeListUseCase:
    result: list[RequestSummary] | None = None

    def execute(self, **kwargs):
        return self.result or []


@dataclass
class FakeUpdateUseCase:
    result: RequestSummary | None = None

    def execute(self, command):
        assert command.request_id > 0
        return self.result


def _summary(request_id: int = 1, status: str = "recibida") -> RequestSummary:
    return RequestSummary(
        id=request_id,
        external_identifier="EXT-001",
        category="soporte técnico",
        requester_name="Ana Perez",
        requester_email="ana@example.com",
        description="No puedo entrar",
        priority="alta",
        status=status,
        created_at=datetime(2026, 8, 2, 12, 0, tzinfo=timezone.utc),
        updated_at=datetime(2026, 8, 2, 12, 0, tzinfo=timezone.utc),
    )


def test_create_request_endpoint_returns_created(api_client, monkeypatch) -> None:
    fake_use_case = FakeCreateUseCase(result=_summary())
    api_client.app.dependency_overrides[get_create_request_use_case] = lambda: fake_use_case

    response = api_client.post(
        "/api/v1/solicitudes",
        json={
            "external_identifier": "EXT-001",
            "category": "soporte técnico",
            "requester_name": "Ana Perez",
            "requester_email": "ana@example.com",
            "description": "No puedo entrar",
            "priority": "alta",
        },
    )

    assert response.status_code == 201
    assert response.json()["external_identifier"] == "EXT-001"


def test_create_request_endpoint_rejects_invalid_email(api_client) -> None:
    response = api_client.post(
        "/api/v1/solicitudes",
        json={
            "external_identifier": "EXT-001",
            "category": "soporte técnico",
            "requester_name": "Ana Perez",
            "requester_email": "not-an-email",
            "description": "No puedo entrar",
            "priority": "alta",
        },
    )

    assert response.status_code == 422


def test_create_request_endpoint_rejects_duplicates(api_client) -> None:
    fake_use_case = FakeCreateUseCase(error=RequestAlreadyExistsError("request already exists"))
    api_client.app.dependency_overrides[get_create_request_use_case] = lambda: fake_use_case

    response = api_client.post(
        "/api/v1/solicitudes",
        json={
            "external_identifier": "EXT-001",
            "category": "soporte técnico",
            "requester_name": "Ana Perez",
            "requester_email": "ana@example.com",
            "description": "Duplicado",
            "priority": "alta",
        },
    )

    assert response.status_code == 409


def test_list_requests_endpoint_returns_items(api_client) -> None:
    fake_use_case = FakeListUseCase(result=[_summary()])
    api_client.app.dependency_overrides[get_list_requests_use_case] = lambda: fake_use_case

    response = api_client.get("/api/v1/solicitudes")

    assert response.status_code == 200
    assert len(response.json()["items"]) == 1


def test_get_request_endpoint_returns_existing_request(api_client) -> None:
    fake_use_case = FakeGetUseCase(result=_summary())
    api_client.app.dependency_overrides[get_get_request_use_case] = lambda: fake_use_case

    response = api_client.get("/api/v1/solicitudes/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_request_endpoint_returns_not_found(api_client) -> None:
    fake_use_case = FakeGetUseCase(error=RequestNotFoundError("request not found"))
    api_client.app.dependency_overrides[get_get_request_use_case] = lambda: fake_use_case

    response = api_client.get("/api/v1/solicitudes/999")

    assert response.status_code == 404


def test_update_request_status_endpoint_returns_updated_request(api_client) -> None:
    fake_use_case = FakeUpdateUseCase(result=_summary(status="en proceso"))
    api_client.app.dependency_overrides[get_update_request_status_use_case] = lambda: fake_use_case

    response = api_client.patch(
        "/api/v1/solicitudes/1/estado",
        json={"status": "en proceso"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "en proceso"
