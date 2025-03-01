from pydantic import BaseModel
from typing import List, Optional
from app.schemas.resume import ResumeResponse


# ✅ Base Job Schema
class JobBase(BaseModel):
    title: str
    description: str


# ✅ Job Creation Schema
class JobCreate(BaseModel):
    title: str
    description: str
    user_id: int


# ✅ Job Response Schema (returns job + resumes linked to it)
class JobResponse(JobBase):
    id: int
    resumes: List[ResumeResponse] = []  # 🔹 Include linked resumes

    class Config:
        from_attributes = True  # ✅ SQLAlchemy conversion
