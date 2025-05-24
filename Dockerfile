# 1) 베이스 이미지
FROM python:3.11-slim

# 2) 작업 디렉터리
WORKDIR /app

# 3) 시스템 패키지 설치
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

# 4) 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5) 애플리케이션 복사
COPY . .

# 5.1) 빈 media 폴더 생성 (StaticFiles 마운트 대비)
RUN mkdir -p app/media

# 6) 문서화용 포트 노출
EXPOSE 8080

# 7) 컨테이너 시작 (app/main.py __main__ 블록에서 PORT 읽음)
ENTRYPOINT ["python", "-m", "app.main"]
