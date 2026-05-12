from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
)

from app.services.auth_service import (
    authenticate_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):

    return await authenticate_user(
        db,
        request,
    )