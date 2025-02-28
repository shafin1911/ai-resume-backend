import os
from transformers import pipeline
import httpx

# Default model (Free Qwen)
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "")
DEFAULT_API_KEY = os.getenv("DEFAULT_API_KEY", "")  # Optional: Store in .env


# ✅ Function to improve resume text using OpenAI
def improve_resume(
    resume_text: str, user_model: str = None, user_api_key: str = None
) -> str:
    """Improve resume text using AI (OpenRouter API)."""

    model = user_model if user_model else DEFAULT_MODEL
    api_key = user_api_key if user_api_key else DEFAULT_API_KEY

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert ATS-friendly resume optimizer.",
            },
            {
                "role": "user",
                "content": f"Improve this resume (keep markdown structure):\n{resume_text}",
            },
        ],
    }

    response = httpx.post(url, headers=headers, json=payload)
    response_json = response.json()

    # ✅ Debug log AI response
    print("🔹 AI Response:", response_json)

    if "choices" not in response_json:
        return "Error: AI response is invalid."

    return response_json["choices"][0]["message"]["content"]


# ✅ Function to summarize experience using Hugging Face
def summarize_experience(resume_text: str) -> str:
    summarizer = pipeline("summarization")
    summary = summarizer(resume_text, max_length=150, min_length=50, do_sample=False)
    return summary[0]["summary_text"]


# ✅ Function to generate AI-powered cover letters
def generate_cover_letter(
    job_description: str,
    experience: str,
    user_model: str = None,
    user_api_key: str = None,
) -> str:
    """
    AI-generated cover letter based on job description and experience.
    - Allows users to specify their own AI model & API key.
    - Uses a free model by default.
    """

    model = user_model if user_model else DEFAULT_MODEL
    api_key = user_api_key if user_api_key else DEFAULT_API_KEY

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert in writing professional cover letters.",
            },
            {
                "role": "user",
                "content": f"Write a professional cover letter for this job:\n{job_description}\nBased on this experience:\n{experience}. Output should be in markdown format.",
            },
        ],
    }

    response = httpx.post(url, headers=headers, json=payload)
    response_json = response.json()

    print("🔹 AI Cover Letter Response:", response_json)

    if "choices" not in response_json:
        return f"Error: {response_json}"

    return response_json["choices"][0]["message"]["content"]
