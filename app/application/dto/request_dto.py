from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class RequestSummary:
    id: int
    external_identifier: str
    category: str
    requester_name: str
    requester_email: str
    description: str
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class CreateRequestCommand:
    external_identifier: str
    category: str
    requester_name: str
    requester_email: str
    description: str
    priority: str


@dataclass(slots=True)
class UpdateRequestStatusCommand:
    request_id: int
    status: str
