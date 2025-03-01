import os
from transformers import pipeline
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Default AI Model (Qwen Free)
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen/qwen2.5-vl-72b-instruct:free")
DEFAULT_API_KEY = os.getenv("DEFAULT_API_KEY", "")  # Optional: Store in .env


# ✅ Generate AI-Powered Cover Letters
def generate_cover_letter(
    job_description: str,
    experience: str,
    user_model: str = None,
    user_api_key: str = None,
) -> str:
    """Generate a professional cover letter using AI."""
    model = user_model or DEFAULT_MODEL
    api_key = user_api_key or DEFAULT_API_KEY

    llm = ChatOpenAI(
        model=model,
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert in writing professional cover letters. "
                "You must generate a complete and professional cover letter based on the given job description and experience. "
                "Do not ask for any additional details. "
                "Your response should be a finalized markdown-formatted cover letter, not a draft or a request for more information.",
            ),
            (
                "human",
                "Write a professional cover letter for this job:\n{job_description}\n"
                "Based on this experience:\n{experience}.\n"
                "Ensure the output is fully written, properly formatted in markdown, and requires no further input from me.",
            ),
        ]
    )

    chain = prompt | llm
    response = chain.invoke(
        {"job_description": job_description, "experience": experience}
    )

    return response.content if hasattr(response, "content") else str(response)
