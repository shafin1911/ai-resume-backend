from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.job import Job  # ✅ Import Job
from app.models.resume import Resume
from app.models.cover_letter import CoverLetter
from app.schemas.cover_letter import CoverLetterResponse
from app.services.cover_letter import generate_cover_letter

router = APIRouter(prefix="/cover-letters", tags=["Cover Letters"])


@router.post("/{user_id}/{job_id}/generate", response_model=CoverLetterResponse)
def generate_cover_letter_for_job(
    user_id: int,
    job_id: int,
    user_model: str = Query(None),
    user_api_key: str = Query(None),
    db: Session = Depends(get_db),
):
    """Generate a cover letter using the latest resume linked to the job"""
    job = db.query(Job).filter(Job.id == job_id).first()  # ✅ Fetch job

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    latest_resume = (
        db.query(Resume)
        .filter(Resume.user_id == user_id, Resume.job_id == job_id)
        .order_by(Resume.id.desc())
        .first()
    )

    if not latest_resume:
        raise HTTPException(status_code=404, detail="No resume linked to this job")

    # ✅ Generate AI-powered cover letter
    cover_letter_text = generate_cover_letter(
        job.description, latest_resume.experience, user_model, user_api_key
    )

    new_cover_letter = CoverLetter(
        user_id=user_id,
        job_id=job_id,
        resume_id=latest_resume.id,
        content=cover_letter_text,
    )

    db.add(new_cover_letter)
    db.commit()
    db.refresh(new_cover_letter)

    return new_cover_letter
