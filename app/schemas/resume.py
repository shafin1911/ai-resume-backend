from pydantic import BaseModel, EmailStr
from typing import Optional


# ✅ Base schema for all resumes
class ResumeBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    parsed_text: Optional[str] = None


# ✅ Schema for creating a resume
class ResumeCreate(ResumeBase):
    pass


# ✅ Schema for updating a resume (all fields optional)
class ResumeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    parsed_text: Optional[str] = None


# ✅ Schema for response (includes `id`)
class ResumeResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None  # Original experience
    improved_experience: Optional[str] = None  # ✅ New field
    parsed_text: Optional[str] = None


# ✅ Schema for improved ai resume response
class ResumeImprovementResponse(BaseModel):
    improved_experience: str  # Make sure this matches what AI returns
