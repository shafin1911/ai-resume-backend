from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# ✅ User creation schema
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


# ✅ User response schema
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True  # Pydantic v2 compatibility


# ✅ User update schema (allows partial updates)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
