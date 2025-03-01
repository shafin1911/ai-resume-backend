from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse
from app.models.user import User
from app.services.job_matching import store_job  # ✅ Import ChromaDB function

router = APIRouter(prefix="/jobs", tags=["Jobs"])


# ✅ Create a new job
@router.post("/", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    if not job.user_id:
        raise HTTPException(
            status_code=400, detail="User ID is required and must be a valid integer."
        )

    user = db.query(User).filter(User.id == job.user_id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with ID {job.user_id} not found."
        )

    # ✅ Create job in the database
    new_job = Job(**job.dict())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    # ✅ Store job description in ChromaDB
    store_job(new_job.description, new_job.id)

    return new_job


# ✅ Get all jobs
@router.get("/", response_model=List[JobResponse])
def get_all_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()


# ✅ Get a single job
@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
