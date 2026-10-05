from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    class Config: from_attributes = True
