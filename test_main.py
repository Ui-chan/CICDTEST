from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    
    # 메시지 내용이 무엇이든 'message'라는 키가 들어있는지 확인합니다.
    data = response.json()
    assert "message" in data
    assert len(data["message"]) > 0  # 메시지가 비어있지는 않은지 확인