from sqlalchemy.orm import Session
from sqlalchemy import func, case, String
from app.models.record import Record, RecordType
def get_summary(db: Session) -> dict:
    result = db.query(
        func.coalesce(
            func.sum(case((Record.type == RecordType.INCOME, Record.amount), else_=0)), 0
        ).label("total_income"),
        func.coalesce(
            func.sum(case((Record.type == RecordType.EXPENSE, Record.amount), else_=0)), 0
        ).label("total_expenses"),
        func.count(Record.id).label("total_records"),
    ).filter(Record.is_deleted == False).first()
    total_income = float(result.total_income)
    total_expenses = float(result.total_expenses)
    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_balance": round(total_income - total_expenses, 2),
        "total_records": result.total_records,
    }
def get_category_summary(db: Session) -> dict:
    results = db.query(
        Record.category,
        func.coalesce(
            func.sum(case((Record.type == RecordType.INCOME, Record.amount), else_=0)), 0
        ).label("total_income"),
        func.coalesce(
            func.sum(case((Record.type == RecordType.EXPENSE, Record.amount), else_=0)), 0
        ).label("total_expense"),
    ).filter(Record.is_deleted == False).group_by(Record.category).all()
    categories = []
    for row in results:
        income = float(row.total_income)
        expense = float(row.total_expense)
        categories.append({
            "category": row.category.value if hasattr(row.category, "value") else str(row.category),
            "total_income": round(income, 2),
            "total_expense": round(expense, 2),
            "net": round(income - expense, 2),
        })
    return {"categories": categories}
def get_trends(db: Session) -> dict:
    month_label = func.strftime("%Y-%m", Record.date).label("month")
    results = db.query(
        month_label,
        func.coalesce(
            func.sum(case((Record.type == RecordType.INCOME, Record.amount), else_=0)), 0
        ).label("income"),
        func.coalesce(
            func.sum(case((Record.type == RecordType.EXPENSE, Record.amount), else_=0)), 0
        ).label("expense"),
    ).filter(Record.is_deleted == False).group_by(month_label).order_by(month_label).all()
    trends = []
    for row in results:
        income = float(row.income)
        expense = float(row.expense)
        trends.append({
            "month": row.month,
            "income": round(income, 2),
            "expense": round(expense, 2),
            "net": round(income - expense, 2),
        })
    return {"trends": trends}
def get_recent(db: Session, limit: int = 10) -> dict:
    records = (
        db.query(Record)
        .filter(Record.is_deleted == False)
        .order_by(Record.date.desc(), Record.created_at.desc())
        .limit(limit)
        .all()
    )
    return {
        "records": [
            {
                "id": r.id,
                "amount": r.amount,
                "type": r.type.value,
                "category": r.category.value,
                "date": str(r.date),
                "description": r.description,
            }
            for r in records
        ]
    }