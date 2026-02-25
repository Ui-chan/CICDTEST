import os
from fastapi import FastAPI

app = FastAPI()

# 환경 변수 'APP_MESSAGE'를 읽어오고, 없으면 기본값 출력
WELCOME_MSG = os.getenv("APP_MESSAGE", "Default Welcome Message")

@app.get("/")  # 이 부분에 'app.'이 꼭 들어가야 합니다!
def read_root():
    return {"message": WELCOME_MSG}