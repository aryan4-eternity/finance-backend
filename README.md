# Finance Dashboard API

A backend API for a finance dashboard system with role-based access control, financial records management, and analytics.

Built with **Python**, **FastAPI**, **SQLAlchemy**, and **SQLite**.

---

## Features

- **JWT Authentication** — Register, login, token-based access
- **Role-Based Access Control** — Viewer, Analyst, Admin with granular permissions
- **Financial Records CRUD** — Create, read, update, soft-delete with filtering & pagination
- **Dashboard Analytics** — Summary stats, category breakdowns, monthly trends, recent activity
- **Input Validation** — Pydantic schemas with proper error responses
- **Automated Tests** — pytest test suite with 40+ test cases
- **Interactive API Docs** — Auto-generated Swagger UI at `/docs`

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite |
| Auth | JWT (python-jose) + bcrypt |
| Validation | Pydantic |
| Testing | pytest + TestClient |
| Docs | Swagger UI (built-in) |

---

## Project Structure

```
finance-backend/
├── app/
│   ├── config.py          # Environment configuration
│   ├── database.py        # SQLAlchemy setup, session management
│   ├── main.py            # FastAPI app, router registration, error handling
│   ├── models/            # SQLAlchemy ORM models
│   │   ├── user.py        # User model with role enum
│   │   └── record.py      # Financial record model with type/category enums
│   ├── schemas/           # Pydantic request/response schemas
│   │   ├── auth.py        # Register, login, token schemas
│   │   ├── user.py        # User management schemas
│   │   ├── record.py      # Record CRUD + pagination schemas
│   │   └── dashboard.py   # Analytics response schemas
│   ├── routers/           # API route handlers
│   │   ├── auth.py        # /api/auth/* endpoints
│   │   ├── users.py       # /api/users/* endpoints
│   │   ├── records.py     # /api/records/* endpoints
│   │   └── dashboard.py   # /api/dashboard/* endpoints
│   ├── services/          # Business logic layer
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── record_service.py
│   │   └── dashboard_service.py
│   ├── middleware/         # Authentication & RBAC
│   │   ├── auth.py        # JWT verification, password hashing
│   │   └── rbac.py        # Role-based access control dependency
│   └── utils/
│       └── response.py    # Standardized response helpers
├── tests/                 # Test suite
│   ├── conftest.py        # Fixtures, test DB setup
│   ├── test_auth.py       # Auth endpoint tests
│   ├── test_users.py      # User management tests
│   ├── test_records.py    # Record CRUD tests
│   └── test_dashboard.py  # Dashboard analytics tests
├── seed.py                # Database seeder
├── server.py              # Server entry point
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
└── README.md
```

---

## Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd finance-backend

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Copy the example env file:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `dev-secret-key-not-for-production` | JWT signing key |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Token expiry (minutes) |
| `DATABASE_URL` | `sqlite:///./finance.db` | Database connection string |

### Seed the Database

```bash
python seed.py
```

This creates 3 test users and 25 sample financial records.

### Run the Server

```bash
python server.py
# or
uvicorn app.main:app --reload
```

Server starts at **http://localhost:8000**

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## API Reference

### Authentication

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/api/auth/register` | Public | Register new user (defaults to viewer) |
| POST | `/api/auth/login` | Public | Login and get JWT token |
| GET | `/api/auth/me` | Authenticated | Get current user profile |

### User Management

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | `/api/users/` | Admin | List all users |
| GET | `/api/users/{id}` | Admin | Get user by ID |
| PATCH | `/api/users/{id}/role` | Admin | Update user role |
| PATCH | `/api/users/{id}/status` | Admin | Activate/deactivate user |

### Financial Records

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/api/records/` | Admin | Create new record |
| GET | `/api/records/` | Analyst, Admin | List records (with filters) |
| GET | `/api/records/{id}` | Analyst, Admin | Get single record |
| PUT | `/api/records/{id}` | Admin | Update record |
| DELETE | `/api/records/{id}` | Admin | Soft-delete record |

**Query Parameters** for `GET /api/records/`:
- `type` — Filter by `income` or `expense`
- `category` — Filter by category (salary, food, etc.)
- `start_date` — Filter from date (YYYY-MM-DD)
- `end_date` — Filter to date (YYYY-MM-DD)
- `page` — Page number (default: 1)
- `limit` — Records per page (default: 20, max: 100)

### Dashboard Analytics

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | `/api/dashboard/summary` | All roles | Total income, expenses, net balance |
| GET | `/api/dashboard/category-summary` | Analyst, Admin | Category-wise totals |
| GET | `/api/dashboard/trends` | Analyst, Admin | Monthly income/expense trends |
| GET | `/api/dashboard/recent` | All roles | Last 10 transactions |

---

## Access Control Matrix

| Action | Viewer | Analyst | Admin |
|--------|--------|---------|-------|
| View dashboard summary | ✅ | ✅ | ✅ |
| View recent activity | ✅ | ✅ | ✅ |
| View records list | ❌ | ✅ | ✅ |
| View category/trend analytics | ❌ | ✅ | ✅ |
| Create/update/delete records | ❌ | ❌ | ✅ |
| Manage users | ❌ | ❌ | ✅ |

---

## Test Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Analyst | `analyst` | `analyst123` |
| Viewer | `viewer` | `viewer123` |

---

## Running Tests

```bash
pytest -v
```

The test suite includes 40+ tests covering:
- Authentication (register, login, token validation)
- User management (CRUD, role updates, RBAC enforcement)
- Financial records (CRUD, filtering, pagination, soft delete)
- Dashboard analytics (summary accuracy, role restrictions)

---

## Architecture Decisions

1. **Layered Architecture**: Routes → Services → Models. Routes handle HTTP concerns, services contain business logic, models define data access. This separation makes the code testable and maintainable.

2. **FastAPI Dependency Injection for RBAC**: Using `Depends()` for authentication and role checks. This is declarative, composable, and built into the framework — no custom middleware needed.

3. **SQLite with SQLAlchemy ORM**: Zero-config database suitable for assessment scope. SQLAlchemy provides abstraction that would make switching to PostgreSQL trivial in production.

4. **Soft Delete**: Records are marked `is_deleted=True` rather than physically removed. This preserves data integrity and audit trails.

5. **Pydantic Validation**: All input validation is handled by Pydantic schemas with regex patterns, min/max constraints, and type checking. FastAPI automatically returns 422 with detailed errors for invalid input.

6. **Standardized Response Format**: All endpoints return `{ success, message, data }` for consistency.

---

## Assumptions

- New users register with the `viewer` role by default. Only admins can promote users.
- Financial records are created by admins and are globally visible to authorized roles (not scoped per-user for this dashboard use case).
- The last admin cannot be demoted or deactivated (safety guard).
- Inactive users cannot log in or access any endpoints.
- Soft-deleted records are excluded from all queries and analytics.
- Categories are predefined (enum) for data consistency.

---

## Possible Improvements (Not Implemented)

- Rate limiting with `slowapi`
- Audit logging for sensitive operations
- Refresh tokens for session management
- User-scoped record visibility
- Export to CSV/PDF
- WebSocket real-time notifications
- Docker containerization
