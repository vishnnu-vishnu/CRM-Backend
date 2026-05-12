from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    role_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    users = relationship(
        "User",
        back_populates="role",
    )
    role_permissions = relationship(
    "RolePermission",
    back_populates="role",
    )

    def __repr__(self):
        return f"<Role {self.role_name}>"