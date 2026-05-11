from datetime import datetime

from pydantic import BaseModel, EmailStr


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