# DocFlow AI — AI Document Integration & Processing Platform

DocFlow AI is a production-oriented SaaS-style document processing platform that combines **document ingestion, SaaS integrations, structured data extraction, AI-powered document Q&A, authentication, and PostgreSQL persistence** into a single full-stack application.

The platform allows users to authenticate, import documents from Google Drive, extract text from PDF/DOCX files, store document metadata and content in PostgreSQL, and ask natural-language questions about their documents using **Groq-powered LLM inference**.

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

## Architecture

```text
                         ┌─────────────────────┐
                         │       User          │
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
                     │       Backend            │
                     │         Render           │
                     └──────┬───────┬───────────┘
                            │       │
              ┌─────────────┘       └──────────────┐
              ▼                                    ▼
     ┌─────────────────┐                  ┌─────────────────┐
     │   PostgreSQL    │                  │   Google Drive  │
     │      Neon       │                  │      OAuth      │
     └─────────────────┘                  └────────┬────────┘
                                                   │
                                                   ▼
                                          ┌─────────────────┐
                                          │ PDF / DOCX      │
                                          │ Extraction      │
                                          └────────┬────────┘
                                                   │
                                                   ▼
                                          ┌─────────────────┐
                                          │ Groq LLM        │
                                          │ GPT-OSS-120B    │
                                          └─────────────────┘
```

---

# Core Pipeline

```text
User Authentication
        ↓
Google Drive OAuth
        ↓
Document Import
        ↓
PDF / DOCX Text Extraction
        ↓
Document Storage
        ↓
Text Chunking / Context Preparation
        ↓
Groq LLM
        ↓
AI-powered Document Q&A
        ↓
Conversation / Query History
```

---

# Features

## Authentication

* JWT-based authentication
* Secure password hashing using bcrypt
* User registration and login
* Protected API routes
* Token-based session handling
* User-specific document access

## Document Processing

* PDF text extraction using `pypdf`
* DOCX text extraction using `python-docx`
* Document metadata storage
* Persistent document content
* Document listing and retrieval
* Structured error handling

## Google Drive Integration

* Google OAuth 2.0 authentication
* Google Drive document discovery
* Import documents directly from Drive
* User-specific connector authorization
* Automatic document ingestion
* Duplicate-aware document importing

## AI Document Q&A

Users can ask natural-language questions about imported documents.

Example:

```text
Question:
What is this document about?

Answer:
The document is a nomination letter from the college principal,
nominating a team to participate in the Smart India Hackathon 2026.
```

The AI pipeline:

```text
Document
   ↓
Text Extraction
   ↓
Context Preparation
   ↓
Relevant Document Content
   ↓
Groq LLM
   ↓
Natural Language Answer
```

The model is instructed to answer based on the supplied document context rather than relying on unrelated external information.

## API & Backend Engineering

* RESTful API architecture
* FastAPI
* Pydantic validation
* SQLAlchemy ORM
* PostgreSQL
* JWT authentication
* Structured HTTP error responses
* Environment-based configuration
* Health-check endpoint
* API documentation through OpenAPI/Swagger

## Testing & Reliability

* Pytest-based backend testing
* API testing with Postman
* Regression testing
* Edge-case validation
* Authentication testing
* Document-processing validation
* Error and exception handling
* Logging for debugging and production diagnosis

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

# Database Schema

The application uses PostgreSQL for persistent storage.

Core entities include:

```text
users
  │
  ├── documents
  │      │
  │      └── document content / metadata
  │
  ├── conversations
  │
  └── OAuth / integration credentials
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
* Source
* File type
* Extracted text
* Metadata
* Owner/user relationship
* Timestamps

### Conversations / Queries

Stores document-related AI interactions and associated metadata where applicable.

---

# Local Development

## 1. Clone the repository

```bash
git clone https://github.com/Vikas-tiwari-dot/docflow-ai.git
cd docflow-ai
```

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

## 3. Configure Environment Variables

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

Start the development server:

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

# AI Q&A

DocFlow AI integrates Groq for document question answering.

Current model:

```text
openai/gpt-oss-120b
```

The backend prepares document content as context before sending the request to the LLM.

Conceptually:

```text
User Question
      +
Document Context
      ↓
Groq API
      ↓
AI Answer
```

This architecture allows the AI layer to remain independent from the document storage and API layers.

The AI provider can also be replaced in the future without redesigning the complete application.

---

# Google Drive Integration

The Google Drive integration uses OAuth 2.0.

Development callback:

```text
http://localhost:8000/api/integrations/google/callback
```

Production callback:

```text
https://docflow-ai-boj1.onrender.com/api/integrations/google/callback
```

Production frontend origin:

```text
https://docflow-ai-three.vercel.app
```

The integration flow is:

```text
User
 ↓
Connect Google Drive
 ↓
Google OAuth
 ↓
Authorization
 ↓
OAuth Callback
 ↓
Backend Token Handling
 ↓
Google Drive API
 ↓
Document Import
 ↓
PDF/DOCX Extraction
 ↓
PostgreSQL
```

---

# SaaS Connector Architecture

The application is structured so that external integrations can be extended independently.

Current connector:

```text
Google Drive
```

Future connectors can include:

```text
Google Drive
    │
    ├── Dropbox
    ├── OneDrive
    ├── Notion
    ├── Slack
    └── Other SaaS APIs
```

A connector can follow the general pattern:

```text
OAuth / API Authentication
        ↓
External API
        ↓
Document Discovery
        ↓
Normalization
        ↓
Document Processing Pipeline
        ↓
Database
```

This separation makes the system easier to extend as additional SaaS integrations are added.

---

# REST API

Representative API endpoints include:

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

Run backend tests with:

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

Examples:

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

Examples of application-level handling include:

* Duplicate user registration
* Invalid credentials
* Missing documents
* Invalid document formats
* OAuth configuration errors
* External API failures
* AI service failures
* Database failures

Production logs are used to diagnose backend errors and deployment issues.

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

The frontend is configured to use the production backend through `VITE_API_URL`.

## Backend — Render

The FastAPI backend is deployed on Render.

Production URL:

```text
https://docflow-ai-boj1.onrender.com/
```

The backend runs using the project's Docker configuration.

## Database — Neon

Production PostgreSQL is hosted using Neon.

The backend connects through:

```env
DATABASE_URL=<production-postgresql-url>
```

Database credentials are stored as deployment environment variables and are not committed to the repository.

---

# Production Configuration

The production architecture is:

```text
                 Internet
                    │
                    ▼
          ┌──────────────────┐
          │      Vercel      │
          │ React Frontend   │
          └────────┬─────────┘
                   │ HTTPS
                   ▼
          ┌──────────────────┐
          │      Render      │
          │ FastAPI Backend  │
          └─────┬─────┬──────┘
                │     │
        ┌───────┘     └──────────┐
        ▼                        ▼
 ┌─────────────┐          ┌──────────────┐
 │    Neon     │          │    Groq      │
 │ PostgreSQL  │          │     LLM      │
 └─────────────┘          └──────────────┘
                │
                ▼
        ┌──────────────┐
        │ Google Drive │
        │    OAuth     │
        └──────────────┘
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

For a production-scale SaaS deployment, additional controls can be added around token encryption, rate limiting, audit logging, secret rotation, monitoring, and automated security scanning.

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

The project was designed to demonstrate how a document-centric SaaS product can connect external data sources, normalize unstructured documents, persist structured information, and expose an AI-powered interface for querying that information.

---

# Resume Positioning

**DocFlow AI — AI Document Integration Platform**
`React, FastAPI, PostgreSQL, REST APIs, Groq, OAuth`

> Built a production-oriented document processing platform with JWT authentication, Google Drive OAuth integration, PDF/DOCX extraction, PostgreSQL persistence, REST APIs, and Groq-powered document Q&A; deployed the frontend on Vercel and backend on Render with production PostgreSQL on Neon.

---

# License

This project is licensed under the **MIT License**.
