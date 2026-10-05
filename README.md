# DocFlow AI — AI Document Integration & Processing Platform

DocFlow AI is a production-oriented SaaS-style document pipeline demonstrating backend engineering and data-integration skills: JWT authentication, REST APIs, PDF/DOCX extraction, PostgreSQL, reusable SaaS connectors, structured validation/errors, logging, testing and Gemini-powered document Q&A.

## Architecture

```text
User
  ↓
React + Vite + Tailwind
  ↓ REST / JSON
FastAPI API
  ├── JWT Authentication
  ├── Document Service → PDF/DOCX extraction → normalization → chunks
  ├── Integration Service → Google Drive OAuth → Drive REST API → import
  ├── AI Service → Gemini
  └── SQLAlchemy
          ↓
      PostgreSQL
```

The requested pipeline is: **External SaaS/API → Authentication → Data Extraction → Validation → Processing → Database → AI → REST API → Frontend**. fileciteturn0file0L63-L67

## Features

- Multi-user registration/login with bcrypt password hashing and JWT access tokens.
- User-scoped document access and deletion.
- PDF/DOCX upload with type/size/empty-file/duplicate validation.
- Extraction, normalization, SHA-256 duplicate detection, status tracking and chunking.
- AI Q&A endpoint: `POST /api/documents/{document_id}/ask`.
- Chat history stored in PostgreSQL.
- Google Drive OAuth connector with metadata retrieval, file download and import.
- Reusable `BaseConnector` abstraction for adding other SaaS sources.
- Consistent JSON errors, centralized exception handling and structured logging.
- FastAPI OpenAPI docs at `/docs`.
- Pytest backend tests and Postman collection.
- Docker Compose for local PostgreSQL + backend + frontend.

## Project structure

```text
docflow-ai/
├── backend/
│   ├── app/
│   │   ├── api/              # HTTP controllers/routes
│   │   ├── connectors/       # SaaS connector abstraction + Google Drive
│   │   ├── core/             # config, security, dependencies, errors
│   │   ├── db/               # SQLAlchemy session/init
│   │   ├── models/           # relational models
│   │   ├── schemas/           # Pydantic request/response models
│   │   └── services/          # processing + AI business logic
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
├── docs/
├── docker-compose.yml
├── postman_collection.json
└── README.md
```

## Database schema

- `users` → owns documents and integrations.
- `documents` → metadata, status, extracted text and content hash.
- `document_chunks` → chunked text for efficient AI context.
- `integrations` → provider credentials/tokens per user.
- `chat_history` → document-specific AI conversations.

The requested relational relationships are User → Documents, User → Integrations, Document → Chunks, and Document → Chat History. fileciteturn0file0L351-L375

## Local setup

### Option A — Docker Compose

```bash
cp backend/.env.example backend/.env
# Put GEMINI_API_KEY / Google OAuth values in the root .env if needed.
docker compose up --build
```

Frontend: http://localhost:5173  
API: http://localhost:8000  
API docs: http://localhost:8000/docs

### Option B — Native development

1. Start PostgreSQL and create a database named `docflow`.
2. Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

3. Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Environment variables

Backend variables are documented in `backend/.env.example`. Important values:

- `DATABASE_URL`
- `JWT_SECRET`
- `CORS_ORIGINS`
- `MAX_FILE_SIZE_MB`
- `GEMINI_API_KEY`
- `GEMINI_MODEL`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REDIRECT_URI`
- `FRONTEND_URL`

Frontend uses `VITE_API_URL`. Never put Gemini or Google client secrets in frontend variables.

## Google Drive setup

Create a Google OAuth web application in Google Cloud, enable the Google Drive API, and register the exact callback URL:

`http://localhost:8000/api/integrations/google/callback`

Set the client ID/secret in the backend environment. The connector uses Drive read-only scope, lists PDF/DOCX files, downloads them, extracts text and persists them through the same document pipeline. This follows the requested connector flow of OAuth → Drive REST API → metadata → download → extraction → PostgreSQL → AI. fileciteturn0file0L202-L241

## Gemini setup

Set `GEMINI_API_KEY`. The browser never calls Gemini. The backend AI service builds a prompt from document chunks and calls Gemini server-side.

Without a Gemini key, local document upload/search still works and the Q&A endpoint returns a clear configuration message rather than silently failing.

## Testing

```bash
cd backend
pytest
```

Tests cover health, registration/login/me and protected document access. The API design also includes validation and connector error paths suitable for extension with integration tests.

## REST endpoints

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/users/me`
- `POST /api/documents/upload`
- `GET /api/documents`
- `GET /api/documents/{id}`
- `DELETE /api/documents/{id}`
- `POST /api/documents/{id}/ask`
- `GET /api/documents/{id}/chat`
- `GET /api/integrations`
- `GET /api/integrations/google/connect`
- `GET /api/integrations/google/callback`
- `POST /api/integrations/google/import`
- `DELETE /api/integrations/google/disconnect`

## Deployment

- Frontend: Vercel, with `VITE_API_URL` pointing to the deployed API.
- Backend: Render/Railway using the included Dockerfile.
- Database: Neon/Supabase PostgreSQL using `DATABASE_URL`.
- Set production CORS and Google callback URL to the deployed domains.
- Set a long random `JWT_SECRET` and never commit `.env` or provider secrets.

## Error contract

Application errors use a consistent shape:

```json
{
  "success": false,
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "Document was not found."
  }
}
```

The project handles validation (422), authentication (401), authorization/not-found (404), conflicts (409), oversized files (413), upstream provider failures (502), and unexpected server errors (500).

## SaaS connector architecture

`BaseConnector` defines `authenticate`, `list_files`, `get_file_metadata`, `download_file`, and `disconnect`. `GoogleDriveConnector` implements the contract. A future Notion/Dropbox/OneDrive connector can implement the same interface without changing document-processing business logic. This is the requested reusable connector architecture. fileciteturn0file0L247-L266

## Production hardening roadmap

- Encrypt OAuth refresh tokens at rest with a managed KMS.
- Move large-file processing to a background queue (Celery/RQ/Cloud Tasks).
- Add Redis rate limiting and distributed request IDs.
- Add object storage (S3/GCS) for originals instead of only storing extracted text.
- Add semantic embeddings/vector search for larger documents.
- Add CI with lint/type/test/security checks.
- Add richer observability and audit logs.

## Resume positioning

**DocFlow AI — AI Document Integration Platform | React, FastAPI, PostgreSQL, REST APIs, Gemini, OAuth**

- Built a multi-user document processing platform with JWT authentication, REST APIs, PDF/DOCX extraction, PostgreSQL storage, and AI-powered document Q&A.
- Developed a reusable SaaS connector architecture for external document ingestion, handling OAuth authentication, API calls, JSON parsing, validation, and automated data processing.
- Implemented automated testing, structured error handling, logging, and deployment-ready backend services.

These bullets match the intended positioning in the supplied project brief. fileciteturn0file0L593-L604

## macOS setup note
If `python` is not available on macOS, use `python3` to create the virtual environment:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The PostgreSQL driver uses a compatible `psycopg[binary]` range rather than pinning the older 3.2.6 binary wheel, which is unavailable on some newer Python/macOS combinations.
