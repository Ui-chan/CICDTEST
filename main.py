import os  # 시스템의 환경 변수(비밀번호 등)를 가져오기 위한 도구
from fastapi import FastAPI, Depends  # 웹 서버 구축 및 기능 연결 도구
from sqlalchemy import create_engine, Column, Integer, String  # DB 연결 및 표(Table) 설계 도구
from sqlalchemy.orm import sessionmaker, Session, declarative_base  # DB와 대화하기 위한 도구

# 1. FastAPI 인스턴스 생성: 우리 서버의 심장입니다.
app = FastAPI()

# 2. 환경 변수 읽기
# GitHub Secrets를 통해 주입될 값들을 가져옵니다.
DB_URL = os.getenv("DATABASE_URL")  # DB 주소 (아이디:비번@주소)
WELCOME_MSG = os.getenv("APP_MESSAGE", "Hello World!")  # 화면에 띄울 메시지

# 3. DB 엔진 설정 (하이브리드 모드)
# [논리] DATABASE_URL이 없으면(테스트 시) SQLite를 쓰고, 있으면(배포 시) PostgreSQL을 씁니다.
if not DB_URL:
    # 테스트용: 파일 하나로 작동하는 가벼운 DB
    DB_URL = "sqlite:///./test.db"
    engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
else:
    # 운영용: 실제 PostgreSQL 서버에 연결
    engine = create_engine(DB_URL)

# 4. DB 세션 및 베이스 설정
# SessionLocal: DB에 명령을 내릴 '창구'를 만듭니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base: 이 클래스를 상속받아야 나중에 DB 테이블로 인식됩니다.
Base = declarative_base()

# 5. DB 테이블 정의 (방문자 기록용)
class Visit(Base):
    __tablename__ = "visits"  # DB에 생성될 실제 테이블 이름
    id = Column(Integer, primary_key=True, index=True)  # 고유 번호
    visitor_name = Column(String)  # 방문자 이름

# 6. 테이블 자동 생성: 서버가 켜질 때 표가 없으면 새로 만듭니다.
Base.metadata.create_all(bind=engine)

# 7. DB 세션 의존성 함수: 안전하게 DB에 접속하고 볼일이 끝나면 연결을 끊습니다.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 8. 메인 API 엔드포인트: 사용자가 브라우저로 접속했을 때 실행됩니다.
@app.get("/")
def read_root(db: Session = Depends(get_db)):
    # 방문 기록을 하나 추가합니다.
    new_visit = Visit(visitor_name="Guest")
    db.add(new_visit)
    db.commit()  # 변경 사항 저장
    
    # 전체 방문자 수를 조회합니다.
    count = db.query(Visit).count()
    
    # 결과를 화면에 보여줍니다.
    return {
        "secret_message": WELCOME_MSG,
        "total_visits": count,
        "database_type": "PostgreSQL" if "postgresql" in DB_URL else "SQLite"
    } 