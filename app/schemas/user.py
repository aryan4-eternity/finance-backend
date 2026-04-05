from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
class UpdateRoleRequest(BaseModel):
    role: str = Field(..., pattern="^(viewer|analyst|admin)$", examples=["analyst"])
class UpdateStatusRequest(BaseModel):
    is_active: bool = Field(..., examples=[True])
class UserListResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    class Config:
        from_attributes = True
class UserDetailResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True