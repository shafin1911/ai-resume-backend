from fastapi import FastAPI
from app.routers import resume, job, job_match, cover_letter, user

app = FastAPI()

# ✅ Include Routers
app.include_router(user.router)
app.include_router(resume.router)
app.include_router(job.router)
app.include_router(job_match.router)
app.include_router(cover_letter.router)

# ✅ Ensure Alembic is used for migrations in production
print("🚀 FastAPI Server Running - Ensure Alembic migrations are applied!")
