# 1) 베이스 이미지
FROM python:3.11-slim

# 2) 작업 디렉터리
WORKDIR /app

# 3) 시스템 패키지 설치: 빌드 도구, libpq, SSL, zlib, libffi, JPEG 등
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      gcc \
      g++ \
      libpq-dev \
      python3-dev \
      libffi-dev \
      libssl-dev \
      libxml2-dev \
      libxslt1-dev \
      zlib1g-dev \
      libjpeg-dev && \
    rm -rf /var/lib/apt/lists/*

# 4) Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5) 애플리케이션 코드 복사
COPY . .

# 6) 문서화용 포트 노출 (명시적)
EXPOSE 8080

# 7) 컨테이너 시작
#    app/main.py 의 __main__ 블록이 PORT 환경변수를 읽어 uvicorn을 실행합니다.
ENTRYPOINT ["python", "-m", "app.main"]
