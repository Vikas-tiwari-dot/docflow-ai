# DocFlow AI — AI Document Integration & Processing Platform

DocFlow AI is a production-oriented SaaS-style platform for uploading, importing, processing, and querying documents using AI.

The project demonstrates backend engineering and data-integration concepts including **JWT authentication, REST APIs, PDF/DOCX processing, PostgreSQL, OAuth-based SaaS integrations, validation, structured error handling, logging, testing, and AI-powered document Q&A**.

## Architecture

```text
User
  │
  ▼
React + Vite + Tailwind
  │
  │ REST / JSON
  ▼
FastAPI Backend
  │
  ├── JWT Authentication
  │
  ├── Document Service
  │     ├── PDF/DOCX Extraction
  │     ├── Text Normalization
  │     └── Document Chunking
  │
  ├── Integration Service
  │     └── Google Drive OAuth → Drive API → Import
  │
  ├── AI Service
  │     └── Groq / LLM
  │
  └── SQLAlchemy
        │
        ▼
   PostgreSQL
```

### Core Pipeline

```text
External SaaS/API
       ↓
Authentication
       ↓
Data Extraction
       ↓
Validation
       ↓
Document Processing
       ↓
PostgreSQL
       ↓
AI Processing
       ↓
REST API
       ↓
React Frontend
```

---

## Features

* Multi-user registration and login with **bcrypt password hashing** and **JWT authentication**
* User-scoped document access and deletion
* PDF and DOCX document upload
* File type, size, empty-file, and duplicate validation
* Text extraction, normalization, hashing, status tracking, and chunking
* AI-powered document Q&A using **Groq**
* Context-aware answers generated from document chunks
* Persistent chat history stored in PostgreSQL
* Google Drive OAuth integration
* Google Drive PDF/DOCX import
* Reusable SaaS connector architecture
* Consistent JSON error responses
* Centralized exception handling
* Structured application logging
* FastAPI OpenAPI documentation
* Pytest backend tests
* Postman API collection
* Docker Compose support for local development

---

## Tech Stack

### Frontend

* React
* Vite
* Tailwind CSS
* JavaScript
* REST API integration

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* JWT
* bcrypt
* Pytest

### Database

* PostgreSQL

### AI

* Groq API
* `openai/gpt-oss-120b`

### Integrations

* Google Drive API
* Google OAuth 2.0

### Tools

* Git / GitHub
* Postman
* Docker
* Linux/macOS CLI

---

## Project Structure

```text
docflow-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/              # HTTP routes/controllers
│   │   ├── connectors/       # SaaS connector abstractions
│   │   ├── core/             # Configuration, security, dependencies
│   │   ├── db/               # Database configuration
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   └── services/         # Business logic and AI services
│   │
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│
├── docs/
│
├── docker-compose.yml
├── postman_collection.json
└── README.md
```

---

## Database Schema

The application uses PostgreSQL with user-scoped relational data.

```text
Users
  │
  ├── Documents
  │      │
  │      ├── Document Chunks
  │      │
  │      └── Chat History
  │
  └── Integrations
```

### Main Tables

| Table             | Purpose                                                    |
| ----------------- | ---------------------------------------------------------- |
| `users`           | Application users                                          |
| `documents`       | Document metadata, extracted text, status and content hash |
| `document_chunks` | Chunked document text used for AI context                  |
| `integrations`    | User-specific OAuth integration data                       |
| `chat_history`    | Document-specific AI conversations                         |

---

# Local Development

## Prerequisites

Make sure the following are installed:

* Python 3.12+
* Node.js
* PostgreSQL
* Git

---

## Option A — Docker Compose

From the project root:

```bash
cp backend/.env.example backend/.env
```

Configure the required environment variables and then run:

```bash
docker compose up --build
```

The application will be available at:

```text
Frontend:  http://localhost:5173
API:       http://localhost:8000
API Docs:  http://localhost:8000/docs
```

---

## Option B — Native Development

### 1. Configure PostgreSQL

Create a PostgreSQL database named:

```text
docflow
```

Then configure `DATABASE_URL` in:

```text
backend/.env
```

---

### 2. Setup Backend

```bash
cd backend

python3 -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

pip install -r requirements.txt
```

Create the environment file:

```bash
cp .env.example .env
```

Start the backend:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

---

### 3. Setup Frontend

Open another terminal:

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# Environment Variables

Backend environment variables are documented in:

```text
backend/.env.example
```

Important variables include:

```env
DATABASE_URL=
JWT_SECRET=
CORS_ORIGINS=

MAX_FILE_SIZE_MB=

GROQ_API_KEY=
GROQ_MODEL=openai/gpt-oss-120b

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=

FRONTEND_URL=
```

The frontend uses:

```env
VITE_API_URL=
```

### Security

Never commit:

```text
.env
```

or any API keys, OAuth secrets, JWT secrets, or database credentials.

Provider secrets are used only by the backend and are never exposed to the browser.

---

# AI Document Q&A

DocFlow AI uses the **Groq API** for document-based question answering.

The backend retrieves relevant document chunks and provides them as context to the language model.

Current model:

```text
openai/gpt-oss-120b
```

The browser does not call the AI provider directly.

The request flow is:

```text
User Question
      ↓
FastAPI
      ↓
Document Ownership Check
      ↓
Document Chunks
      ↓
Groq API
      ↓
AI Answer
      ↓
Chat History
      ↓
Frontend
```

If the Groq API key is not configured, the application returns a clear configuration message instead of silently failing.

---

# Google Drive Integration

DocFlow AI supports importing documents directly from Google Drive.

### Flow

```text
User
  ↓
Google OAuth
  ↓
Google Drive API
  ↓
File Metadata
  ↓
PDF/DOCX Download
  ↓
Document Extraction
  ↓
Validation
  ↓
PostgreSQL
  ↓
AI Q&A
```

The integration currently supports PDF and DOCX files.

### Local OAuth Callback

For local development, configure the Google OAuth redirect URI as:

```text
http://localhost:8000/api/integrations/google/callback
```

The Google Drive API must be enabled in the associated Google Cloud project.

OAuth credentials should be stored only in the backend environment.

---

# SaaS Connector Architecture

DocFlow AI uses a reusable connector abstraction for external SaaS integrations.

The `BaseConnector` interface defines operations such as:

```text
authenticate()
list_files()
get_file_metadata()
download_file()
disconnect()
```

The Google Drive integration implements this interface through:

```text
GoogleDriveConnector
```

This design allows future integrations such as:

```text
Notion
Dropbox
OneDrive
Google Drive
```

to be added without changing the core document-processing pipeline.

---

# REST API

## Authentication

```text
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/users/me
```

## Documents

```text
POST   /api/documents/upload
GET    /api/documents
GET    /api/documents/{id}
DELETE /api/documents/{id}
POST   /api/documents/{id}/ask
GET    /api/documents/{id}/chat
```

## Integrations

```text
GET    /api/integrations
GET    /api/integrations/google/connect
GET    /api/integrations/google/callback
POST   /api/integrations/google/import
DELETE /api/integrations/google/disconnect
```

---

# API Documentation

FastAPI automatically provides interactive OpenAPI documentation.

Once the backend is running:

```text
http://localhost:8000/docs
```

The API can be tested directly through Swagger UI.

A Postman collection is also included:

```text
postman_collection.json
```

---

# Testing

Run the backend tests with:

```bash
cd backend

source .venv/bin/activate

pytest
```

The test suite covers core API functionality including:

* Health checks
* User registration
* Login
* Current-user authentication
* Protected document access

The architecture also supports extending the test suite with integration tests for document processing and external connectors.

---

# Error Handling

The API follows a consistent JSON error format:

```json
{
  "success": false,
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "Document was not found."
  }
}
```

The application handles common API failures including:

| Status | Meaning                   |
| ------ | ------------------------- |
| `401`  | Authentication required   |
| `404`  | Resource not found        |
| `409`  | Resource conflict         |
| `413`  | File too large            |
| `422`  | Validation error          |
| `502`  | External provider failure |
| `500`  | Unexpected server error   |

---

# Deployment

The project is structured for cloud deployment.

### Frontend

Recommended:

```text
Vercel
```

Configure:

```env
VITE_API_URL=https://your-backend-domain
```

### Backend

Compatible deployment options include:

```text
Render
Railway
```

The backend includes a Dockerfile for containerized deployment.

### Database

Recommended PostgreSQL providers:

```text
Neon
Supabase
```

Production deployment requires:

* Production `DATABASE_URL`
* Strong random `JWT_SECRET`
* Production CORS configuration
* Production Google OAuth redirect URI
* Secure provider credentials
* HTTPS-enabled frontend and backend

---

# Production Hardening Roadmap

The current project is deployment-ready, while the following improvements can be added for larger-scale production use:

* Encrypt OAuth refresh tokens using a managed KMS
* Move large-file processing to background workers
* Add Redis-based rate limiting
* Add distributed request IDs
* Store original documents in object storage such as S3/GCS
* Add embeddings and vector search for large document collections
* Add CI/CD with linting, type checking, tests and security scanning
* Add richer observability and audit logging

---

# Resume Positioning

### DocFlow AI — AI Document Integration Platform

**React, FastAPI, PostgreSQL, REST APIs, Groq, OAuth**

* Built a multi-user document processing platform with JWT authentication, REST APIs, PDF/DOCX extraction, PostgreSQL storage, and AI-powered document Q&A.
* Developed a reusable SaaS connector architecture for Google Drive ingestion, handling OAuth authentication, API integration, metadata retrieval, validation, and automated document processing.
* Implemented structured error handling, logging, automated testing, document chunking, and deployment-ready backend services.

---

# Project Highlights

```text
✓ Multi-user authentication
✓ JWT-based authorization
✓ PDF/DOCX processing
✓ PostgreSQL persistence
✓ Google Drive OAuth integration
✓ External API integration
✓ Reusable SaaS connector architecture
✓ AI-powered document Q&A
✓ Chat history
✓ Validation and duplicate detection
✓ Structured API errors
✓ Logging and debugging
✓ Automated backend tests
✓ Swagger / OpenAPI documentation
✓ Docker support
✓ Deployment-ready architecture
```

---

## License

This project is licensed under the **MIT License**.
