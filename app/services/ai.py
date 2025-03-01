import os
from transformers import pipeline
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Default AI Model (Qwen Free)
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen/qwen2.5-vl-72b-instruct:free")
DEFAULT_API_KEY = os.getenv("DEFAULT_API_KEY", "")  # Optional: Store in .env


# ✅ Improve Resume Using OpenRouter via LangChain
def improve_resume(
    resume_text: str, user_model: str = None, user_api_key: str = None
) -> str:
    """Improve resume experience using OpenRouter AI."""
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
                "You are an AI resume optimizer. "
                "Your task is to take an input resume and improve it while maintaining the original structure, formatting, and sectioning. "
                "The output should be a complete and professional resume in markdown format, without any extra explanations, questions, or placeholders. "
                "Only return the final resume.",
            ),
            (
                "human",
                "Improve this resume while keeping proper sectioning and structure:\n{resume_text}\n\n"
                "Ensure the resume has a clear Markdown format, structured sections (such as **Summary, Experience, Education, Skills, Projects**), "
                "and is well-formatted without any additional text, comments, or requests for more details.",
            ),
        ]
    )

    chain = prompt | llm
    response = chain.invoke({"resume_text": resume_text})

    return response.content if hasattr(response, "content") else str(response)


# ✅ Summarize Experience Using Hugging Face
def summarize_experience(resume_text: str) -> str:
    """Summarize experience using a pre-trained summarization model."""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    max_length = 1024
    resume_text = resume_text[:max_length]  # Ensure within model limits
    summary = summarizer(resume_text, max_length=150, min_length=50, do_sample=False)
    return summary[0]["summary_text"]


# ✅ New Function for Job-Specific Resume Improvement
def optimize_resume_for_job(
    resume_text: str,
    job_description: str,
    user_model: str = None,
    user_api_key: str = None,
) -> str:
    """Optimize an existing resume to better match a job description using OpenRouter AI."""
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
                "You are an AI resume optimizer specializing in tailoring resumes for specific jobs. "
                "Your task is to enhance an input resume so that it better aligns with the given job description, "
                "while maintaining the resume's original structure and formatting. "
                "Ensure the final output is in professional Markdown format and requires no additional modifications.",
            ),
            (
                "human",
                "Here is a resume that needs to be improved for a job:\n\n"
                "**Job Description:**\n{job_description}\n\n"
                "**Current Resume:**\n{resume_text}\n\n"
                "Improve the resume so it is highly relevant to the job, keeping its structure (such as **Summary, Experience, Education, Skills, Projects**), "
                "and formatting intact. The output should be a fully improved Markdown resume with no extra explanations, questions, or placeholders.",
            ),
        ]
    )

    chain = prompt | llm
    response = chain.invoke(
        {"resume_text": resume_text, "job_description": job_description}
    )

    return response.content if hasattr(response, "content") else str(response)
