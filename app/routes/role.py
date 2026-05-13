from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
    RoleResponse,
)

from app.services.role_service import (
    create_role,
    list_roles,
    get_role,
    update_role,
    delete_role,
)

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


@router.post(
    "/",
    response_model=RoleResponse,
)
async def add_role(
    data: RoleCreate,
    db: AsyncSession = Depends(get_db),
):

    return await create_role(
        db,
        data,
    )


@router.get(
    "/",
    response_model=list[RoleResponse],
)
async def get_roles(
    db: AsyncSession = Depends(get_db),
):

    return await list_roles(db)


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
)
async def get_single_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
):

    return await get_role(
        db,
        role_id,
    )


@router.patch(
    "/{role_id}",
    response_model=RoleResponse,
)
async def edit_role(
    role_id: int,
    data: RoleUpdate,
    db: AsyncSession = Depends(get_db),
):

    return await update_role(
        db,
        role_id,
        data,
    )


@router.delete(
    "/{role_id}",
)
async def remove_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
):

    return await delete_role(
        db,
        role_id,
    )