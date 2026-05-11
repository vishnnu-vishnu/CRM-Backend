import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User, UserStatus
from app.schemas.user import (
    UserCreate,
    UserResponse,
)


async def create_user(
    db: AsyncSession,
    data: UserCreate,
) -> UserResponse:

    result = await db.execute(
        select(User).where(User.email == data.email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    

    result = await db.execute(
        select(User).where(User.phone == data.phone)
    )
    

    existing_phone = result.scalar_one_or_none()

    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered",
        )

    user = User(
        # id=uuid.uuid4().int >> 64,
        name=data.name,
        email=data.email,
        phone=data.phone,
        password=get_password_hash(data.password),
        role_id=data.role_id,
        department_id=data.department_id,
        status=UserStatus.ACTIVE,
    )

    db.add(user)

    await db.flush()
    await db.refresh(user)

    return UserResponse.model_validate(user)