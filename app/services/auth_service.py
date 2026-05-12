from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission

from app.core.security import verify_password


from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
)

from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    UserInfo,
    RoleInfo,
)

async def authenticate_user(
    db: AsyncSession,
    request: LoginRequest,
) -> TokenResponse:

    result = await db.execute(
        select(User).where(
            User.email == request.email
        )
    )

    user = result.scalar_one_or_none()

    

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


    if not verify_password(
        request.password,
        user.password,
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    
    if user.status.value != "Active":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account inactive",
        )

    

    role_result = await db.execute(
        select(Role).where(
            Role.id == user.role_id
        )
    )

    role = role_result.scalar_one_or_none()

    

    permission_result = await db.execute(

        select(Permission.code)

        .join(
            RolePermission,
            RolePermission.permission_id == Permission.id
        )

        .where(
            RolePermission.role_id == role.id
        )
    )

    permissions = [
        row[0]
        for row in permission_result.all()
    ]

    token_data = {

        "user_id": user.id,

        "email": user.email,

        "role_id": role.id if role else None,

        "role": role.role_name if role else None,

        "permissions": permissions,
    }


    access_token = create_access_token(
        token_data
    )

    refresh_token = create_refresh_token(
        token_data
    )

    return TokenResponse(

        access_token=access_token,

        refresh_token=refresh_token,

        token_type="bearer",

        user=UserInfo(

            id=user.id,

            name=user.name,

            email=user.email,

            phone=user.phone,

            status=user.status.value,
        ),

        role=(
            RoleInfo(
                id=role.id,
                role_name=role.role_name,
            )
            if role else None
        ),

        permissions=permissions,
    )