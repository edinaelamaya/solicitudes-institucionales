from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RequestBaseSchema(BaseModel):
    external_identifier: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=60)
    requester_name: str = Field(min_length=1, max_length=150)
    requester_email: EmailStr
    description: str = Field(min_length=1)
    priority: str = Field(min_length=1, max_length=20)


class RequestCreateSchema(RequestBaseSchema):
    pass


class RequestStatusUpdateSchema(BaseModel):
    status: str = Field(min_length=1, max_length=20)


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
