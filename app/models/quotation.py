from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    Text,
    ForeignKey,
    DateTime,
    DECIMAL,
    Enum as SqlEnum,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.session import Base


class QuotationStatus(str, Enum):
    DRAFT = "Draft"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    CONFIRMED = "Confirmed"


class Quotation(Base):
    __tablename__ = "quotations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    enquiry_id: Mapped[int] = mapped_column(
        ForeignKey("enquiries.id"),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[QuotationStatus] = mapped_column(
        SqlEnum(QuotationStatus),
        default=QuotationStatus.DRAFT,
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    approved_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    enquiry = relationship(
        "Enquiry",
        back_populates="quotations",
    )

    projects = relationship(
        "Project",
        back_populates="quotation",
    )