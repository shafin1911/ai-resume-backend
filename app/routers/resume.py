from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.resume import Resume
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeResponse

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
