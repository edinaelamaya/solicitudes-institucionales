from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class RequestModel(Base):
    __tablename__ = "requests"
    __table_args__ = (
        UniqueConstraint("external_identifier", name="uq_requests_external_identifier"),
        Index("ix_requests_status", "status"),
        Index("ix_requests_category", "category"),
        Index("ix_requests_priority", "priority"),
        Index("ix_requests_external_identifier", "external_identifier"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_identifier: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(60), nullable=False)
    requester_name: Mapped[str] = mapped_column(String(150), nullable=False)
    requester_email: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="recibida")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
