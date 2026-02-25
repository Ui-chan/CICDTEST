import os
import time
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError

app = FastAPI()

# 1. 환경 변수 읽기
# 배포 시 GitHub Secrets에서 주입한 값들을 가져옵니다.
DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/dbname")
WELCOME_MSG = os.getenv("APP_MESSAGE", "Hello, welcome to my service!")

# 2. DB 연결 설정
# 실무 Tip: DB가 뜰 때까지 시간이 걸릴 수 있어, 연결 실패 시 재시도 로직을 넣기도 합니다.
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. 데이터 모델 정의 (방문 기록 저장용)
class Visit(Base):
    __tablename__ = "visits"
    id = Column(Integer, primary_key=True, index=True)
    visitor_name = Column(String)

# 서버 시작 시 테이블이 없으면 생성
# (실무에서는 Alembic 같은 마이그레이션 도구를 쓰지만, 지금은 자동 생성을 사용합니다)
try:
    Base.metadata.create_all(bind=engine)
except OperationalError:
    print("DB is not ready yet. Waiting...")

# DB 세션 관리 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    # 새로운 방문 기록 추가
    new_visit = Visit(visitor_name="Anonymous Guest")
    db.add(new_visit)
    db.commit()
    
    # 전체 방문 횟수 조회
    total_count = db.query(Visit).count()
    
    # 비밀 메시지와 방문 횟수를 함께 반환
    return {
        "secret_message": WELCOME_MSG,
        "total_visits": total_count,
        "status": "Connected to PostgreSQL"
    }