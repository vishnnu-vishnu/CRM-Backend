from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
)

from app.services.department_service import (
    create_department,
    list_departments,
    get_department,
    update_department,
    delete_department,
)

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)


@router.post(
    "/",
    response_model=DepartmentResponse,
)
async def add_department(
    data: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
):

    return await create_department(
        db,
        data,
    )


@router.get(
    "/",
    response_model=list[DepartmentResponse],
)
async def get_departments(
    db: AsyncSession = Depends(get_db),
):

    return await list_departments(db)


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
)
async def get_single_department(
    department_id: int,
    db: AsyncSession = Depends(get_db),
):

    return await get_department(
        db,
        department_id,
    )


@router.patch(
    "/{department_id}",
    response_model=DepartmentResponse,
)
async def edit_department(
    department_id: int,
    data: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
):

    return await update_department(
        db,
        department_id,
        data,
    )


@router.delete(
    "/{department_id}",
)
async def remove_department(
    department_id: int,
    db: AsyncSession = Depends(get_db),
):

    return await delete_department(
        db,
        department_id,
    )