from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.auth import RegisterRequest, TokenResponse, UserResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.services import auth_service
from app.utils.response import success_response
router = APIRouter(prefix="/api/auth", tags=["Authentication"])
@router.post(
    "/register",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new user account with the default role of 'viewer'.",
)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user = auth_service.register_user(data, db)
    return success_response(
        data=UserResponse.model_validate(user).model_dump(),
        message="User registered successfully",
    )
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and get access token",
    description="Authenticate with username and password. Returns a JWT access token.",
)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_service.login_user(data, db)
@router.get(
    "/me",
    response_model=dict,
    summary="Get current user profile",
    description="Returns the profile of the currently authenticated user.",
)
def get_me(current_user: User = Depends(get_current_user)):
    return success_response(
        data=UserResponse.model_validate(current_user).model_dump(),
        message="Current user profile",
    )