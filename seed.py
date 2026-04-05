import sys
import os
from datetime import date, datetime, timezone
sys.path.insert(0, os.path.dirname(__file__))
from app.database import engine, SessionLocal, Base
from app.models.user import User, UserRole
from app.models.record import Record, RecordType, Category
from app.middleware.auth import hash_password
def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            print("Database already seeded. Skipping.")
            return
        print("Seeding database...")
        users = [
            User(
                username="admin",
                email="admin@example.com",
                password_hash=hash_password("admin123"),
                role=UserRole.ADMIN,
                is_active=True,
            ),
            User(
                username="analyst",
                email="analyst@example.com",
                password_hash=hash_password("analyst123"),
                role=UserRole.ANALYST,
                is_active=True,
            ),
            User(
                username="viewer",
                email="viewer@example.com",
                password_hash=hash_password("viewer123"),
                role=UserRole.VIEWER,
                is_active=True,
            ),
        ]
        db.add_all(users)
        db.commit()
        print(f"  ✓ Created {len(users)} users")
        admin = db.query(User).filter(User.username == "admin").first()
        records = [
            Record(user_id=admin.id, amount=5000.00, type=RecordType.INCOME, category=Category.SALARY, date=date(2025, 1, 1), description="January salary"),
            Record(user_id=admin.id, amount=5000.00, type=RecordType.INCOME, category=Category.SALARY, date=date(2025, 2, 1), description="February salary"),
            Record(user_id=admin.id, amount=5000.00, type=RecordType.INCOME, category=Category.SALARY, date=date(2025, 3, 1), description="March salary"),
            Record(user_id=admin.id, amount=1200.00, type=RecordType.INCOME, category=Category.FREELANCE, date=date(2025, 1, 15), description="Web design project"),
            Record(user_id=admin.id, amount=800.00, type=RecordType.INCOME, category=Category.FREELANCE, date=date(2025, 2, 20), description="Logo design"),
            Record(user_id=admin.id, amount=500.00, type=RecordType.INCOME, category=Category.INVESTMENT, date=date(2025, 1, 10), description="Stock dividends"),
            Record(user_id=admin.id, amount=350.00, type=RecordType.INCOME, category=Category.INVESTMENT, date=date(2025, 3, 15), description="Mutual fund returns"),
            Record(user_id=admin.id, amount=1200.00, type=RecordType.EXPENSE, category=Category.UTILITIES, date=date(2025, 1, 5), description="Rent payment"),
            Record(user_id=admin.id, amount=1200.00, type=RecordType.EXPENSE, category=Category.UTILITIES, date=date(2025, 2, 5), description="Rent payment"),
            Record(user_id=admin.id, amount=1200.00, type=RecordType.EXPENSE, category=Category.UTILITIES, date=date(2025, 3, 5), description="Rent payment"),
            Record(user_id=admin.id, amount=450.00, type=RecordType.EXPENSE, category=Category.FOOD, date=date(2025, 1, 8), description="Monthly groceries"),
            Record(user_id=admin.id, amount=380.00, type=RecordType.EXPENSE, category=Category.FOOD, date=date(2025, 2, 8), description="Monthly groceries"),
            Record(user_id=admin.id, amount=420.00, type=RecordType.EXPENSE, category=Category.FOOD, date=date(2025, 3, 8), description="Monthly groceries"),
            Record(user_id=admin.id, amount=150.00, type=RecordType.EXPENSE, category=Category.TRANSPORT, date=date(2025, 1, 12), description="Monthly bus pass"),
            Record(user_id=admin.id, amount=150.00, type=RecordType.EXPENSE, category=Category.TRANSPORT, date=date(2025, 2, 12), description="Monthly bus pass"),
            Record(user_id=admin.id, amount=85.00, type=RecordType.EXPENSE, category=Category.ENTERTAINMENT, date=date(2025, 1, 20), description="Movie and dinner"),
            Record(user_id=admin.id, amount=120.00, type=RecordType.EXPENSE, category=Category.ENTERTAINMENT, date=date(2025, 2, 14), description="Concert tickets"),
            Record(user_id=admin.id, amount=200.00, type=RecordType.EXPENSE, category=Category.HEALTHCARE, date=date(2025, 1, 25), description="Doctor visit"),
            Record(user_id=admin.id, amount=300.00, type=RecordType.EXPENSE, category=Category.EDUCATION, date=date(2025, 2, 1), description="Online course subscription"),
            Record(user_id=admin.id, amount=75.00, type=RecordType.EXPENSE, category=Category.OTHER, date=date(2025, 3, 10), description="Miscellaneous supplies"),
            Record(user_id=admin.id, amount=2500.00, type=RecordType.INCOME, category=Category.FREELANCE, date=date(2025, 3, 20), description="Mobile app development"),
            Record(user_id=admin.id, amount=180.00, type=RecordType.EXPENSE, category=Category.TRANSPORT, date=date(2025, 3, 12), description="Uber rides"),
            Record(user_id=admin.id, amount=95.00, type=RecordType.EXPENSE, category=Category.ENTERTAINMENT, date=date(2025, 3, 25), description="Streaming subscriptions"),
            Record(user_id=admin.id, amount=150.00, type=RecordType.EXPENSE, category=Category.HEALTHCARE, date=date(2025, 3, 18), description="Pharmacy"),
            Record(user_id=admin.id, amount=1000.00, type=RecordType.INCOME, category=Category.OTHER, date=date(2025, 3, 28), description="Tax refund"),
        ]
        db.add_all(records)
        db.commit()
        print(f"  ✓ Created {len(records)} financial records")
        print("\nSeeding complete! 🎉")
        print("\nTest credentials:")
        print("  Admin:   admin / admin123")
        print("  Analyst: analyst / analyst123")
        print("  Viewer:  viewer / viewer123")
    finally:
        db.close()
if __name__ == "__main__":
    seed()