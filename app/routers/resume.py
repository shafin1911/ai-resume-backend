from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.resume import Resume
from app.schemas.resume import (
    ResumeCreate,
    ResumeUpdate,
    ResumeResponse,
    ResumeImprovementResponse,
)
from app.services.ai import (
    summarize_experience,
    improve_resume,
    generate_cover_letter,
)


# Create router for handling resume API requests
router = APIRouter(prefix="/resumes", tags=["Resumes"])


# ✅ Create a new resume
@router.post("/", response_model=ResumeResponse)
def create_resume(resume: ResumeCreate, db: Session = Depends(get_db)):
    # 🔍 Check if the email already exists
    existing_resume = db.query(Resume).filter(Resume.email == resume.email).first()
    if existing_resume:
        raise HTTPException(
            status_code=400,
            detail="Email already exists. Please use a different email.",
        )

    # ✅ Create a new resume
    new_resume = Resume(**resume.dict())
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    return new_resume


# ✅ Get a single resume by ID
@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


# ✅ Get all resumes
@router.get("/", response_model=List[ResumeResponse])
def get_all_resumes(db: Session = Depends(get_db)):
    return db.query(Resume).all()


# ✅ Update a resume
@router.put("/{resume_id}", response_model=ResumeResponse)
def update_resume(
    resume_id: int, updated_resume: ResumeUpdate, db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Update fields dynamically
    for key, value in updated_resume.dict(exclude_unset=True).items():
        setattr(resume, key, value)

    db.commit()
    db.refresh(resume)
    return resume


# ✅ Delete a resume
@router.delete("/{resume_id}")
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    db.delete(resume)
    db.commit()
    return {"message": "Resume deleted successfully"}


# ✅ Improve resume with optional AI model & API key
@router.post("/{resume_id}/improve", response_model=ResumeImprovementResponse)
def improve_resume_endpoint(
    resume_id: int,
    db: Session = Depends(get_db),
    user_model: str = None,
    user_api_key: str = None,
):
    """
    Improve an existing resume entry using AI.
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not resume:
        return {"error": "Resume not found"}

    improved_text = improve_resume(resume.experience, user_model, user_api_key)

    # ✅ Save improved text in the new `improved_experience` column
    resume.improved_experience = improved_text
    db.commit()
    db.refresh(resume)

    return {"improved_experience": improved_text}


# ✅ AI-powered Cover Letter Generation
@router.post("/{resume_id}/cover-letter", response_model=dict)
def generate_resume_cover_letter(
    resume_id: int,
    job_description: str,
    db: Session = Depends(get_db),
    user_model: str = None,
    user_api_key: str = None,
):
    """
    Generate a professional cover letter using AI.
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not resume:
        return {"error": "Resume not found"}

    cover_letter = generate_cover_letter(
        job_description, resume.experience, user_model, user_api_key
    )

    # ✅ Store cover letter in the database
    resume.ai_cover_letter = cover_letter
    db.commit()
    db.refresh(resume)

    return {"cover_letter": cover_letter}
