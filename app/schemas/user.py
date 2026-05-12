from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import UserStatus


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    role_id: int
    department_id: int


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    role_id: int
    department_id: int
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }




class UserUpdate(BaseModel):

    name: Optional[str] = None

    email: Optional[EmailStr] = None

    phone: Optional[str] = None

    password: Optional[str] = None

    role_id: Optional[int] = None

    department_id: Optional[int] = None

    status: Optional[UserStatus] = None