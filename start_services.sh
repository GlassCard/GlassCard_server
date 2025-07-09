#!/bin/bash

echo "GlassCard 서비스를 시작합니다..."

# FastAPI 서버 백그라운드에서 실행
echo "FastAPI 서버를 시작합니다..."
python main.py &
FASTAPI_PID=$!

# 잠시 대기
sleep 3

# Nginx 시작
echo "Nginx를 시작합니다..."
nginx -c $(pwd)/nginx.conf

echo "서비스가 시작되었습니다!"
echo "FastAPI PID: $FASTAPI_PID"
echo "HTTPS URL: https://211.182.230.53"
echo "API 문서: https://211.182.230.53/docs"

# 프로세스 종료를 위한 트랩 설정
trap "echo '서비스를 종료합니다...'; kill $FASTAPI_PID; nginx -s quit; exit" INT TERM

# 프로세스가 실행 중인 동안 대기
wait
EOF

chmod +x start_services.sh