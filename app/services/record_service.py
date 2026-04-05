import math
from typing import Optional
from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.record import Record, RecordType, Category
from app.models.user import User
from app.schemas.record import RecordCreate, RecordUpdate
def create_record(data: RecordCreate, current_user: User, db: Session) -> Record:
    record = Record(
        user_id=current_user.id,
        amount=data.amount,
        type=RecordType(data.type),
        category=Category(data.category),
        date=data.date,
        description=data.description,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
def get_records(
    db: Session,
    record_type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    page: int = 1,
    limit: int = 20,
) -> dict:
    query = db.query(Record).filter(Record.is_deleted == False)
    if record_type:
        try:
            query = query.filter(Record.type == RecordType(record_type))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid type: {record_type}. Must be 'income' or 'expense'",
            )
    if category:
        try:
            query = query.filter(Record.category == Category(category))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid category: {category}",
            )
    if start_date:
        query = query.filter(Record.date >= start_date)
    if end_date:
        query = query.filter(Record.date <= end_date)
    total = query.count()
    pages = math.ceil(total / limit) if total > 0 else 1
    offset = (page - 1) * limit
    records = query.order_by(Record.date.desc()).offset(offset).limit(limit).all()
    return {
        "records": records,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages,
    }
def get_record_by_id(record_id: int, db: Session) -> Record:
    record = db.query(Record).filter(
        Record.id == record_id,
        Record.is_deleted == False,
    ).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record with id {record_id} not found",
        )
    return record
def update_record(record_id: int, data: RecordUpdate, db: Session) -> Record:
    record = get_record_by_id(record_id, db)
    if data.amount is not None:
        record.amount = data.amount
    if data.type is not None:
        record.type = RecordType(data.type)
    if data.category is not None:
        record.category = Category(data.category)
    if data.date is not None:
        record.date = data.date
    if data.description is not None:
        record.description = data.description
    db.commit()
    db.refresh(record)
    return record
def delete_record(record_id: int, db: Session) -> Record:
    record = get_record_by_id(record_id, db)
    record.is_deleted = True
    db.commit()
    db.refresh(record)
    return record