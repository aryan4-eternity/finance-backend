from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import init_db
from app.routers import auth, users, records, dashboard
app = FastAPI(
    title="Finance Dashboard API",
    description=(
        "A backend API for a finance dashboard system with role-based access control, "
        "financial records management, and analytics. Built with FastAPI, SQLAlchemy, and SQLite."
    ),
    version="1.0.0",
    docs_url="/docs",                   
    redoc_url="/redoc",            
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                                          
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)
@app.on_event("startup")
def on_startup():
    init_db()
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An unexpected error occurred",
            "detail": str(exc),
        },
    )
@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "message": "Finance Dashboard API is running",
        "docs": "/docs",
    }