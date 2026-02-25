import os
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import OperationalError

app = FastAPI()

# 1. 환경 변수 및 DB URL 설정
DB_URL = os.getenv("DATABASE_URL")
WELCOME_MSG = os.getenv("APP_MESSAGE", "Hello, Welcome!")

# 핵심: DATABASE_URL이 없으면(테스트 환경) SQLite를, 있으면(배포 환경) PostgreSQL을 사용
if not DB_URL:
    # 테스트용 SQLite (파일 기반)
    DB_URL = "sqlite:///./test.db"
    engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
else:
    # 운영용 PostgreSQL
    engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. 데이터 모델 (방문 기록)
class Visit(Base):
    __tablename__ = "visits"
    id = Column(Integer, primary_key=True, index=True)
    visitor_name = Column(String)

# 서버 시작 시 테이블 자동 생성
Base.metadata.create_all(bind=engine)

# DB 세션 의존성 주입
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    # 방문 기록 저장
    new_visit = Visit(visitor_name="Guest")
    db.add(new_visit)
    db.commit()
    
    # 누적 방문 횟수 계산
    count = db.query(Visit).count()
    
    return {
        "secret_message": WELCOME_MSG,
        "total_visits": count,
        "database": "PostgreSQL" if "postgresql" in DB_URL else "SQLite (Test Mode)"
    }