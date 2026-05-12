from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import create_user,list_users,get_user,delete_user,update_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)



#create user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
)
async def register_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_user(db, data)


# get all users

@router.get(
    "/",
    response_model=list[UserResponse],
)
async def get_all_users(
    db: AsyncSession = Depends(get_db),
):

    return await list_users(db)


# get single user

@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_single_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
):

    return await get_user(
        db,
        user_id,
    )





#delete user

@router.delete(
    "/{user_id}",
)
async def remove_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
):

    return await delete_user(
        db,
        user_id,
    )


# update user details


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
async def edit_user(
    user_id: str,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
):

    return await update_user(
        db,
        user_id,
        data,
    )