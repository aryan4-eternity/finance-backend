from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth import get_current_user
from app.middleware.rbac import require_role
from app.models.user import User, UserRole
from app.schemas.record import RecordCreate, RecordUpdate, RecordResponse, PaginatedRecordsResponse
from app.services import record_service
from app.utils.response import success_response
router = APIRouter(prefix="/api/records", tags=["Financial Records"])
@router.post(
    "/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Create a financial record",
    description="Create a new income or expense record. Accessible only by admins.",
)
def create_record(
    data: RecordCreate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    record = record_service.create_record(data, current_user, db)
    return success_response(
        data=RecordResponse.model_validate(record).model_dump(mode="json"),
        message="Record created successfully",
    )
@router.get(
    "/",
    response_model=PaginatedRecordsResponse,
    summary="List financial records",
    description="Retrieve records with optional filtering by type, category, and date range. "
    "Supports pagination. Accessible by analysts and admins.",
)
def list_records(
    type: Optional[str] = Query(None, description="Filter by type: income or expense"),
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[date] = Query(None, description="Filter records from this date"),
    end_date: Optional[date] = Query(None, description="Filter records up to this date"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Records per page"),
    current_user: User = Depends(require_role(UserRole.ANALYST, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    result = record_service.get_records(
        db, record_type=type, category=category,
        start_date=start_date, end_date=end_date,
        page=page, limit=limit,
    )
    result["records"] = [
        RecordResponse.model_validate(r).model_dump(mode="json") for r in result["records"]
    ]
    return result
@router.get(
    "/{record_id}",
    response_model=dict,
    summary="Get a record by ID",
    description="Retrieve a specific financial record. Accessible by analysts and admins.",
)
def get_record(
    record_id: int,
    current_user: User = Depends(require_role(UserRole.ANALYST, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    record = record_service.get_record_by_id(record_id, db)
    return success_response(
        data=RecordResponse.model_validate(record).model_dump(mode="json"),
        message="Record found",
    )
@router.put(
    "/{record_id}",
    response_model=dict,
    summary="Update a financial record",
    description="Update an existing record's fields. Accessible only by admins.",
)
def update_record(
    record_id: int,
    data: RecordUpdate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    record = record_service.update_record(record_id, data, db)
    return success_response(
        data=RecordResponse.model_validate(record).model_dump(mode="json"),
        message="Record updated successfully",
    )
@router.delete(
    "/{record_id}",
    response_model=dict,
    summary="Delete a financial record (soft delete)",
    description="Soft-delete a record — marks it as deleted but retains data. Accessible only by admins.",
)
def delete_record(
    record_id: int,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    record_service.delete_record(record_id, db)
    return success_response(message="Record deleted successfully")