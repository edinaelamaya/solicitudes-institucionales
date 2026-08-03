from fastapi import APIRouter, Depends, Query, status

from app.application.dto.request_dto import CreateRequestCommand, UpdateRequestStatusCommand
from app.application.use_cases.create_request import CreateRequestUseCase
from app.application.use_cases.get_request import GetRequestUseCase
from app.application.use_cases.get_requests import ListRequestsUseCase
from app.application.use_cases.update_request_status import UpdateRequestStatusUseCase
from app.interfaces.api.dependencies import (
    get_create_request_use_case,
    get_get_request_use_case,
    get_list_requests_use_case,
    get_update_request_status_use_case,
)
from app.interfaces.api.schemas.request import (
    RequestCreateSchema,
    RequestListResponseSchema,
    RequestResponseSchema,
    RequestStatusUpdateSchema,
)

router = APIRouter(prefix="/solicitudes", tags=["solicitudes"])


@router.post("", response_model=RequestResponseSchema, status_code=status.HTTP_201_CREATED)
def create_request(
    payload: RequestCreateSchema,
    use_case: CreateRequestUseCase = Depends(get_create_request_use_case),
) -> RequestResponseSchema:
    result = use_case.execute(
        CreateRequestCommand(
            external_identifier=payload.external_identifier,
            category=payload.category,
            requester_name=payload.requester_name,
            requester_email=str(payload.requester_email),
            description=payload.description,
            priority=payload.priority,
        )
    )
    return RequestResponseSchema.model_validate(result)


@router.get("", response_model=RequestListResponseSchema)
def list_requests(
    status_filter: str | None = Query(default=None, alias="status"),
    category: str | None = None,
    priority: str | None = None,
    use_case: ListRequestsUseCase = Depends(get_list_requests_use_case),
) -> RequestListResponseSchema:
    results = use_case.execute(status=status_filter, category=category, priority=priority)
    return RequestListResponseSchema(items=[RequestResponseSchema.model_validate(item) for item in results])


@router.get("/{request_id}", response_model=RequestResponseSchema)
def get_request(
    request_id: int,
    use_case: GetRequestUseCase = Depends(get_get_request_use_case),
) -> RequestResponseSchema:
    result = use_case.execute(request_id)
    return RequestResponseSchema.model_validate(result)


@router.patch("/{request_id}/estado", response_model=RequestResponseSchema)
def update_request_status(
    request_id: int,
    payload: RequestStatusUpdateSchema,
    use_case: UpdateRequestStatusUseCase = Depends(get_update_request_status_use_case),
) -> RequestResponseSchema:
    result = use_case.execute(UpdateRequestStatusCommand(request_id=request_id, status=payload.status))
    return RequestResponseSchema.model_validate(result)
