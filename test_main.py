from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    # 1. 요청 보내기
    response = client.get("/")
    
    # 2. 상태 코드 확인
    assert response.status_code == 200
    
    # 3. 응답 구조 확인 (내용이 아니라 키 값이 존재하는지!)
    data = response.json()
    assert "secret_message" in data
    assert "total_visits" in data
    assert "database" in data
    
    # 4. 방문 횟수가 숫자인지 확인
    assert isinstance(data["total_visits"], int)