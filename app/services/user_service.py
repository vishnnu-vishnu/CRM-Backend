import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User, UserStatus
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
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



async def list_users(
    db: AsyncSession,
):

    result = await db.execute(
        select(User)
    )

    users = result.scalars().all()

    return [
        UserResponse.model_validate(user)
        for user in users
    ]



async def get_user(
    db: AsyncSession,
    user_id: str,
):

    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    user = result.scalar_one_or_none()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserResponse.model_validate(user)




async def delete_user(
    db: AsyncSession,
    user_id: str,
):

    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    user = result.scalar_one_or_none()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await db.delete(user)

    await db.commit()

    return {
        "message": "User deleted successfully"
    }




# Update user details


async def update_user(
    db: AsyncSession,
    user_id: str,
    data: UserUpdate,
):

    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    user = result.scalar_one_or_none()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    

    if "email" in update_data:

        email_result = await db.execute(
            select(User).where(
                User.email == update_data["email"],
                User.id != user_id,
            )
        )

        existing_email = email_result.scalar_one_or_none()

        if existing_email:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )


    if "phone" in update_data:

        phone_result = await db.execute(
            select(User).where(
                User.phone == update_data["phone"],
                User.id != user_id,
            )
        )

        existing_phone = phone_result.scalar_one_or_none()

        if existing_phone:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone already exists",
            )

    

    if "password" in update_data:

        update_data["password"] = get_password_hash(
            update_data["password"]
        )


    for field, value in update_data.items():

        setattr(user, field, value)

    await db.commit()

    await db.refresh(user)

    return UserResponse.model_validate(user)


