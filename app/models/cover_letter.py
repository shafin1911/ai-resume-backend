from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class CoverLetter(Base):
    __tablename__ = "cover_letters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Links to User
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)  # ✅ Links to Job
    resume_id = Column(
        Integer, ForeignKey("resumes.id"), nullable=False
    )  # ✅ Links to Resume
    content = Column(Text, nullable=False)

    user = relationship("User", back_populates="cover_letters")
    job = relationship("Job", back_populates="cover_letters")
    resume = relationship("Resume", back_populates="cover_letters")
