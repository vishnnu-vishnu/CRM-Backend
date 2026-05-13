from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission

from app.schemas.permission import (
    PermissionCreate,
    PermissionUpdate,
    PermissionResponse,
)


# create a new permission

async def create_permission(
    db: AsyncSession,
    data: PermissionCreate,
):

    permission_code = (
        f"{data.module}:{data.action}"
    )

    result = await db.execute(
        select(Permission).where(
            Permission.code == permission_code
        )
    )

    existing = result.scalar_one_or_none()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Permission already exists",
        )

    permission = Permission(

        module=data.module,

        action=data.action,

        code=permission_code,

        description=data.description,
    )

    db.add(permission)

    await db.commit()

    await db.refresh(permission)

    return PermissionResponse.model_validate(
        permission
    )


# list all permissions

async def list_permissions(
    db: AsyncSession,
):

    result = await db.execute(
        select(Permission)
    )

    permissions = result.scalars().all()

    return [
        PermissionResponse.model_validate(
            permission
        )
        for permission in permissions
    ]


#get permission by id

async def get_permission(
    db: AsyncSession,
    permission_id: int,
):

    result = await db.execute(
        select(Permission).where(
            Permission.id == permission_id
        )
    )

    permission = result.scalar_one_or_none()

    if not permission:

        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )

    return PermissionResponse.model_validate(
        permission
    )


# update permission

async def update_permission(
    db: AsyncSession,
    permission_id: int,
    data: PermissionUpdate,
):

    result = await db.execute(
        select(Permission).where(
            Permission.id == permission_id
        )
    )

    permission = result.scalar_one_or_none()

    if not permission:

        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    # Update fields
    for field, value in update_data.items():

        setattr(permission, field, value)

    # Regenerate permission code
    permission.code = (
        f"{permission.module}:{permission.action}"
    )

    await db.commit()

    await db.refresh(permission)

    return PermissionResponse.model_validate(
        permission
    )



# delete permission


async def delete_permission(
    db: AsyncSession,
    permission_id: int,
):

    result = await db.execute(
        select(Permission).where(
            Permission.id == permission_id
        )
    )

    permission = result.scalar_one_or_none()

    if not permission:

        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )

    await db.delete(permission)

    await db.commit()

    return {
        "message": "Permission deleted successfully"
    }