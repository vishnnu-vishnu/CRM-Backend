from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.permission import (
    PermissionCreate,
    PermissionUpdate,
    PermissionResponse,
)

from app.services.permission_service import (
    create_permission,
    list_permissions,
    get_permission,
    update_permission,
    delete_permission,
)

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
)




@router.post(
    "/",
    response_model=PermissionResponse,
)
async def add_permission(
    data: PermissionCreate,
    db: AsyncSession = Depends(get_db),
):

    return await create_permission(
        db,
        data,
    )




@router.get(
    "/",
    response_model=list[PermissionResponse],
)
async def get_permissions(
    db: AsyncSession = Depends(get_db),
):

    return await list_permissions(db)




@router.get(
    "/{permission_id}",
    response_model=PermissionResponse,
)
async def get_single_permission(
    permission_id: int,
    db: AsyncSession = Depends(get_db),
):

    return await get_permission(
        db,
        permission_id,
    )




@router.patch(
    "/{permission_id}",
    response_model=PermissionResponse,
)
async def edit_permission(
    permission_id: int,
    data: PermissionUpdate,
    db: AsyncSession = Depends(get_db),
):

    return await update_permission(
        db,
        permission_id,
        data,
    )




@router.delete(
    "/{permission_id}",
)
async def remove_permission(
    permission_id: int,
    db: AsyncSession = Depends(get_db),
):

    return await delete_permission(
        db,
        permission_id,
    )