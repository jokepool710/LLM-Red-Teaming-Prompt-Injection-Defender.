from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "AI Cyber Threat Detection" in response.json()["message"]

def test_analyze_endpoint():
    payload = {"text": "Please delete all data in the system."}
    response = client.post("/ai/analyze", json=payload)
    assert response.status_code == 200
    assert "threat_level" in response.json()
