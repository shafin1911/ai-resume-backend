# 🤖 AI Integration - AI Resume Builder

This document explains how AI models are integrated into the backend.

---

## **📌 AI Services Used**

| AI Feature              | Model Provider | Description                           |
| ----------------------- | -------------- | ------------------------------------- |
| Resume Summarization    | Hugging Face   | Extracts key experience summary       |
| Resume Improvement      | OpenRouter AI  | Enhances resume for ATS compatibility |
| Cover Letter Generation | OpenRouter AI  | Generates a custom cover letter       |

---

## **🔧 How AI API Calls Work**

- API calls are made to **OpenRouter AI** via `httpx` (external API request).
- Users can **override the default model** using query parameters.

### **📥 Sample AI Request (Resume Improvement)**

```json
{
  "model": "google/gemini-2.0-flash-thinking-exp:free",
  "messages": [
    {
      "role": "system",
      "content": "You are an expert ATS-friendly resume optimizer."
    },
    { "role": "user", "content": "Improve this resume:\n[Experience]" }
  ]
}
```
