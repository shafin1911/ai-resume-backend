from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.job_matching import match_resume_to_job
from app.models.resume import Resume
from app.models.job import Job
from app.services.ai import optimize_resume_for_job
from app.schemas.resume import ResumeResponse

router = APIRouter(prefix="/job-match", tags=["Job Matching"])


@router.get("/{resume_id}/match/{job_id}")
def find_resume_match(resume_id: int, job_id: int, db: Session = Depends(get_db)):
    """Find how well a resume matches a specific job."""

    # Fetch the resume from DB
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Compute match percentage
    match_percentage, error = match_resume_to_job(
        resume.improved_experience or resume.experience, job_id, db
    )
    if error:
        raise HTTPException(status_code=404, detail=error)

    return {
        "resume_id": resume_id,
        "job_id": job_id,
        "match_percentage": match_percentage,
    }


@router.post("/{resume_id}/optimize/{job_id}", response_model=ResumeResponse)
def generate_resume_for_job(resume_id: int, job_id: int, db: Session = Depends(get_db)):
    """Create a job-specific resume if the match score is low."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    parent_resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not parent_resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # ✅ Correct: Improve the resume using the job description!
    improved_experience = optimize_resume_for_job(
        resume_text=parent_resume.experience, job_description=job.description
    )

    # ✅ Create a new resume linked to the job & parent resume
    new_resume = Resume(
        user_id=parent_resume.user_id,
        job_id=job.id,
        parent_resume_id=parent_resume.id,
        experience=improved_experience,
        improved_experience=improved_experience,
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return new_resume
