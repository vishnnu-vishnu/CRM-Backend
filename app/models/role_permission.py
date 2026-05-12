from sqlalchemy import ForeignKey

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.session import Base


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
    )

    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id"),
        nullable=False,
    )

    role = relationship(
        "Role",
        back_populates="role_permissions",
    )

    permission = relationship(
        "Permission",
        back_populates="role_permissions",
    )