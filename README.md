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
pip install -r requirements.txt
```

### 2. 환경 변수 설정 (선택사항)

Hugging Face 모델 다운로드 시 인증 문제가 발생하는 경우, 환경 변수를 설정하세요:

```bash
# Hugging Face 토큰 설정 (선택사항)
export HUGGINGFACE_TOKEN=your_token_here

# 또는 .env 파일 생성 (권장)
echo "HUGGINGFACE_TOKEN=your_token_here" > .env
```

**Hugging Face 토큰 생성 방법:**
1. https://huggingface.co/settings/tokens 에서 새 토큰 생성
2. 토큰을 환경 변수 `HUGGINGFACE_TOKEN`에 설정

### 3. 서버 실행
```bash
python main.py
```

또는
```bash
uvicorn main:app --reload
```

## 🔧 문제 해결

### Hugging Face 401 Unauthorized 오류

이 오류가 발생하는 경우:

1. **환경 변수 설정** (권장):
   ```bash
   export HUGGINGFACE_TOKEN=your_token_here
   ```

2. **토큰 없이 실행**: 코드가 자동으로 대체 모델을 시도합니다.

3. **수동 모델 다운로드**:
   ```bash
   python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
   ```

## 📚 API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 🧪 테스트

API 테스트는 `test_main.http` 파일을 사용하거나 FastAPI 자동 생성 문서를 사용할 수 있습니다.

## 🔄 자동 학습 시스템

- **학습 임계값**: 0.7 이상의 점수
- **최대 단어 수**: 1000개 (설정 가능)
- **중복 방지**: 이미 있는 단어는 학습하지 않음

## 📊 모니터링

- 단어장 통계 실시간 조회
- 검색 방법 추적 (database_search vs semantic_analysis)
- 성능 메트릭 제공

## 🤝 기여

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 

## 🏷️ 태그 시스템

단어장에 태그를 추가하여 카테고리별로 필터링할 수 있습니다.

### 지원 태그 예시
- **학년별**: `1학년`, `2학년`, `3학년`
- **시험별**: `단어시험`, `토익`, `토플`, `수능`
- **난이도별**: `기초`, `중급`, `고급`
- **기타**: `단어왕`, `영어`, `일본어`, `중국어`

### 태그 사용법
- **단어장 생성 시**: `tags` 필드에 태그 배열 추가
- **단어장 수정 시**: `tags` 필드로 태그 업데이트
- **필터링**: `GET /v1/vocab-list/?tags=1학년,영어` 형태로 쿼리 파라미터 사용

### 태그 필터링 예시
```bash
# 1학년 관련 단어장만 조회
GET /v1/vocab-list/?tags=1학년

# 토익 관련 단어장만 조회
GET /v1/vocab-list/?tags=토익

# 영어 관련 단어장만 조회
GET /v1/vocab-list/?tags=영어

# 여러 태그로 필터링 (OR 조건)
GET /v1/vocab-list/?tags=영어,시험
``` 