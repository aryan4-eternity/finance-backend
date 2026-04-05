from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.rbac import require_role
from app.models.user import User, UserRole
from app.schemas.user import UpdateRoleRequest, UpdateStatusRequest, UserListResponse, UserDetailResponse
from app.services import user_service
from app.utils.response import success_response
router = APIRouter(prefix="/api/users", tags=["User Management"])
@router.get(
    "/",
    response_model=dict,
    summary="List all users",
    description="Retrieve all users. Accessible only by admins.",
)
def list_users(
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    users = user_service.get_all_users(db)
    return success_response(
        data=[UserListResponse.model_validate(u).model_dump() for u in users],
        message=f"Found {len(users)} users",
    )
@router.get(
    "/{user_id}",
    response_model=dict,
    summary="Get user by ID",
    description="Retrieve a specific user's details. Accessible only by admins.",
)
def get_user(
    user_id: int,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    user = user_service.get_user_by_id(user_id, db)
    user_data = UserDetailResponse.model_validate(user).model_dump()
    if user.created_at:
        user_data["created_at"] = user.created_at.isoformat()
    if user.updated_at:
        user_data["updated_at"] = user.updated_at.isoformat()
    return success_response(data=user_data, message="User found")
@router.patch(
    "/{user_id}/role",
    response_model=dict,
    summary="Update user role",
    description="Change a user's role (viewer/analyst/admin). Accessible only by admins.",
)
def update_role(
    user_id: int,
    data: UpdateRoleRequest,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    user = user_service.update_user_role(user_id, data.role, db)
    return success_response(
        data=UserListResponse.model_validate(user).model_dump(),
        message=f"User role updated to '{data.role}'",
    )
@router.patch(
    "/{user_id}/status",
    response_model=dict,
    summary="Activate or deactivate user",
    description="Toggle user active status. Accessible only by admins.",
)
def update_status(
    user_id: int,
    data: UpdateStatusRequest,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    user = user_service.update_user_status(user_id, data.is_active, db)
    status_label = "activated" if data.is_active else "deactivated"
    return success_response(
        data=UserListResponse.model_validate(user).model_dump(),
        message=f"User {status_label} successfully",
    )