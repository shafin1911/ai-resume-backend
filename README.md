# 📝 AI-Powered Resume Builder (Backend)

🚀 FastAPI-based backend for AI-powered resume parsing, improvement, and cover letter generation.

## 🌟 Features

✅ Upload & Parse Resumes (Extract text from PDFs)  
✅ AI-Powered Resume Improvement (Better structure & ATS-friendly)  
✅ AI-Generated Cover Letters (Custom for job descriptions)  
✅ Store & Retrieve Resumes in PostgreSQL  
✅ Support for Multiple AI Models (OpenRouter, Hugging Face)  
✅ JWT Authentication (Upcoming)

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL + SQLAlchemy + Alembic
- **AI Models**: OpenAI, Hugging Face, OpenRouter
- **Caching & Background Tasks** (Planned): Redis + Celery
- **Containerization**: Docker + Docker Compose

---

## 🚀 Getting Started

### **1️⃣ Clone the Repository**

```sh
git clone https://github.com/your-username/ai-resume-backend.git
cd ai-resume-backend


## Set Up Environment Variables

Create a .env file and add the following:

env
Copy
Edit
DATABASE_URL=postgresql://postgres:password@db:5432/resume_db
DEFAULT_AI_API_KEY=your_openrouter_api_key
SECRET_KEY=your_secret_key
3️⃣ Run with Docker
sh
Copy
Edit
docker compose up --build -d

## Apply Migrations
sh
Copy
Edit
docker exec -it ai-resume-backend alembic upgrade head

## Access API Docs

Swagger UI: http://localhost:8000/docs
Redoc: http://localhost:8000/redoc

📌 API Endpoints
Method	Endpoint	Description
POST	/resumes/	Upload a new resume
GET	/resumes/{id}	Retrieve a resume
POST	/resumes/{id}/improve	AI-powered resume improvement
POST	/resumes/{id}/cover-letter	AI-generated cover letter
👉 For full API details, see docs/api-endpoints.md.

🏗️ Backend Structure
bash
Copy
Edit
/ai-resume-backend
│── app/
│   ├── main.py          # FastAPI entry point
│   ├── database.py      # DB connection & models
│   ├── models/          # SQLAlchemy ORM models
│   ├── schemas/         # Pydantic validation schemas
│   ├── routers/         # API routes
│   ├── services/        # Business logic & AI integration
│   ├── dependencies.py  # Reusable dependencies (DB, Auth)
│   ├── config.py        # Environment variables
│── alembic/             # DB migrations
│── docs/                # Additional documentation
│── Dockerfile           # Docker configuration
│── docker-compose.yml   # Docker setup
│── requirements.txt     # Dependencies
│── README.md            # Main project documentation
👉 For detailed architecture, see docs/architecture.md.

🛠️ Deployment
Coming soon! Will include guides for:
✅ Docker Swarm
✅ AWS/GCP Deployment
✅ CI/CD Pipeline
```
