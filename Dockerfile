FROM python:3.10-slim

WORKDIR /app

# 시스템 패키지 설치 (konlpy 의존성)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 환경 변수 설정
ENV PYTHONPATH=/app
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 