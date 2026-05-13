from pydantic import BaseModel
from typing import Optional


class PermissionCreate(BaseModel):
    module: str
    action: str
    description: Optional[str] = None


class PermissionUpdate(BaseModel):
    module: Optional[str] = None
    action: Optional[str] = None
    description: Optional[str] = None


class PermissionResponse(BaseModel):
    id: int
    module: str
    action: str
    code: str
    description: Optional[str] = None
    class Config:
        from_attributes = True