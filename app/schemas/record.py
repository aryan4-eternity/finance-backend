import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
class RecordCreate(BaseModel):
    amount: float = Field(..., gt=0, examples=[1500.00])
    type: str = Field(..., pattern="^(income|expense)$", examples=["income"])
    category: str = Field(
        ...,
        pattern="^(salary|freelance|investment|food|transport|utilities|entertainment|healthcare|education|other)$",
        examples=["salary"],
    )
    date: datetime.date = Field(..., examples=["2025-01-15"])
    description: Optional[str] = Field(None, max_length=500, examples=["Monthly salary"])
class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0, examples=[2000.00])
    type: Optional[str] = Field(None, pattern="^(income|expense)$", examples=["income"])
    category: Optional[str] = Field(
        None,
        pattern="^(salary|freelance|investment|food|transport|utilities|entertainment|healthcare|education|other)$",
        examples=["salary"],
    )
    date: Optional[datetime.date] = Field(None, examples=["2025-01-15"])
    description: Optional[str] = Field(None, max_length=500, examples=["Updated description"])
class RecordResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    type: str
    category: str
    date: datetime.date
    description: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    class Config:
        from_attributes = True
class PaginatedRecordsResponse(BaseModel):
    records: List[RecordResponse]
    total: int
    page: int
    limit: int
    pages: int