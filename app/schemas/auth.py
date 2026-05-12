from pydantic import (
    BaseModel,
    EmailStr,
)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserInfo(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    status: str


class RoleInfo(BaseModel):
    id: int
    role_name: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserInfo
    role: RoleInfo | None = None
    permissions: list[str] = []