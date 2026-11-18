from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["classes"] == ["Favour", "Against", "None"]

def test_health():
    assert client.get("/health").status_code == 200

def test_feedback_validation():
    r = client.post("/feedback", json={"text":"test","corrected_label":"Maybe"})
    assert r.status_code == 422
