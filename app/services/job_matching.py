import numpy as np
import logging
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from sqlalchemy.orm import Session
from app.models.job import Job
from app.services.ai import summarize_experience

# ✅ Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ✅ Initialize an embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Ensure this is mapped in Docker
DB_PATH = "/app/chromadb"

# ✅ Connect to ChromaDB with embeddings
db = Chroma(
    collection_name="job-matching",
    persist_directory=DB_PATH,  # Ensure this directory exists for persistence
    embedding_function=embedding_model,  # ✅ Provide embedding function
)


# ✅ Function to compute cosine similarity manually
def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


# ✅ Function to store job descriptions in ChromaDB
def store_job(job_text: str, job_id: int):
    """Store job descriptions for matching against resumes."""

    # Generate job embedding
    try:
        summary_text = summarize_experience(job_text)
        job_embedding = embedding_model.embed_query(summary_text)
        if job_embedding is None:
            raise ValueError("❌ Embedding generation failed!")
    except Exception as e:
        logger.error(f"❌ Error in embedding generation: {e}")
        return

    # Check if job already exists in ChromaDB
    try:
        existing_data = db.get(include=["embeddings"], where={"job_id": str(job_id)})
        if existing_data and existing_data["embeddings"]:
            logger.warning(
                f"⚠️ Job {job_id} already exists in ChromaDB. Skipping storage."
            )
            return

        # Store in ChromaDB
        db.add_texts(
            [job_text],
            metadatas=[{"job_id": str(job_id)}],
            embeddings=[job_embedding],
        )
        logger.info(f"✅ Job {job_id} stored successfully in ChromaDB!")

        # Verify storage
        results = db.get(include=["embeddings"], where={"job_id": str(job_id)})
        if results and results["embeddings"]:
            logger.info(
                f"✅ Embedding successfully stored and retrieved for Job {job_id}!"
            )
        else:
            logger.warning(
                f"⚠️ Storage verification failed for Job {job_id}. Check ChromaDB persistence settings."
            )

    except Exception as e:
        logger.error(f"❌ Error storing job embedding in ChromaDB: {e}")


# ✅ Function to match a resume against a specific job
def match_resume_to_job(resume_text: str, job_id: int, db_session: Session):
    """Match a resume to a job description and return a match percentage."""

    # Fetch job description from the database
    job = db_session.query(Job).filter(Job.id == job_id).first()
    if not job:
        logger.warning(f"⚠️ Job ID {job_id} not found in the database.")
        return None, "Job not found"

    # Encode the resume text using the same embedding model
    try:
        summary_text = summarize_experience(resume_text)
        resume_embedding = embedding_model.embed_query(summary_text)
    except Exception as e:
        logger.error(f"❌ Error in resume embedding generation: {e}")
        return None, "Failed to generate resume embedding"

    # ✅ Retrieve job embedding from ChromaDB
    try:
        results = db.get(include=["embeddings"], where={"job_id": str(job_id)})

        if not results or not results["embeddings"]:
            logger.warning(f"⚠️ Job ID {job_id} embedding not found in ChromaDB.")
            return None, "Job embedding not found in ChromaDB"

        job_embedding = results["embeddings"][
            0
        ]  # ✅ Extract the first embedding correctly

        # ✅ Compute cosine similarity using the extracted embedding
        similarity_score = cosine_similarity(resume_embedding, job_embedding)

        # ✅ Convert similarity to a percentage (0 to 100)
        match_percentage = round(similarity_score * 100, 2)

        logger.info(f"✅ Resume match for Job {job_id}: {match_percentage}% similarity")
        return match_percentage, None

    except Exception as e:
        logger.error(f"❌ Error retrieving job embedding from ChromaDB: {e}")
        return None, "Error retrieving job embedding from ChromaDB"
