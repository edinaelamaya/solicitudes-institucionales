from app.domain.entities.request import Solicitud
from app.domain.value_objects.request_catalogs import RequestCategory, RequestPriority, RequestStatus
from app.infrastructure.database.models.request import RequestModel


def to_domain(model: RequestModel) -> Solicitud:
    return Solicitud(
        id=model.id,
        external_identifier=model.external_identifier,
        category=RequestCategory(model.category),
        requester_name=model.requester_name,
        requester_email=model.requester_email,
        description=model.description,
        priority=RequestPriority(model.priority),
        status=RequestStatus(model.status),
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def to_model(entity: Solicitud) -> RequestModel:
    return RequestModel(
        id=entity.id,
        external_identifier=entity.external_identifier,
        category=entity.category.value,
        requester_name=entity.requester_name,
        requester_email=entity.requester_email,
        description=entity.description,
        priority=entity.priority.value,
        status=entity.status.value,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
