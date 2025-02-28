from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    skills = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)
    education = Column(Text, nullable=True)
    parsed_text = Column(Text, nullable=True)
    improved_experience = Column(Text, nullable=True)  # New column
    ai_cover_letter = Column(Text, nullable=True)  # New column
