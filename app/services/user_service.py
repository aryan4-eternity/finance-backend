from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()
def get_user_by_id(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user
def update_user_role(user_id: int, new_role: str, db: Session) -> User:
    user = get_user_by_id(user_id, db)
    try:
        role_enum = UserRole(new_role)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role: {new_role}. Must be one of: viewer, analyst, admin",
        )
    if user.role == UserRole.ADMIN and role_enum != UserRole.ADMIN:
        admin_count = db.query(User).filter(User.role == UserRole.ADMIN).count()
        if admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot change role of the last admin user",
            )
    user.role = role_enum
    db.commit()
    db.refresh(user)
    return user
def update_user_status(user_id: int, is_active: bool, db: Session) -> User:
    user = get_user_by_id(user_id, db)
    if not is_active and user.role == UserRole.ADMIN:
        active_admin_count = (
            db.query(User)
            .filter(User.role == UserRole.ADMIN, User.is_active == True)
            .count()
        )
        if active_admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot deactivate the last active admin user",
            )
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user