from __future__ import annotations

from typing import Protocol

from app.domain.entities.request import Solicitud
from app.domain.value_objects.request_catalogs import RequestPriority, RequestStatus, RequestCategory


class RequestRepository(Protocol):
    def add(self, request: Solicitud) -> Solicitud:
        raise NotImplementedError

    def get_by_id(self, request_id: int) -> Solicitud | None:
        raise NotImplementedError

    def get_by_external_identifier(self, external_identifier: str) -> Solicitud | None:
        raise NotImplementedError

    def list(
        self,
        *,
        status: RequestStatus | None = None,
        category: RequestCategory | None = None,
        priority: RequestPriority | None = None,
    ) -> list[Solicitud]:
        raise NotImplementedError

    def update(self, request: Solicitud) -> Solicitud:
        raise NotImplementedError
