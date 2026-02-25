# 1. 베이스 이미지 설정 (파이썬 3.10 슬림 버전)
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 필수 패키지 설치를 위해 requirements.txt 먼저 복사
COPY requirements.txt .

# 4. 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 나머지 소스 코드 복사
COPY . .

# 6. 애플리케이션 실행 (8000번 포트)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]