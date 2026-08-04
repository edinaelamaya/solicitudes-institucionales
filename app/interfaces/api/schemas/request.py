from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domain.value_objects.request_catalogs import RequestCategory, RequestPriority, RequestStatus


class RequestBaseSchema(BaseModel):
    external_identifier: str = Field(min_length=1, max_length=100)
    category: RequestCategory
    requester_name: str = Field(min_length=1, max_length=150)
    requester_email: EmailStr
    description: str = Field(min_length=1)
    priority: RequestPriority


class RequestCreateSchema(RequestBaseSchema):
    pass


class RequestStatusUpdateSchema(BaseModel):
    status: RequestStatus


class RequestResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_identifier: str
    category: str
    requester_name: str
    requester_email: EmailStr
    description: str
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime


class RequestListResponseSchema(BaseModel):
    items: list[RequestResponseSchema]
