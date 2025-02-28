# 📌 AI Resume Builder - API Documentation

This document provides a detailed overview of the API endpoints for the AI-powered resume builder.

## 🌐 Base URL

`http://localhost:8000`

---

## **1️⃣ Resume Management**

### 🟢 Create a Resume

📌 **Endpoint**: `POST /resumes/`  
✅ **Description**: Upload a new resume and store it in the database.

#### **📥 Request Body (JSON)**

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "123-456-7890",
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "skills": "Python, FastAPI, PostgreSQL",
  "experience": "5 years in backend development...",
  "education": "B.Sc. in Computer Science"
}
```

#### **📤 Response (201 Created)**

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "123-456-7890",
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "skills": "Python, FastAPI, PostgreSQL",
  "experience": "5 years in backend development...",
  "education": "B.Sc. in Computer Science"
}
```

---

### 🔵 Get a Resume

📌 **Endpoint**: `GET /resumes/{id}`  
✅ **Description**: Fetch a resume by its ID.

#### **📤 Response (200 OK)**

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "123-456-7890",
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "skills": "Python, FastAPI, PostgreSQL",
  "experience": "5 years in backend development...",
  "education": "B.Sc. in Computer Science",
  "ai_improved_experience": "Optimized experience using AI",
  "ai_cover_letter": "Generated AI cover letter"
}
```

---

## **2️⃣ AI-Powered Enhancements**

### ✨ Improve Resume Experience

📌 **Endpoint**: `POST /resumes/{id}/improve`  
✅ **Description**: Enhances the experience section of the resume using AI.

🔧 **Optional Query Parameters**:

- `user_model` → Use a custom AI model (e.g., "google/gemini-2.0-flash-thinking-exp:free")

#### **📤 Response (200 OK)**

```json
{
  "id": 1,
  "ai_improved_experience": "AI-optimized experience text..."
}
```

---

### 📜 Generate AI Cover Letter

📌 **Endpoint**: `POST /resumes/{id}/cover-letter`  
✅ **Description**: Generates a job-specific AI-powered cover letter.

#### **📥 Request Body (JSON)**

```json
{
  "job_description": "We are looking for a backend engineer skilled in Python..."
}
```

#### **📤 Response (200 OK)**

```json
{
  "id": 1,
  "ai_cover_letter": "Dear Hiring Manager, I am excited to apply for the Backend Engineer role..."
}
```

---

## **📌 Error Handling**

All API responses follow this error format:

```json
{
  "detail": "Error message here"
}
```

### **HTTP Status Codes**

| Code | Description                               |
| ---- | ----------------------------------------- |
| 200  | OK - Successful request                   |
| 201  | Created - Resource created successfully   |
| 400  | Bad Request - Invalid request data        |
| 404  | Not Found - Resume or resource not found  |
| 500  | Internal Server Error - Server-side error |

---

📌 **Note**: Ensure all requests include appropriate headers and authentication (if applicable). Happy coding! 🚀
