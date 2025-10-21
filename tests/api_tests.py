from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

def test_health_endpoint():
    """Verifica que /health responda correctamente"""
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}

def test_classify_smishing():
    """Verifica que un mensaje sospechoso se detecte como smishing"""
    body = {"message": "Tu cuenta será bloqueada http://falso.com"}
    res = client.post("/classify", json=body)
    assert res.status_code == 200
    data = res.json()
    assert data["label"] in ["smishing", "legit"]
    assert 0 <= data["score"] <= 1
