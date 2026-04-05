from pydantic import BaseModel, EmailStr, Field
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["john_doe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(..., min_length=6, max_length=100, examples=["strongpass123"])
class LoginRequest(BaseModel):
    username: str = Field(..., examples=["john_doe"])
    password: str = Field(..., examples=["strongpass123"])
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    class Config:
        from_attributes = True