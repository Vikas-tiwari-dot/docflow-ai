# DocFlow AI — AI Document Integration & Processing Platform

DocFlow AI is a full-stack SaaS-style document processing platform that combines **document ingestion, Google Drive integration, structured document extraction, authentication, PostgreSQL persistence, and AI-powered document Q&A**.

Users can register/login, upload **PDF/DOCX** documents through **Manage Documentation**, or connect **Google Drive** to import supported documents. DocFlow AI extracts document content, stores metadata and extracted text in PostgreSQL, and allows users to ask natural-language questions about their documents using **Groq-powered LLM inference**.

---

## 🚀 Live Application

**Frontend:**
https://docflow-ai-three.vercel.app/

**Backend API:**
https://docflow-ai-boj1.onrender.com/

**API Health Check:**
https://docflow-ai-boj1.onrender.com/api/health

**Swagger API Documentation:**
https://docflow-ai-boj1.onrender.com/docs

---

# ✨ Features

## 🔐 Authentication

* JWT-based authentication
* User registration and login
* Secure password hashing with bcrypt
* Protected API routes
* User-specific document access

## 📄 Document Management

* Upload PDF documents
* Upload DOCX documents
* PDF text extraction
* DOCX text extraction
* Document metadata storage
* Extracted text persistence
* Document listing and retrieval
* Document-specific AI Q&A

## ☁️ Google Drive Integration

* Google OAuth 2.0 integration
* Connect Google Drive
* Import supported documents
* User-specific integration handling
* PDF/DOCX document ingestion
* Duplicate-aware document importing

## 🤖 AI Document Q&A

* Natural-language document queries
* Groq-powered LLM inference
* Document-aware responses
* Context-based question answering
* Document-specific conversations
* AI provider abstraction for future model changes

## 🧪 Testing & Reliability

* Pytest-based backend testing
* API testing with Postman
* Regression testing
* Edge-case validation
* Authentication testing
* Document-processing validation
* Structured error handling
* Production logging

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │        User         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                     ┌──────────────────────────┐
                     │   React + Vite + Tailwind│
                     │        Frontend          │
                     │         Vercel           │
                     └────────────┬─────────────┘
                                  │ REST / JSON
                                  ▼
                     ┌──────────────────────────┐
                     │         FastAPI          │
                     │         Backend          │
                     │          Render          │
                     └──────┬─────────┬─────────┘
                            │         │
                 ┌──────────┘         └──────────────┐
                 ▼                                   ▼
        ┌─────────────────┐                 ┌─────────────────┐
        │   PostgreSQL    │                 │   Google Drive  │
        │      Neon       │                 │      OAuth      │
        └─────────────────┘                 └────────┬────────┘
                                                     │
                                                     ▼
                                            ┌─────────────────┐
                                            │ PDF / DOCX      │
                                            │ Processing      │
                                            └────────┬────────┘
                                                     │
                                                     ▼
                                            ┌─────────────────┐
                                            │    Groq LLM     │
                                            │   GPT-OSS-120B  │
                                            └─────────────────┘
```

---

# 🔄 Core Document Pipeline

```text
User Authentication
        ↓
Manage Documentation / Google Drive
        ↓
PDF / DOCX Upload or Import
        ↓
Document Text Extraction
        ↓
Document Processing
        ↓
PostgreSQL Storage
        ↓
Context Preparation
        ↓
Groq LLM
        ↓
AI-powered Document Q&A
```

---

# 🖥️ How to Use

## 1. Register / Sign In

Create an account or sign in using the authentication system.

```text
Register / Login
       ↓
JWT Authentication
       ↓
Dashboard
```

---

## 2. Manage Documentation

After signing in, open **Manage Documentation** from the dashboard.

Upload a PDF or DOCX file from your device.

```text
Manage Documentation
        ↓
Upload Document
        ↓
Select PDF / DOCX
        ↓
Document Processing
        ↓
Text Extraction
        ↓
PostgreSQL Storage
        ↓
Available for AI Q&A
```

### Supported Formats

* PDF
* DOCX

After processing, the extracted document content and metadata are stored and the document becomes available for AI-powered questions.

---

## 3. Connect Google Drive

Users can connect Google Drive through the Google OAuth integration.

```text
Connect Google Drive
        ↓
Google OAuth Authorization
        ↓
Drive Access
        ↓
Import Supported Documents
        ↓
PDF / DOCX Processing
        ↓
PostgreSQL Storage
        ↓
AI Q&A
```

This allows users to import supported documents from their connected Google Drive instead of manually uploading them.

---

## 4. Ask Questions About Documents

Open an uploaded or imported document and ask questions about its content.

Example:

```text
Question:
What is this document about?

Answer:
The document is a nomination letter from the college
principal, nominating a team to participate in the
Smart India Hackathon 2026.
```

The backend prepares relevant document content as context and sends the request to the configured Groq-powered LLM.

---

# 🧰 Tech Stack

## Frontend

* React
* Vite
* Tailwind CSS
* JavaScript
* REST APIs

## Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* JWT
* Passlib
* bcrypt

## Database

* PostgreSQL
* Neon PostgreSQL
* SQLAlchemy ORM

## AI

* Groq API
* `openai/gpt-oss-120b`

## Document Processing

* `pypdf`
* `python-docx`

## Integrations

* Google Drive API
* Google OAuth 2.0

## Development & Testing

* Git
* GitHub
* Postman
* Pytest
* Linux CLI

## Deployment

* Vercel — Frontend
* Render — Backend
* Neon — PostgreSQL

---

# 📁 Project Structure

```text
docflow-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   └── ...
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   │
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── ai.py
│   │   │   ├── document.py
│   │   │   └── integrations/
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── lib/
│   │   └── ...
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── docs/
├── .gitignore
├── README.md
└── LICENSE
```

---

# 🗄️ Database Architecture

DocFlow AI uses PostgreSQL for persistent application data.

```text
users
  │
  ├── documents
  │
  ├── conversations
  │
  └── integrations
```

### Users

Stores:

* User identity
* Email
* Password hash
* Account metadata

### Documents

Stores:

* Document name
* File type
* Source
* Extracted text
* Metadata
* Owner/user relationship
* Timestamps

### Conversations

Stores document-related AI interactions and associated metadata.

### Integrations

Stores information required to manage external service integrations for authenticated users.

---

# 🔌 REST API

Representative endpoints include:

## Authentication

```text
POST /api/auth/register
POST /api/auth/login
```

## Documents

```text
GET  /api/documents
GET  /api/documents/{document_id}
POST /api/documents/{document_id}/chat
```

## Google Drive

```text
GET  /api/integrations/google/connect
GET  /api/integrations/google/callback
POST /api/integrations/google/import
```

## Health

```text
GET /api/health
```

---

# 📚 API Documentation

FastAPI automatically generates OpenAPI documentation.

### Swagger UI

https://docflow-ai-boj1.onrender.com/docs

### OpenAPI Specification

https://docflow-ai-boj1.onrender.com/openapi.json

The API documentation can be used to inspect endpoints, request schemas, response formats, and authentication requirements.

---

# 🧠 AI Document Q&A

DocFlow AI uses Groq for AI-powered document question answering.

Current configured model:

```text
openai/gpt-oss-120b
```

The backend prepares document content as context before sending the request to the LLM.

```text
User Question
      +
Document Context
      ↓
Groq API
      ↓
AI Answer
```

The AI layer is separated from the core document-processing pipeline, making it easier to replace or extend the underlying model provider.

---

# ☁️ Google Drive Integration

DocFlow AI uses Google OAuth 2.0 for Google Drive integration.

### Integration Flow

```text
User
 ↓
Connect Google Drive
 ↓
Google OAuth Authorization
 ↓
OAuth Callback
 ↓
Backend Authentication
 ↓
Google Drive API
 ↓
Document Import
 ↓
PDF/DOCX Processing
 ↓
PostgreSQL
 ↓
AI Q&A
```

The connector architecture is designed so that additional SaaS integrations can be added independently.

Potential future integrations include:

```text
Google Drive
     │
     ├── Dropbox
     ├── OneDrive
     ├── Notion
     ├── Slack
     └── Other SaaS APIs
```

---

# 🧪 Testing

Run backend tests:

```bash
cd backend

source .venv/bin/activate

pytest
```

Testing areas include:

* Authentication
* API validation
* Document processing
* Error handling
* Database interactions
* Regression scenarios

API endpoints can additionally be tested using Postman.

---

# ⚠️ Error Handling

The backend uses structured HTTP responses for common failures.

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Validation Error
500 Internal Server Error
503 Service Unavailable
```

Application-level handling includes:

* Duplicate user registration
* Invalid credentials
* Missing documents
* Invalid document formats
* OAuth configuration errors
* External API failures
* AI service failures
* Database failures

---

# 🔐 Security

The application follows several security practices:

* Passwords are hashed using bcrypt
* JWT authentication protects private resources
* Secrets are provided through environment variables
* Production credentials are not committed to Git
* CORS is configured for the frontend
* User-specific resources require authentication
* OAuth credentials are handled server-side
* Database credentials are stored through environment configuration

> **Never commit `.env` files, API keys, database credentials, OAuth secrets, or other private credentials to GitHub.**

---

# 💻 Local Development

## 1. Clone Repository

```bash
git clone https://github.com/Vikas-tiwari-dot/docflow-ai.git

cd docflow-ai
```

---

## 2. Backend Setup

```bash
cd backend

python -m venv .venv

source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Backend Environment Variables

Create:

```text
backend/.env
```

Use placeholder values:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/docflow

JWT_SECRET=your-secret-key

GROQ_API_KEY=your-groq-api-key

GROQ_MODEL=openai/gpt-oss-120b

CORS_ORIGINS=http://localhost:5173

FRONTEND_URL=http://localhost:5173

GOOGLE_CLIENT_ID=your-google-client-id

GOOGLE_CLIENT_SECRET=your-google-client-secret

GOOGLE_REDIRECT_URI=http://localhost:8000/api/integrations/google/callback
```

**Do not use real credentials in the README.**

---

## 4. Start Backend

```bash
cd backend

source .venv/bin/activate

python -m uvicorn app.main:app \
  --reload \
  --reload-dir app \
  --port 8000
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

Health check:

```bash
curl http://localhost:8000/api/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "docflow-api"
}
```

---

# 🎨 Frontend Setup

Open another terminal:

```bash
cd frontend

npm install
```

Create:

```text
frontend/.env
```

Add:

```env
VITE_API_URL=http://localhost:8000
```

Start the frontend:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# ⚙️ Environment Variables

## Backend

| Variable               | Purpose                        |
| ---------------------- | ------------------------------ |
| `DATABASE_URL`         | PostgreSQL connection string   |
| `JWT_SECRET`           | JWT signing secret             |
| `GROQ_API_KEY`         | Groq API authentication        |
| `GROQ_MODEL`           | AI model used for document Q&A |
| `CORS_ORIGINS`         | Allowed frontend origins       |
| `FRONTEND_URL`         | Frontend application URL       |
| `GOOGLE_CLIENT_ID`     | Google OAuth client ID         |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret     |
| `GOOGLE_REDIRECT_URI`  | Google OAuth callback URL      |

## Frontend

| Variable       | Purpose              |
| -------------- | -------------------- |
| `VITE_API_URL` | Backend API base URL |

---

# 🚀 Deployment

## Frontend

The React/Vite frontend is deployed using Vercel.

```text
Frontend
   ↓
Vercel
   ↓
React + Vite
```

## Backend

The FastAPI backend is deployed using Render.

```text
Backend
   ↓
Render
   ↓
FastAPI
```

## Database

The production PostgreSQL database is hosted using Neon.

```text
FastAPI
   ↓
SQLAlchemy
   ↓
PostgreSQL
   ↓
Neon
```

---

# 🌐 Production Architecture

```text
                         Internet
                            │
                            ▼
                 ┌─────────────────────┐
                 │       Vercel        │
                 │   React Frontend    │
                 └──────────┬──────────┘
                            │ HTTPS
                            ▼
                 ┌─────────────────────┐
                 │       Render        │
                 │   FastAPI Backend   │
                 └──────┬──────┬───────┘
                        │      │
              ┌─────────┘      └───────────┐
              ▼                            ▼
      ┌───────────────┐             ┌──────────────┐
      │     Neon      │             │     Groq     │
      │  PostgreSQL   │             │      LLM     │
      └───────────────┘             └──────────────┘
                        │
                        ▼
                ┌────────────────┐
                │  Google Drive  │
                │     OAuth      │
                └────────────────┘
```

---

# 🔮 Future Improvements

Potential improvements include:

* Refresh-token rotation
* OAuth token encryption at rest
* Rate limiting
* Background document processing
* Task queues
* Object storage for uploaded files
* Vector database integration
* Semantic search
* Retrieval-Augmented Generation (RAG)
* Document chunk indexing
* Improved observability
* Automated CI/CD
* Automated security scanning
* Role-based access control
* Audit logs
* Multi-tenant organization support
* Subscription and billing infrastructure

---

# 💡 Engineering Highlights

DocFlow AI demonstrates practical experience across:

* Full-stack application development
* REST API design
* Backend engineering with FastAPI
* PostgreSQL database design
* Authentication and authorization
* OAuth 2.0 integration
* External API integration
* PDF/DOCX data extraction
* AI/LLM integration
* Error handling and debugging
* Automated testing
* Production deployment
* Cloud-based application architecture

The project demonstrates how a document-centric SaaS platform can accept documents through direct uploads or external integrations, process unstructured content, persist structured data, and provide an AI-powered interface for querying that information.

---

# 📌 Resume Positioning

### DocFlow AI — AI Document Integration Platform

`React · FastAPI · PostgreSQL · REST APIs · Groq · OAuth`

> Built a document processing platform with JWT authentication, Google Drive OAuth integration, PDF/DOCX extraction, PostgreSQL persistence, REST APIs, and Groq-powered document Q&A; deployed the frontend on Vercel and backend on Render with PostgreSQL on Neon.

---

---

# 👨‍💻 Author

**Vikas Tiwari**

B.Tech Computer Science & Engineering
ABES Institute of Technology, Ghaziabad

* GitHub: https://github.com/Vikas-tiwari-dot
* LinkedIn: https://linkedin.com/in/vikas-tiwari-4226a03a/
* LeetCode: https://leetcode.com/u/vikas7375/

---

# 📄 License

This project is licensed under the **MIT License**.
