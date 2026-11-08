"""
API tests for DocFlow AI (FastAPI).

PLACE THIS FILE AT:  backend/tests/test_docflow.py

RUN (from the backend/ folder, venv active):
    python -m pytest tests/test_docflow.py -v
    python -m pytest tests/test_docflow.py --cov=app --cov-report=term-missing

!! Ye tests random test users aur documents banate hain. Agar backend/.env ka
DATABASE_URL asli (Neon / production) database par point karta hai, to wahan test
data jayega. Local test database use karo (neeche TEST_DATABASE_URL).
"""
import io
import os
import uuid

import pytest

# =============================== CONFIG ===============================
# Example: "postgresql://user:pass@localhost:5432/docflow_test". Ye app import se PEHLE set hona chahiye.
TEST_DATABASE_URL = None
if TEST_DATABASE_URL:
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402

HEALTH_URL = "/api/health"
REGISTER_URL = "/api/auth/register"
LOGIN_URL = "/api/auth/login"
REGISTER_EXTRA = {"name": "Test User"}
TOKEN_KEY = "access_token"

DOCS_LIST_URL = "/api/documents"
UPLOAD_URL = "/api/documents/upload"
UPLOAD_FILE_FIELD = "file"        # documents.py mein upload ke parameter ka naam; alag ho to badlo
DOC_DETAIL_URL = "/api/documents/{id}"
ASK_URL = "/api/documents/{id}/ask"
CHAT_HISTORY_URL = "/api/documents/{id}/chat"
GOOGLE_CONNECT_URL = "/api/integrations/google/connect"

# AI test ke liye: wo function jo Groq ko call karta hai, jaise "app.api.documents.generate_answer".
# Jab tak None hai, test_18 skip hoga.
AI_FUNCTION_PATH = None
# ======================================================================

client = TestClient(app)
PASSWORD = "StrongPass#123"
NONEXISTENT_ID = 999999999


# ------------------------------- helpers -------------------------------
def unique_email():
    return f"test_{uuid.uuid4().hex[:10]}@testmail.com"


def register(email, password=PASSWORD):
    body = {"email": email, "password": password, **REGISTER_EXTRA}
    return client.post(REGISTER_URL, json=body)


def login(email, password=PASSWORD):
    return client.post(LOGIN_URL, json={"email": email, "password": password})


def auth_headers():
    email = unique_email()
    reg = register(email)
    assert reg.status_code in (200, 201), f"Register fail: {reg.status_code} {reg.text}"
    resp = login(email)
    assert resp.status_code == 200, f"Login fail: {resp.status_code} {resp.text}"
    return {"Authorization": f"Bearer {resp.json()[TOKEN_KEY]}"}


def make_pdf_bytes(text="DocFlow test document about invoices."):
    from reportlab.pdfgen import canvas

    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    c.drawString(72, 750, text)
    c.save()
    return buf.getvalue()


def make_docx_bytes(text="DocFlow test document about invoices."):
    import docx

    buf = io.BytesIO()
    d = docx.Document()
    d.add_paragraph(text)
    d.save(buf)
    return buf.getvalue()


def upload(headers, filename, content, content_type):
    return client.post(
        UPLOAD_URL,
        files={UPLOAD_FILE_FIELD: (filename, content, content_type)},
        headers=headers,
    )


def upload_pdf(headers):
    resp = upload(headers, "sample.pdf", make_pdf_bytes(), "application/pdf")
    assert resp.status_code == 201, f"Upload fail: {resp.status_code} {resp.text}"
    return resp.json()["id"]


# ================================ HEALTH ================================
def test_01_health_check_returns_ok():
    resp = client.get(HEALTH_URL)
    assert resp.status_code == 200
    assert resp.json().get("status") == "ok"


# ============================ AUTHENTICATION ============================
def test_02_login_success_returns_token():
    email = unique_email()
    register(email)
    resp = login(email)
    assert resp.status_code == 200
    assert TOKEN_KEY in resp.json()


def test_03_login_wrong_password_rejected():
    email = unique_email()
    assert register(email).status_code in (200, 201)
    resp = login(email, "WrongPassword!1")
    assert resp.status_code in (400, 401, 403)


def test_04_register_new_user_returns_token():
    resp = register(unique_email())
    assert resp.status_code == 201, resp.text
    assert TOKEN_KEY in resp.json()


def test_05_register_duplicate_email_rejected():
    email = unique_email()
    assert register(email).status_code in (200, 201)
    resp = register(email)
    assert resp.status_code in (400, 409, 422)


def test_06_protected_endpoint_without_token_rejected():
    resp = client.get(DOCS_LIST_URL)
    assert resp.status_code in (401, 403)


def test_07_tampered_token_rejected():
    resp = client.get(DOCS_LIST_URL, headers={"Authorization": "Bearer not.a.valid.token"})
    assert resp.status_code in (401, 403)


# ========================= UPLOAD AND EXTRACTION =========================
def test_08_valid_pdf_upload_succeeds():
    headers = auth_headers()
    resp = upload(headers, "sample.pdf", make_pdf_bytes(), "application/pdf")
    assert resp.status_code == 201, resp.text
    assert resp.json()["filename"] == "sample.pdf"


def test_09_valid_docx_upload_succeeds():
    headers = auth_headers()
    resp = upload(
        headers,
        "sample.docx",
        make_docx_bytes(),
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    assert resp.status_code == 201, resp.text


def test_10_unsupported_file_type_rejected():
    headers = auth_headers()
    resp = upload(headers, "malware.exe", b"MZ fake binary", "application/octet-stream")
    assert resp.status_code in (400, 415, 422)


def test_11_empty_pdf_gives_client_error_not_crash():
    headers = auth_headers()
    resp = upload(headers, "broken.pdf", b"", "application/pdf")
    assert resp.status_code in (400, 415, 422)  # 500 nahi aana chahiye


# ========================= DOCUMENT MANAGEMENT =========================
def test_12_uploaded_document_appears_in_list():
    headers = auth_headers()
    doc_id = upload_pdf(headers)
    resp = client.get(DOCS_LIST_URL, headers=headers)
    assert resp.status_code == 200
    assert doc_id in [d["id"] for d in resp.json()]


def test_13_owner_can_fetch_document_with_extracted_text():
    headers = auth_headers()
    doc_id = upload_pdf(headers)
    resp = client.get(DOC_DETAIL_URL.format(id=doc_id), headers=headers)
    assert resp.status_code == 200
    assert "extracted_text" in resp.json()


def test_14_user_cannot_access_another_users_document():
    owner = auth_headers()
    other = auth_headers()
    doc_id = upload_pdf(owner)
    resp = client.get(DOC_DETAIL_URL.format(id=doc_id), headers=other)
    assert resp.status_code in (403, 404)


def test_15_deleted_document_returns_404_afterwards():
    headers = auth_headers()
    doc_id = upload_pdf(headers)
    deleted = client.delete(DOC_DETAIL_URL.format(id=doc_id), headers=headers)
    assert deleted.status_code in (200, 204)
    after = client.get(DOC_DETAIL_URL.format(id=doc_id), headers=headers)
    assert after.status_code == 404


def test_16_user_cannot_delete_another_users_document():
    owner = auth_headers()
    other = auth_headers()
    doc_id = upload_pdf(owner)
    resp = client.delete(DOC_DETAIL_URL.format(id=doc_id), headers=other)
    assert resp.status_code in (403, 404)
    # Owner ka document abhi bhi maujood hona chahiye
    still_there = client.get(DOC_DETAIL_URL.format(id=doc_id), headers=owner)
    assert still_there.status_code == 200


# =========================== AI Q&A (ASK / CHAT) ===========================
def test_17_ask_without_question_returns_validation_error():
    headers = auth_headers()
    doc_id = upload_pdf(headers)
    resp = client.post(ASK_URL.format(id=doc_id), json={}, headers=headers)  # AI call nahi hota
    assert resp.status_code == 422


def test_18_ask_on_nonexistent_document_returns_404():
    headers = auth_headers()
    resp = client.post(ASK_URL.format(id=NONEXISTENT_ID), json={"question": "Hello?"}, headers=headers)
    assert resp.status_code == 404


def test_19_ask_returns_answer_and_saves_chat_history_with_ai_mocked(monkeypatch):
    """Groq ko mock karta hai taaki asli API call na ho. AI_FUNCTION_PATH set karo (config)."""
    if AI_FUNCTION_PATH is None:
        pytest.skip("AI_FUNCTION_PATH set karo, tab ye test chalega")

    monkeypatch.setattr(AI_FUNCTION_PATH, lambda *a, **k: "Mocked answer")
    headers = auth_headers()
    doc_id = upload_pdf(headers)
    resp = client.post(
        ASK_URL.format(id=doc_id), json={"question": "What is this document about?"}, headers=headers
    )
    assert resp.status_code == 200
    assert resp.json()["answer"] == "Mocked answer"

    history = client.get(CHAT_HISTORY_URL.format(id=doc_id), headers=headers)
    assert history.status_code == 200
    assert len(history.json()) == 1


# ============================ GOOGLE DRIVE ============================
def test_20_google_connect_requires_authentication():
    resp = client.get(GOOGLE_CONNECT_URL)
    assert resp.status_code in (401, 403)