# DocFlow AI — AI Document Integration & Processing Platform

DocFlow AI is a production-oriented SaaS-style document processing platform that combines **document ingestion, SaaS integrations, structured data extraction, AI-powered document Q&A, authentication, and PostgreSQL persistence** into a single full-stack application.

The platform allows users to authenticate, upload PDF/DOCX documents through **Manage Documentation**, or connect **Google Drive** to import supported documents. DocFlow AI extracts and processes document content, stores document metadata and extracted text in PostgreSQL, and enables users to ask natural-language questions about their documents using **Groq-powered LLM inference**.

---

## Live Application

**Frontend:**
https://docflow-ai-three.vercel.app/

**Backend API:**
https://docflow-ai-boj1.onrender.com/

**API Health Check:**
https://docflow-ai-boj1.onrender.com/api/health

**API Documentation:**
https://docflow-ai-boj1.onrender.com/docs

---

# Architecture

```text
                         ┌─────────────────────┐
                         │        User         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                     ┌──────────────────────────┐
                     │ React + Vite + Tailwind  │
                     │        Frontend          │
                     │        Vercel            │
                     └────────────┬─────────────┘
                                  │ REST / JSON
                                  ▼
                     ┌──────────────────────────┐
                     │        FastAPI           │
                     │        Backend           │
                     │         Render           │
                     └──────┬────────┬──────────┘
                            │        │
              ┌─────────────┘        └──────────────┐
              ▼                                     ▼
     ┌─────────────────┐                   ┌─────────────────┐
     │   PostgreSQL    │                   │   Google Drive  │
     │      Neon       │                   │      OAuth      │
     └─────────────────┘                   └────────┬────────┘
                                                    │
                                                    ▼
                                           ┌─────────────────┐
                                           │ PDF / DOCX      │
                                           │ Processing      │
                                           └────────┬────────┘
                                                    │
                                                    ▼
                                           ┌─────────────────┐
                                           │ Groq LLM        │
                                           │ GPT-OSS-120B    │
                                           └─────────────────┘
```

---

# Core Document Pipeline

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

# How to Use

## 1. Sign In / Register

Create an account or sign in using the authentication system.

DocFlow AI uses JWT-based authentication to protect user-specific documents and application resources.

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

You can upload your documents directly from your device.

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

After uploading, DocFlow AI processes the document, extracts its content, stores the document metadata and extracted text, and makes it available in the document library.

Users can then open the document and ask natural-language questions about its content.

---

## 3. Connect Google Drive

Instead of manually uploading documents, users can connect their **Google Drive** through the Google Drive integration.

```text
Connect Google Drive
        ↓
Google OAuth Authorization
        ↓
Access Connected Drive
        ↓
Import Supported Documents
        ↓
PDF / DOCX Processing
        ↓
PostgreSQL Storage
        ↓
AI Q&A
```

The Google Drive integration provides a convenient way to import supported documents from a connected Drive without repeatedly uploading files manually.

### Google Drive Workflow

```text
User
  ↓
Connect Google Drive
  ↓
Google OAuth
  ↓
Drive Authorization
  ↓
Document Import
  ↓
Text Extraction
  ↓
Database Storage
  ↓
AI Document Q&A
```

---

## 4. Ask Questions About Documents

Once a document has been uploaded or imported, users can open the document and ask questions about its content.

Example:

```text
Question:
What is this document about?

Answer:
The document is a nomination letter from the college principal,
nominating a team to participate in the Smart India Hackathon 2026.
```

The AI response is generated using the document content provided as context to the Groq-powered LLM.

---

# Features

## Authentication

* JWT-based authentication
* Secure password hashing using bcrypt
* User registration and login
* Protected API routes
* Token-based authentication
* User-specific document access

## Document Management

* Upload PDF documents
* Upload DOCX documents
* PDF text extraction
* DOCX text extraction
* Document metadata storage
* Extracted text persistence
* Document listing and retrieval
* Document-specific AI Q&A

## Google Drive Integration

* Google OAuth 2.0 authentication
* Google Drive integration
* Import supported documents
* User-specific connector authorization
* Document ingestion pipeline
* Duplicate-aware document importing

## AI Document Q&A

* Natural-language document queries
* Groq-powered LLM inference
* Document-aware responses
* Context-based question answering
* Document-specific conversations
* AI provider abstraction for future model changes

## Backend Engineering

* RESTful API architecture
* FastAPI
* Pydantic validation
* SQLAlchemy ORM
* PostgreSQL
* JWT authentication
* Structured HTTP errors
* Environment-based configuration
* Health-check endpoint
* OpenAPI/Swagger documentation

## Testing & Reliability

* Pytest-based backend testing
* API testing with Postman
* Regression testing
* Edge-case validation
* Authentication testing
* Document-processing validation
* Error handling
* Production logging

---

# Tech Stack

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

# Project Structure

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
│
├── .gitignore
├── README.md
└── LICENSE
```

---

# Database Architecture

The application uses PostgreSQL for persistent application data.

Core relationships:

```text
users
  │
  ├── documents
  │
  ├── conversations
  │
  └── integrations
```

## Users

Stores:

* User identity
* Email
* Password hash
* Account metadata

## Documents

Stores:

* Document name
* File type
* Source
* Extracted text
* Metadata
* Owner/user relationship
* Timestamps

## Conversations

Stores document-related AI interactions and associated metadata where applicable.

## Integrations

Stores information required to manage external service integrations for authenticated users.

---

# Local Development

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

**Never commit `.env` or API keys to GitHub.**

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

Swagger documentation:

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

# Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
```

Create:

```text
frontend/.env
```

Example:

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

# Environment Variables

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

# AI Document Q&A

DocFlow AI uses Groq for AI-powered document question answering.

Current model:

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

The system is designed to answer questions using the available document context.

Example:

```text
Document:
Smart India Hackathon nomination letter

Question:
What is this document about?

Answer:
The document is a nomination letter from the college principal,
nominating a team to participate in the Smart India Hackathon 2026.
```

The AI layer is separated from the core document-processing pipeline, making it possible to replace or extend the underlying model provider in the future.

---

# Google Drive Integration

DocFlow AI uses Google OAuth 2.0 for Google Drive integration.

## Development Callback

```text
http://localhost:8000/api/integrations/google/callback
```

## Production Callback

```text
https://docflow-ai-boj1.onrender.com/api/integrations/google/callback
```

## Production Frontend

```text
https://docflow-ai-three.vercel.app
```

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

---

# SaaS Connector Architecture

DocFlow AI is structured so that additional external integrations can be added independently.

Current connector:

```text
Google Drive
```

Potential future connectors:

```text
Google Drive
     │
     ├── Dropbox
     ├── OneDrive
     ├── Notion
     ├── Slack
     └── Other SaaS APIs
```

General connector architecture:

```text
OAuth / API Authentication
          ↓
External Service API
          ↓
Document Discovery
          ↓
Data Normalization
          ↓
Document Processing
          ↓
PostgreSQL
          ↓
AI Q&A
```

This separation makes the application easier to extend with additional SaaS integrations.

---

# REST API

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

# API Documentation

FastAPI automatically generates OpenAPI documentation.

Swagger UI:

```text
https://docflow-ai-boj1.onrender.com/docs
```

OpenAPI specification:

```text
https://docflow-ai-boj1.onrender.com/openapi.json
```

The API documentation can be used to inspect endpoints, request schemas, response formats, and authentication requirements.

---

# Testing

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

# Error Handling

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

Production logs can be used to diagnose backend errors and deployment issues.

---

# Deployment

## Frontend — Vercel

The React/Vite frontend is deployed on Vercel.

Production URL:

```text
https://docflow-ai-three.vercel.app/
```

Production environment variable:

```env
VITE_API_URL=https://docflow-ai-boj1.onrender.com
```

The frontend uses `VITE_API_URL` to communicate with the production FastAPI backend.

---

## Backend — Render

The FastAPI backend is deployed on Render.

Production URL:

```text
https://docflow-ai-boj1.onrender.com/
```

The backend runs using the project's Docker configuration.

---

## Database — Neon

Production PostgreSQL is hosted using Neon.

The backend connects through:

```env
DATABASE_URL=<production-postgresql-url>
```

Database credentials are stored as deployment environment variables and are not committed to the repository.

---

# Production Architecture

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

# Security Considerations

The application follows several security practices:

* Passwords are stored using bcrypt hashing.
* JWT authentication is used for protected endpoints.
* Secrets are provided through environment variables.
* Production secrets are not committed to Git.
* CORS is configured for the production frontend.
* User-specific resources are protected through authentication.
* OAuth credentials are kept server-side.
* Database credentials are stored as deployment secrets.

For a larger production deployment, additional controls can be introduced around:

* Token encryption
* Secret rotation
* Rate limiting
* Audit logging
* Monitoring
* Automated security scanning
* Role-based access control

---

# Production Hardening Roadmap

Potential future improvements include:

* Refresh-token rotation
* OAuth token encryption at rest
* Redis-based caching
* Rate limiting
* Background document processing
* Celery / task queues
* Object storage for uploaded files
* Vector database integration
* Semantic search
* Retrieval-Augmented Generation (RAG)
* Document chunk indexing
* Observability and distributed tracing
* Automated CI/CD pipelines
* Automated security scanning
* Role-based access control
* Audit logs
* Multi-tenant organization support
* Subscription and billing infrastructure

---

# Engineering Highlights

DocFlow AI demonstrates practical experience across:

* Full-stack application development
* REST API design
* Backend engineering with FastAPI
* PostgreSQL database design
* Authentication and authorization
* OAuth 2.0 integrations
* External API integration
* PDF/DOCX data extraction
* AI/LLM integration
* Error handling and debugging
* Automated testing
* Production deployment
* Cloud-based application architecture

The project demonstrates how a document-centric SaaS platform can accept documents through direct uploads or external integrations, process unstructured document content, persist the resulting data, and provide an AI-powered interface for querying that information.

---

# Resume Positioning

**DocFlow AI — AI Document Integration Platform**
`React, FastAPI, PostgreSQL, REST APIs, Groq, OAuth`

> Built a production-oriented document processing platform with JWT authentication, Google Drive OAuth integration, PDF/DOCX extraction, PostgreSQL persistence, REST APIs, and Groq-powered document Q&A; deployed the frontend on Vercel and backend on Render with production PostgreSQL on Neon.

---

# License

This project is licensed under the **MIT License**.
