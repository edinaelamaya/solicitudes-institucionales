from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.exceptions.request_exceptions import InvalidRequestStatusError
from app.domain.value_objects.request_catalogs import RequestCategory, RequestPriority, RequestStatus


@dataclass(slots=True)
class Solicitud:
    external_identifier: str
    category: RequestCategory
    requester_name: str
    requester_email: str
    description: str
    priority: RequestPriority
    status: RequestStatus = RequestStatus.RECEIVED
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id: int | None = None

    def change_status(self, new_status: RequestStatus) -> None:
        if new_status not in RequestStatus:
            raise InvalidRequestStatusError("invalid request status")
        self.status = new_status
        self.updated_at = datetime.now(timezone.utc)
