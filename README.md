# GlassCard - 한국어 단어 의미 비교 시스템

한국어 단어 및 구문을 의미론적 유사도와 품사(POS)를 고려해 비교하는 FastAPI 기반 시스템입니다.

## 🏗️ 프로젝트 구조

```
GlassCard/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # API 라우터
│   ├── models/
│   │   ├── __init__.py
│   │   ├── word_database.py   # 단어장 데이터베이스
│   │   └── auto_learner.py    # 자동 학습 시스템
│   ├── services/
│   │   ├── __init__.py
│   │   └── similarity_service.py  # 유사도 분석 서비스
│   └── utils/
│       ├── __init__.py
│       └── text_processor.py  # 텍스트 처리 유틸리티
├── main.py                    # FastAPI 앱 진입점
├── test_main.http            # API 테스트 파일
└── README.md                 # 프로젝트 문서
```

## 🚀 주요 기능

### 1. 의미론적 유사도 분석
- **sentence-transformers** 모델을 사용한 의미 유사도 계산
- 다국어 지원 (한국어 최적화)

### 2. 품사(POS) 분석
- **konlpy**를 활용한 한국어 품사 분석
- 품사 매칭을 통한 정확도 향상

### 3. 하이브리드 검색 시스템
- **단어장 기반 빠른 검색**: 미리 계산된 임베딩으로 초고속 검색
- **의미 분석**: 단어장에 없는 단어는 실시간 분석
- **자동 학습**: 높은 점수의 결과는 자동으로 단어장에 추가

### 4. 다양한 입력 형태 지원
- 쉼표로 구분된 단어 목록
- 품사 태그가 포함된 입력 (`동.사랑하다/명.사랑`)
- 불완전한 품사 입력 감지 및 안내

## 📦 설치 및 실행

### 1. 의존성 설치
```bash
pip install fastapi uvicorn sentence-transformers konlpy torch
```

### 2. 서버 실행
```bash
python main.py
```

또는
```bash
uvicorn main:app --reload
```

### 3. API 문서 확인
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 🔧 API 엔드포인트

### 기본 엔드포인트
- `GET /` - 시스템 정보
- `GET /health` - 헬스 체크

### 단어 분석 API (`/api/v1/`)
- `POST /compare` - 단어 의미 비교
- `POST /add-word` - 단어장에 단어 추가
- `GET /word-stats` - 단어장 통계 조회
- `GET /search` - 단어장에서 검색
- `GET /analyze-pos` - 품사 분석

## 💡 사용 예시

### 1. 기본 의미 비교
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/compare?meaning=사랑,좋아해,행복&user_input=행복한,좋아하다,사랑하다"
```

### 2. 품사 정보 포함 비교
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/compare?meaning=동.사랑하다,좋아하다/명.사랑&user_input=동.사랑하다,좋아하다/명.사랑"
```

### 3. 단어 추가
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/add-word?word=기쁨&meaning=기쁘다,즐겁다,환희&pos=명사"
```

### 4. 단어장 검색
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/search?query=사랑&top_k=3"
```

## 🧪 테스트

`test_main.http` 파일을 사용하여 모든 API를 테스트할 수 있습니다:

```bash
# VS Code에서 REST Client 확장 사용
# 또는 curl 명령어로 직접 테스트
```

## ⚡ 성능 최적화

### 1. 캐싱 시스템
- LRU 캐시를 통한 품사 분석 결과 캐싱
- 임베딩 계산 결과 캐싱

### 2. 배치 처리
- 여러 단어의 임베딩을 한 번에 계산
- 벡터화 연산으로 성능 향상

### 3. 하이브리드 검색
- 단어장에 있는 단어: 즉시 응답
- 새로운 단어: 실시간 분석 후 자동 학습

## 🔄 자동 학습 시스템

- **학습 임계값**: 0.7 이상의 점수
- **최대 단어 수**: 1000개 (설정 가능)
- **중복 방지**: 이미 있는 단어는 학습하지 않음

## 📊 모니터링

- 단어장 통계 실시간 조회
- 검색 방법 추적 (database_search vs semantic_analysis)
- 성능 메트릭 제공

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🆘 문제 해결

### Java 관련 오류
konlpy 사용 시 Java가 필요합니다:
```bash
# macOS
brew install openjdk

# Ubuntu
sudo apt-get install openjdk-11-jdk
```

### 메모리 부족 오류
JVM 힙 크기 조정:
```bash
export JAVA_TOOL_OPTIONS="-Xss512m"
``` 