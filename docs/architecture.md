---

## **📌 Step 3: Document Database Schema**
📄 **Create `docs/database-schema.md`** to explain the database structure.  

### **📄 `docs/database-schema.md`**
```md
# 🗄️ Database Schema - AI Resume Builder
This document explains the database schema used in our PostgreSQL database.

---

## 📌 **Tables Overview**

### 1️⃣ **`resumes` Table**

Stores user resume details.

| Column Name              | Type      | Constraints        | Description                    |
| ------------------------ | --------- | ------------------ | ------------------------------ |
| `id`                     | `SERIAL`  | `PRIMARY KEY`      | Unique ID for each resume      |
| `name`                   | `VARCHAR` | `NOT NULL`         | Candidate's name               |
| `email`                  | `VARCHAR` | `UNIQUE, NOT NULL` | Candidate's email (unique)     |
| `phone`                  | `VARCHAR` |                    | Phone number                   |
| `linkedin_url`           | `VARCHAR` |                    | LinkedIn profile link          |
| `skills`                 | `TEXT`    |                    | List of skills                 |
| `experience`             | `TEXT`    |                    | Original work experience       |
| `ai_improved_experience` | `TEXT`    |                    | AI-enhanced experience section |
| `education`              | `TEXT`    |                    | Candidate's education history  |
| `ai_cover_letter`        | `TEXT`    |                    | AI-generated cover letter      |

---

## **📌 Relationships**

- Each `resume` entry is standalone (no foreign keys for now).
- Future enhancements may include **user authentication** (link resumes to users).

---

## 🎯 **Next Steps**

- ✅ **Enhance AI model selection logic**
- ✅ **Optimize database queries with indexing**
- ✅ **Add authentication support in the future**
