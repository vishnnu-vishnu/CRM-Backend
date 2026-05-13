from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.departments import Department

from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
)


#create a new department

async def create_department(
    db: AsyncSession,
    data: DepartmentCreate,
):

    result = await db.execute(
        select(Department).where(
            Department.name == data.name
        )
    )

    existing = result.scalar_one_or_none()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Department already exists",
        )

    department = Department(
        name=data.name,
        description=data.description,
    )

    db.add(department)

    await db.commit()

    await db.refresh(department)

    return DepartmentResponse.model_validate(
        department
    )


# list all departments

async def list_departments(
    db: AsyncSession,
):

    result = await db.execute(
        select(Department)
    )

    departments = result.scalars().all()

    return [
        DepartmentResponse.model_validate(
            department
        )
        for department in departments
    ]


# get department by id

async def get_department(
    db: AsyncSession,
    department_id: int,
):

    result = await db.execute(
        select(Department).where(
            Department.id == department_id
        )
    )

    department = result.scalar_one_or_none()

    if not department:

        raise HTTPException(
            status_code=404,
            detail="Department not found",
        )

    return DepartmentResponse.model_validate(
        department
    )


# update department

async def update_department(
    db: AsyncSession,
    department_id: int,
    data: DepartmentUpdate,
):

    result = await db.execute(
        select(Department).where(
            Department.id == department_id
        )
    )

    department = result.scalar_one_or_none()

    if not department:

        raise HTTPException(
            status_code=404,
            detail="Department not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():

        setattr(department, field, value)

    await db.commit()

    await db.refresh(department)

    return DepartmentResponse.model_validate(
        department
    )


# delete department

async def delete_department(
    db: AsyncSession,
    department_id: int,
):

    result = await db.execute(
        select(Department).where(
            Department.id == department_id
        )
    )

    department = result.scalar_one_or_none()

    if not department:

        raise HTTPException(
            status_code=404,
            detail="Department not found",
        )

    await db.delete(department)

    await db.commit()

    return {
        "message": "Department deleted successfully"
    }