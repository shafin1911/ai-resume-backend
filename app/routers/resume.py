from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from app.utils.pdf_parser import extract_experience_from_pdf
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.resume import Resume
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeResponse
from app.services.ai import improve_resume, summarize_experience
from app.models.user import User
from app.models.job import Job

router = APIRouter(prefix="/resumes", tags=["Resumes"])


# ✅ Create a new resume
@router.post("/", response_model=ResumeResponse)
def create_resume(resume: ResumeCreate, db: Session = Depends(get_db)):
    # ✅ Check if user exists
    user = db.query(User).filter(User.id == resume.user_id).first()
    if not user:
        raise HTTPException(
            status_code=400, detail=f"User with id {resume.user_id} does not exist."
        )

    # ✅ Create the resume only if user exists
    new_resume = Resume(**resume.dict())
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    return new_resume


# ✅ Upload a resume and store it in the database
@router.post("/upload-resume/{user_id}", response_model=ResumeResponse)
async def upload_resume(
    user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    """Upload a resume PDF, extract experience, and store in the database"""

    # ✅ Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=400, detail=f"User with id {user_id} does not exist."
        )

    # ✅ Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # ✅ Save file temporarily
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # ✅ Extract experience from the PDF
    extracted_experience = extract_experience_from_pdf(file_path)

    # ✅ Store resume in DB
    new_resume = Resume(user_id=user_id, experience=extracted_experience)
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return new_resume


# ✅ Get all resumes for a user
@router.get("/user/{user_id}", response_model=List[ResumeResponse])
def get_user_resumes(user_id: int, db: Session = Depends(get_db)):
    return db.query(Resume).filter(Resume.user_id == user_id).all()


# ✅ Get a single resume by ID
@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


# ✅ Improve resume experience (AI-powered)
@router.post("/{resume_id}/improve", response_model=ResumeResponse)
def improve_resume_endpoint(
    resume_id: int,
    user_model: str = Query(None),
    user_api_key: str = Query(None),
    db: Session = Depends(get_db),
):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    improved_text = improve_resume(resume.experience, user_model, user_api_key)
    summary_text = summarize_experience(improved_text)

    resume.improved_experience = improved_text
    resume.summary_experience = summary_text
    db.commit()
    db.refresh(resume)

    return resume


# ✅ Update resume manually
@router.put("/{resume_id}", response_model=ResumeResponse)
def update_resume(
    resume_id: int, updated_resume: ResumeUpdate, db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

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


# ✅ Link a resume to a job
@router.post("/{user_id}/add-job/{job_id}", response_model=ResumeResponse)
def link_resume_to_job(user_id: int, job_id: int, db: Session = Depends(get_db)):
    """Link the user's resume to a job"""

    # ✅ Check if job exists
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=400, detail=f"Job with id {job_id} does not exist."
        )

    # ✅ Find user's unlinked resume
    user_resume = (
        db.query(Resume)
        .filter(Resume.user_id == user_id, Resume.job_id == None)
        .first()
    )

    if not user_resume:
        raise HTTPException(status_code=404, detail="User does not have a base resume.")

    # ✅ Link the resume to the job
    user_resume.job_id = job_id
    db.commit()
    db.refresh(user_resume)

    return user_resume
