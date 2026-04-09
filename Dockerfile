# 1. 가볍고 최신인 Node 18 알핀 이미지 사용
FROM node:18-alpine

# 2. 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 파일 복사 및 설치
COPY package*.json ./
RUN npm install

# 4. 소스 코드 전체 복사
COPY . .

# 5. 앱이 사용하는 포트 번호 명시
EXPOSE 3000

# 6. 앱 실행 명령
CMD ["node", "app.js"]