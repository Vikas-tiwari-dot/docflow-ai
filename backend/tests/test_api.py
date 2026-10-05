import os
os.environ["DATABASE_URL"]="sqlite:///./test_docflow.db"
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_register_login_me():
    email="test@example.com"
    r=client.post("/api/auth/register",json={"name":"Test User","email":email,"password":"password123"})
    assert r.status_code in (201,409)
    if r.status_code==201: token=r.json()["access_token"]
    else:
        token=client.post("/api/auth/login",json={"email":email,"password":"password123"}).json()["access_token"]
    assert client.get("/api/users/me",headers={"Authorization":f"Bearer {token}"}).status_code==200

def test_protected_documents():
    assert client.get("/api/documents").status_code==401

def test_health(): assert client.get("/api/health").json()["status"]=="ok"
