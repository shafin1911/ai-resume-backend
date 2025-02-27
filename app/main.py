from fastapi import FastAPI
from app.routers import resume
from app.database import engine
from app.models import resume as resume_model

app = FastAPI()

# Register the resume router
app.include_router(resume.router)

# Ensure database tables are created (only runs once)
resume_model.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Welcome to the AI Resume API"}
