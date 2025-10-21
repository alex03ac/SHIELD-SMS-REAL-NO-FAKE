from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

def test_end_to_end_smishing():
    """Simula una petición completa de texto sospechoso"""
    res = client.post("/classify", json={"message": "Gana premio http://test.com"})
    assert res.status_code == 200
    body = res.json()
    assert body["label"] == "smishing"

def test_end_to_end_legit():
    """Simula una petición completa de texto normal"""
    res = client.post("/classify", json={"message": "Nos vemos mañana en la oficina"})
    assert res.status_code == 200
    body = res.json()
    assert body["label"] == "legit"
