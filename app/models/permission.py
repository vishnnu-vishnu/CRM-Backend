from sqlalchemy import (
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.session import Base


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    module: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    role_permissions = relationship(
        "RolePermission",
        back_populates="permission",
    )