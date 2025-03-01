from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)
    parent_resume_id = Column(
        Integer, ForeignKey("resumes.id"), nullable=True
    )  # ✅ Track AI-generated versions
    experience = Column(Text, nullable=False)
    improved_experience = Column(Text)
    summary_experience = Column(Text)

    user = relationship("User", back_populates="resumes")
    job = relationship("Job", back_populates="resumes")
    cover_letters = relationship(
        "CoverLetter", back_populates="resume", cascade="all, delete-orphan"
    )
    parent_resume = relationship(
        "Resume", remote_side=[id]
    )  # ✅ Link to the original resume
