import os
from fastapi import FastAPI

app = FastAPI()

# 환경 변수 'APP_MESSAGE'를 읽어오고, 설정값이 없으면 기본 메시지를 출력합니다.
WELCOME_MSG = os.getenv("APP_MESSAGE", "Default Welcome Message")

@app.get("/")  # 'app.'을 붙여서 FastAPI 인스턴스와 연결 완료
def read_root():
    return {"message": WELCOME_MSG}