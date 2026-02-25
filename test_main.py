from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "secret_message" in data
    assert "total_visits" in data
    assert isinstance(data["total_visits"], int)