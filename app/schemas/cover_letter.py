from pydantic import BaseModel


# ✅ Generate a cover letter response
class CoverLetterResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    resume_id: int  # 🔹 Add reference to resume
    content: str
