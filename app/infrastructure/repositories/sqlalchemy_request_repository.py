from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.domain.entities.request import Solicitud
from app.domain.exceptions.request_exceptions import DuplicateExternalIdentifierError
from app.domain.repositories.request_repository import RequestRepository
from app.domain.value_objects.request_catalogs import RequestCategory, RequestPriority, RequestStatus
from app.infrastructure.database.mappers import to_domain, to_model
from app.infrastructure.database.models.request import RequestModel
from app.infrastructure.database.session import get_session_factory


class SQLAlchemyRequestRepository(RequestRepository):
    def __init__(self) -> None:
        self._session_factory = get_session_factory()

    def add(self, request: Solicitud) -> Solicitud:
        session = self._session_factory()
        try:
            model = to_model(request)
            session.add(model)
            session.commit()
            session.refresh(model)
            return to_domain(model)
        except IntegrityError as exc:
            session.rollback()
            raise DuplicateExternalIdentifierError("duplicate external identifier") from exc
        finally:
            session.close()

    def get_by_id(self, request_id: int) -> Solicitud | None:
        session = self._session_factory()
        try:
            model = session.get(RequestModel, request_id)
            return to_domain(model) if model is not None else None
        finally:
            session.close()

    def get_by_external_identifier(self, external_identifier: str) -> Solicitud | None:
        session = self._session_factory()
        try:
            statement = select(RequestModel).where(RequestModel.external_identifier == external_identifier)
            model = session.execute(statement).scalar_one_or_none()
            return to_domain(model) if model is not None else None
        finally:
            session.close()

    def list(
        self,
        *,
        status: RequestStatus | None = None,
        category: RequestCategory | None = None,
        priority: RequestPriority | None = None,
    ) -> list[Solicitud]:
        session = self._session_factory()
        try:
            statement = select(RequestModel)
            if status is not None:
                statement = statement.where(RequestModel.status == status.value)
            if category is not None:
                statement = statement.where(RequestModel.category == category.value)
            if priority is not None:
                statement = statement.where(RequestModel.priority == priority.value)
            models = session.execute(statement.order_by(RequestModel.created_at.desc())).scalars().all()
            return [to_domain(model) for model in models]
        finally:
            session.close()

    def update(self, request: Solicitud) -> Solicitud:
        session = self._session_factory()
        try:
            model = session.get(RequestModel, request.id)
            if model is None:
                return request
            model.external_identifier = request.external_identifier
            model.category = request.category.value
            model.requester_name = request.requester_name
            model.requester_email = request.requester_email
            model.description = request.description
            model.priority = request.priority.value
            model.status = request.status.value
            model.created_at = request.created_at
            model.updated_at = request.updated_at
            session.commit()
            session.refresh(model)
            return to_domain(model)
        finally:
            session.close()
