from pydantic import BaseModel


# ✅ Schema for Resume-Job Match Response
class ResumeJobMatchResponse(BaseModel):
    resume_id: int
    job_id: int
    match_percentage: float
