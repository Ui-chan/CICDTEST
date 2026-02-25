import os
from fastapi import FastAPI

app = FastAPI()

# 환경 변수 'APP_MESSAGE'를 읽어오고, 없으면 기본값 출력
WELCOME_MSG = os.getenv("APP_MESSAGE", "Default Welcome Message")

@get("/")
def read_root():
    return {"message": WELCOME_MSG}