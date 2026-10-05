# DocFlow AI — AI Document Integration & Processing Platform

DocFlow AI is a full-stack SaaS-style document processing platform that combines **document ingestion, Google Drive integration, PDF/DOCX extraction, PostgreSQL persistence, authentication, and AI-powered document Q&A**.

Users can register/login, upload documents through **Manage Documentation**, or connect **Google Drive** to import supported documents. Extracted document content is stored in PostgreSQL and can be queried using **Groq-powered LLM inference**.

---

## 🚀 Live Application

**Frontend:** https://docflow-ai-three.vercel.app/

**Backend API:** https://docflow-ai-boj1.onrender.com/

**Swagger Documentation:** https://docflow-ai-boj1.onrender.com/docs

**Health Check:** https://docflow-ai-boj1.onrender.com/api/health

---

## ✨ Features

### Authentication

* JWT-based authentication
* User registration and login
* bcrypt password hashing
* Protected API routes
* User-specific document access

### Document Management

* PDF upload
* DOCX upload
* PDF/DOCX text extraction
* Document metadata storage
* Extracted text persistence
* Document listing and retrieval
* Document-specific AI Q&A

### Google Drive Integration

* Google OAuth 2.0
* Connect Google Drive
* Import supported documents
* User-specific integration handling
* Duplicate-aware document importing

### AI Document Q&A

* Natural-language document queries
* Groq-powered LLM inference
* Document-aware responses
* Context-based question answering
* Document-specific conversations
* AI provider abstraction

### Testing & Reliability

* Pytest backend testing
* Postman API testing
* Regression testing
* Edge-case validation
* Authentication testing
* Document-processing validation
* Structured error handling

---

## 🏗️ Architecture

```text
                         User
                           │
                           ▼
                ┌────────────────────┐
                │ React + Vite       │
                │ Tailwind Frontend  │
                │      Vercel        │
                └─────────┬──────────┘
                          │ REST / JSON
                          ▼
                ┌────────────────────┐
                │      FastAPI       │
                │      Backend       │
                │      Render        │
                └──────┬─────┬───────┘
                       │     │
              ┌────────┘     └─────────┐
              ▼                        ▼
       ┌──────────────┐         ┌──────────────┐
       │ PostgreSQL   │         │ Google Drive │
       │    Neon      │         │    OAuth     │
       └──────────────┘         └──────┬───────┘
                                       │
                                       ▼
                                PDF / DOCX
                                Processing
                                       │
                                       ▼
                                ┌────────────┐
                                │  Groq LLM  │
                                └────────────┘
```

---

## 🔄 Document Pipeline

```text
User Login
    ↓
Manage Documentation / Google Drive
    ↓
PDF / DOCX Upload or Import
    ↓
Text Extraction
    ↓
Document Processing
    ↓
PostgreSQL Storage
    ↓
Context Preparation
    ↓
Groq LLM
    ↓
AI Document Q&A
```

---

## 🖥️ How It Works

### 1. Register / Login

Users create an account or sign in.

```text
Register / Login
      ↓
JWT Authentication
      ↓
Dashboard
```

### 2. Upload Documents

Open **Manage Documentation** and upload a PDF or DOCX file.

```text
Upload PDF/DOCX
      ↓
Text Extraction
      ↓
Document Processing
      ↓
PostgreSQL
      ↓
Available for AI Q&A
```

### 3. Import from Google Drive

```text
Connect Google Drive
      ↓
Google OAuth
      ↓
Drive Authorization
      ↓
Import Document
      ↓
PDF/DOCX Processing
      ↓
PostgreSQL
```

### 4. Ask Questions

Users can open an uploaded/imported document and ask questions about its content.

```text
User Question
      +
Document Context
      ↓
Groq API
      ↓
AI Answer
```

Example:

```text
Question:
What is this document about?

Answer:
The document is a nomination letter from the college
principal, nominating a team to participate in the
Smart India Hackathon 2026.
```

---

# 🧰 Tech Stack

| Category       | Technologies                          |
| -------------- | ------------------------------------- |
| Frontend       | React, Vite, Tailwind CSS, JavaScript |
| Backend        | Python, FastAPI, SQLAlchemy, Pydantic |
| Authentication | JWT, Passlib, bcrypt                  |
| Database       | PostgreSQL, Neon                      |
| AI             | Groq API, `openai/gpt-oss-120b`       |
| Documents      | `pypdf`, `python-docx`                |
| Integration    | Google Drive API, Google OAuth 2.0    |
| Testing        | Pytest, Postman                       |
| Development    | Git, GitHub, Linux CLI                |
| Deployment     | Vercel, Render, Neon                  |

---

# 📁 Project Structure

```text
docflow-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── ai.py
│   │   │   ├── document.py
│   │   │   └── integrations/
│   │   └── main.py
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

Stores user identity, email, password hash, and account metadata.

### Documents

Stores document name, file type, source, extracted text, metadata, owner relationship, and timestamps.

### Conversations

Stores document-related AI interactions and associated metadata.

### Integrations

Stores information required for external service integrations.

---

# 🔌 REST API

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

FastAPI provides automatic OpenAPI documentation.

**Swagger UI**

https://docflow-ai-boj1.onrender.com/docs

**OpenAPI Specification**

https://docflow-ai-boj1.onrender.com/openapi.json

---

# 🤖 AI Document Q&A

DocFlow AI currently uses:

```text
Groq API
    ↓
openai/gpt-oss-120b
```

The backend prepares document content as context before sending the request to the LLM.

```text
Document Content
       +
User Question
       ↓
Context Preparation
       ↓
Groq LLM
       ↓
AI Response
```

The AI layer is separated from the document-processing logic, allowing the underlying model provider to be changed or extended later.

---

# ☁️ Google Drive Integration

DocFlow AI uses Google OAuth 2.0 for Drive integration.

```text
User
 ↓
Connect Google Drive
 ↓
Google OAuth
 ↓
OAuth Callback
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

The connector architecture can be extended to support additional services in the future.

Possible integrations:

```text
Google Drive
    ├── Dropbox
    ├── OneDrive
    ├── Notion
    ├── Slack
    └── Other SaaS APIs
```

---

# 💻 Local Development

## 1. Clone

```bash
git clone https://github.com/Vikas-tiwari-dot/docflow-ai.git

cd docflow-ai
```

## 2. Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

## 3. Backend Environment

Create:

```text
backend/.env
```

Example:

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

> Never commit `.env` files, API keys, database credentials, OAuth secrets, or other private credentials to GitHub.

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

Expected:

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

Start:

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

| Variable               | Purpose                  |
| ---------------------- | ------------------------ |
| `DATABASE_URL`         | PostgreSQL connection    |
| `JWT_SECRET`           | JWT signing secret       |
| `GROQ_API_KEY`         | Groq authentication      |
| `GROQ_MODEL`           | AI model                 |
| `CORS_ORIGINS`         | Allowed frontend origins |
| `FRONTEND_URL`         | Frontend URL             |
| `GOOGLE_CLIENT_ID`     | Google OAuth client ID   |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret      |
| `GOOGLE_REDIRECT_URI`  | OAuth callback           |

## Frontend

| Variable       | Purpose         |
| -------------- | --------------- |
| `VITE_API_URL` | Backend API URL |

---

# 🧪 Testing

Run backend tests:

```bash
cd backend

source .venv/bin/activate

pytest
```

Testing covers areas such as:

* Authentication
* API validation
* Document processing
* Database interactions
* Error handling
* Regression scenarios

API endpoints can also be tested using Postman.

---

# ⚠️ Error Handling

The API uses structured HTTP responses:

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

Handled application scenarios include:

* Duplicate registration
* Invalid credentials
* Missing documents
* Invalid document formats
* OAuth configuration errors
* External API failures
* AI service failures
* Database failures

---

# 🚀 Deployment

```text
                    Internet
                       │
                       ▼
                ┌─────────────┐
                │   Vercel    │
                │   React     │
                └──────┬──────┘
                       │ HTTPS
                       ▼
                ┌─────────────┐
                │   Render    │
                │   FastAPI   │
                └──────┬──────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
        ┌──────────┐       ┌──────────┐
        │   Neon   │       │   Groq   │
        │PostgreSQL│       │   LLM    │
        └──────────┘       └──────────┘
              │
              ▼
       ┌─────────────┐
       │Google Drive │
       │    OAuth    │
       └─────────────┘
```

### Deployment

* **Frontend:** Vercel
* **Backend:** Render
* **Database:** Neon PostgreSQL
* **AI:** Groq

---

# 🔐 Security

The application follows basic security practices:

* bcrypt password hashing
* JWT authentication
* Protected API routes
* Environment-based secrets
* Server-side OAuth credentials
* User-specific document access
* Configured CORS
* No credentials committed to source control

---

# 🔮 Future Improvements

* Refresh-token rotation
* OAuth token encryption
* Rate limiting
* Background document processing
* Task queues
* Object storage
* Vector database integration
* Semantic search
* RAG
* Document chunk indexing
* Observability
* CI/CD automation
* Security scanning
* Role-based access control
* Audit logging
* Multi-tenant organizations
* Subscription and billing

---

# 💡 Engineering Highlights

DocFlow AI demonstrates practical experience with:

* Full-stack application development
* REST API design
* FastAPI backend development
* PostgreSQL database design
* JWT authentication
* OAuth 2.0 integration
* External API integration
* PDF/DOCX processing
* AI/LLM integration
* Automated testing
* Debugging and error handling
* Cloud deployment

The project demonstrates an end-to-end document workflow:

```text
Ingest
  ↓
Extract
  ↓
Process
  ↓
Persist
  ↓
Retrieve
  ↓
Query with AI
```

---

# 📌 Resume Positioning

### DocFlow AI — AI Document Integration Platform

`React · FastAPI · PostgreSQL · REST APIs · Groq · OAuth`

> Built a document processing platform with JWT authentication, Google Drive OAuth integration, PDF/DOCX extraction, PostgreSQL persistence, REST APIs, and Groq-powered document Q&A; deployed the frontend on Vercel and backend on Render with PostgreSQL on Neon.

---

# 👨‍💻 Author

**Vikas Tiwari**

B.Tech Computer Science & Engineering
ABES Institute of Technology, Ghaziabad

* **GitHub:** https://github.com/Vikas-tiwari-dot
* **LinkedIn:** https://linkedin.com/in/vikas-tiwari-4226a03a/
* **LeetCode:** https://leetcode.com/u/vikas7375/

---

# 📄 License

This project is licensed under the **MIT License**.
