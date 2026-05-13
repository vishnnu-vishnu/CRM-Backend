from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role

from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
    RoleResponse,
)


# Create a new role

async def create_role(
    db: AsyncSession,
    data: RoleCreate,
):

    result = await db.execute(
        select(Role).where(
            Role.role_name == data.role_name
        )
    )

    existing = result.scalar_one_or_none()

    if existing:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already exists",
        )

    role = Role(
        role_name=data.role_name,
        description=data.description,
    )

    db.add(role)

    await db.commit()

    await db.refresh(role)

    return RoleResponse.model_validate(role)


# get list of all roles

async def list_roles(
    db: AsyncSession,
):

    result = await db.execute(
        select(Role)
    )

    roles = result.scalars().all()

    return [
        RoleResponse.model_validate(role)
        for role in roles
    ]


#get role by id

async def get_role(
    db: AsyncSession,
    role_id: int,
):

    result = await db.execute(
        select(Role).where(
            Role.id == role_id
        )
    )

    role = result.scalar_one_or_none()

    if not role:

        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )

    return RoleResponse.model_validate(role)


# update role

async def update_role(
    db: AsyncSession,
    role_id: int,
    data: RoleUpdate,
):

    result = await db.execute(
        select(Role).where(
            Role.id == role_id
        )
    )

    role = result.scalar_one_or_none()

    if not role:

        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():

        setattr(role, field, value)

    await db.commit()

    await db.refresh(role)

    return RoleResponse.model_validate(role)


# delete role


async def delete_role(
    db: AsyncSession,
    role_id: int,
):

    result = await db.execute(
        select(Role).where(
            Role.id == role_id
        )
    )

    role = result.scalar_one_or_none()

    if not role:

        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )

    await db.delete(role)

    await db.commit()

    return {
        "message": "Role deleted successfully"
    }