from app.infrastructure.database.base import Base
from app.infrastructure.database.models.request import RequestModel  # noqa: F401
from app.infrastructure.database.session import get_engine


def initialize_database() -> None:
    Base.metadata.create_all(bind=get_engine())
