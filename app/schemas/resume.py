from pydantic import BaseModel
from typing import Optional


class ResumeBase(BaseModel):
    experience: str
    improved_experience: Optional[str] = None
    summary_experience: Optional[str] = None
    job_id: Optional[int] = None
    parent_resume_id: Optional[int] = None


class ResumeCreate(ResumeBase):
    user_id: int


class ResumeUpdate(BaseModel):
    """✅ Allows partial updates"""

    experience: Optional[str] = None
    improved_experience: Optional[str] = None
    summary_experience: Optional[str] = None
    job_id: Optional[int] = None
    parent_resume_id: Optional[int] = None


class ResumeResponse(ResumeBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
