FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential gcc g++ libpq-dev python3-dev libffi-dev \
      libssl-dev libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p app/media

ENV PORT=8080
EXPOSE 8080
ENTRYPOINT ["uvicorn","app.main:app","--host","0.0.0.0","--port","8080"]
