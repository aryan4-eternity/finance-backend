from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth import get_current_user
from app.middleware.rbac import require_role
from app.models.user import User, UserRole
from app.schemas.dashboard import (
    SummaryResponse,
    CategorySummaryResponse,
    TrendsResponse,
    RecentResponse,
)
from app.services import dashboard_service
router = APIRouter(prefix="/api/dashboard", tags=["Dashboard Analytics"])
@router.get(
    "/summary",
    response_model=SummaryResponse,
    summary="Get financial summary",
    description="Returns total income, total expenses, net balance, and record count. "
    "Accessible by all authenticated users.",
)
def get_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return dashboard_service.get_summary(db)
@router.get(
    "/category-summary",
    response_model=CategorySummaryResponse,
    summary="Get category-wise summary",
    description="Returns income and expense totals grouped by category. "
    "Accessible by analysts and admins.",
)
def get_category_summary(
    current_user: User = Depends(require_role(UserRole.ANALYST, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    return dashboard_service.get_category_summary(db)
@router.get(
    "/trends",
    response_model=TrendsResponse,
    summary="Get monthly trends",
    description="Returns monthly income, expense, and net balance trends. "
    "Accessible by analysts and admins.",
)
def get_trends(
    current_user: User = Depends(require_role(UserRole.ANALYST, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    return dashboard_service.get_trends(db)
@router.get(
    "/recent",
    response_model=RecentResponse,
    summary="Get recent transactions",
    description="Returns the 10 most recent financial records. "
    "Accessible by all authenticated users.",
)
def get_recent(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return dashboard_service.get_recent(db)