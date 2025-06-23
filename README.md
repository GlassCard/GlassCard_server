<<<<<<< HEAD
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
=======
# GlassCard API

의미 기반 단어 암기 웹 서비스 API (Access Key 인증 시스템 + 자동 품사 추출/추측 기능 + 태그 필터링)

## 📋 프로젝트 개요

GlassCard는 사용자가 단어의 의미를 자신의 언어로 표현하고, AI가 이를 정답과 비교하여 의미 기반 평가를 수행하는 단어 암기 서비스입니다. **Access Key를 통한 간단한 인증 시스템**, **자동 품사 추출/추측 기능**, **태그 기반 필터링**으로 단어장을 효율적으로 관리할 수 있습니다.

## 🔐 Access Key 인증 시스템

- **단어장 생성**: 사용자가 원하는 Access Key를 설정
- **단어장 수정/삭제**: Access Key 검증 후에만 가능
- **단어 추가/삭제**: 단어장의 Access Key 검증 후에만 가능
- **단어장 조회**: Access Key 없이도 가능 (공개)
- **답변 제출**: Access Key 없이도 가능 (공개)

## 🤖 자동 품사 추출/추측 시스템

### 품사 표기 자동 인식
- **한국어**: `명.`, `동.`, `형.`, `부.`, `전.`, `접.`, `감.`, `대.`, `관.`, `수.`
- **영어**: `N.`, `V.`, `ADJ.`, `ADV.`, `PREP.`, `CONJ.`, `INT.`, `PRON.`, `ART.`, `NUM.`

### 품사 자동 추측
품사 표기가 없는 경우에도 단어의 형태를 분석하여 자동으로 품사를 추측합니다:

#### 한국어 추측 패턴
- **동사**: `하다`, `되다`, `이다`, `있다`, `없다` 등으로 끝나는 단어
- **형용사**: `다`로 끝나는 단어 (동사가 아닌 경우)
- **부사**: `게`, `히`, `이`, `로`, `으로` 등으로 끝나는 단어
- **감탄사**: `와`, `오`, `어`, `아` 등
- **수사**: 숫자나 한자 숫자
- **대명사**: `나`, `너`, `그`, `이`, `저` 등
- **전치사/접속사**: `에서`, `에`, `와`, `과`, `그리고`, `또는` 등

#### 영어 추측 패턴
- **동사**: `ing`, `ed`, `s`로 끝나는 단어
- **형용사**: `ful`, `ous`, `al`, `ive`, `able`, `ible` 등으로 끝나는 단어
- **부사**: `ly`로 끝나는 단어
- **감탄사**: `wow`, `oh`, `ah`, `oops` 등
- **수사**: 숫자나 `one`, `two`, `first` 등
- **대명사**: `I`, `you`, `he`, `she`, `it`, `we`, `they` 등
- **전치사/접속사**: `in`, `on`, `at`, `and`, `or`, `but` 등

### 사용 예시
```json
{
  "word": "Love",
  "meaning": "명. 사랑, 사랑애/동. 사랑하다"  // → "noun/verb"
}
{
  "word": "Beautiful", 
  "meaning": "adj. beautiful, pretty"        // → "adjective"
}
{
  "word": "사랑",
  "meaning": "사랑"                          // → "noun" (추측)
}
{
  "word": "달리다",
  "meaning": "달리다"                        // → "verb" (추측)
}
```

## 🏗️ 아키텍처

- **Backend**: FastAPI (Python 3.12)
- **Database**: Supabase (PostgreSQL)
- **Architecture**: DDD (Domain-Driven Design)
- **Authentication**: Access Key 기반 간단 인증
- **AI**: 의미 기반 평가 시스템

## 📁 프로젝트 구조

```
GC-server/
├── api/                    # FastAPI 라우터
│   ├── __init__.py
│   ├── dependencies.py     # 의존성 주입 (Access Key 검증 포함)
│   ├── vocab_list.py      # 단어장 API
│   ├── vocab_item.py      # 단어 API
│   └── answer.py          # 답변 API
├── application/           # 애플리케이션 서비스
│   ├── __init__.py
│   └── services.py        # 비즈니스 로직
├── domain/               # 도메인 모델
│   ├── __init__.py
│   ├── models.py         # 엔티티
│   └── repositories.py   # 리포지토리 인터페이스
├── infrastructure/       # 인프라스트럭처
│   ├── __init__.py
│   ├── config.py         # 설정
│   ├── supabase_client.py # Supabase 클라이언트
│   ├── repositories.py   # Supabase 리포지토리 구현
│   ├── ai_service.py     # AI 평가 서비스
│   └── utils.py          # 유틸리티 (품사 추출/추측)
├── schemas/              # Pydantic DTO
│   ├── __init__.py
│   ├── requests.py       # 요청 DTO
│   └── responses.py      # 응답 DTO
├── main.py              # FastAPI 엔트리포인트
├── requirements.txt     # 의존성
├── .env                 # 환경 변수
├── .gitignore          # Git 무시 파일
├── test_main.http      # API 테스트
└── README.md           # 프로젝트 문서
```

## 🚀 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 Supabase 설정을 입력하세요:

```env
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here
DEBUG=True
```

### 3. 서버 실행

>>>>>>> f417104b5291f33fd4b76b159ca571ca2b6a48c6
```bash
python main.py
```

또는
<<<<<<< HEAD
=======

>>>>>>> f417104b5291f33fd4b76b159ca571ca2b6a48c6
```bash
uvicorn main:app --reload
```

<<<<<<< HEAD
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
=======
서버가 실행되면 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📊 데이터베이스 스키마

### vocab_lists
- `id`: UUID (PK)
- `title`: TEXT NOT NULL
- `description`: TEXT
- `created_at`: TIMESTAMP DEFAULT NOW()
- `expires_at`: TIMESTAMP NOT NULL
- `access_key`: TEXT NOT NULL
- `is_deleted`: BOOLEAN DEFAULT FALSE

### vocab_items
- `id`: UUID (PK)
- `vocab_list_id`: UUID (FK)
- `word`: TEXT NOT NULL
- `meaning`: TEXT NOT NULL
- `part_of_speech`: TEXT

### answers
- `id`: UUID (PK)
- `vocab_item_id`: UUID (FK)
- `user_meaning`: TEXT NOT NULL
- `similarity_score`: FLOAT
- `is_correct`: BOOLEAN
- `created_at`: TIMESTAMP DEFAULT NOW()

## 🔌 API 엔드포인트

### 단어장 관리
- `POST /v1/vocab-list/` - 단어장 생성
- `POST /v1/vocab-list/with-items` - 단어장과 단어들을 한 번에 생성 (품사 자동 추출/추측)
- `GET /v1/vocab-list/` - 모든 단어장 목록 조회 (삭제되지 않은 것만)
- `GET /v1/vocab-list/{id}` - 단어장 상세 조회
- `PUT /v1/vocab-list/{id}` - 단어장 수정 (Access Key 검증 필요)
- `DELETE /v1/vocab-list/{id}` - 단어장 삭제 (Access Key 검증 필요)

### 단어 관리
- `POST /v1/vocab-list/{id}/items` - 단어 추가 (Access Key 검증 필요)
- `GET /v1/vocab-list/{id}/items` - 단어장의 단어 목록 조회
- `DELETE /v1/vocab-list/items/{item_id}` - 단어 삭제 (Access Key 검증 필요)

### 답변 및 평가
- `POST /v1/answer` - 답변 제출 및 AI 평가 (실시간 평가, DB 저장 없음)
- `GET /v1/vocab-item/{item_id}/answers` - 단어의 답변 목록 조회 (DB 저장을 하지 않으므로 빈 리스트 반환)

## 🔑 Access Key 사용법

### 1. 단어장 생성 시 Access Key 설정
```json
{
  "title": "영어 기초 단어장",
  "description": "일상생활에서 자주 사용하는 영어 단어들",
  "expires_at": "2024-12-31T23:59:59",
  "access_key": "my-secret-key-123"
}
```

### 2. 단어장과 단어들을 한 번에 생성 (품사 자동 처리)
```json
{
  "title": "임시 단어장",
  "description": "임시 단어장장",
  "expires_at": "2024-12-31T23:59:59",
  "access_key": "temp-key-456",
  "items": [
    {
      "word": "Love",
      "meaning": "명. 사랑, 사랑애/동. 사랑하다"  // 품사 자동 추출
    },
    {
      "word": "사랑",
      "meaning": "사랑"                          // 품사 자동 추측
    }
  ]
}
```

### 3. 단어장 수정 시 Access Key 검증
```json
{
  "title": "수정된 제목",
  "access_key": "my-secret-key-123"
}
```

### 4. 단어 추가 시 Access Key 검증
```
POST /v1/vocab-list/{id}/items?access_key=my-secret-key-123
```

### 5. 단어장/단어 삭제 시 Access Key 검증
```
DELETE /v1/vocab-list/{id}?access_key=my-secret-key-123
DELETE /v1/vocab-list/items/{item_id}?access_key=my-secret-key-123
```

## 🤖 AI 평가 시스템

AI 서비스는 다음과 같은 방식으로 의미 기반 평가를 수행합니다:

1. **텍스트 전처리**: 소문자 변환, 특수문자 제거
2. **키워드 추출**: 불용어 제거 후 핵심 키워드 추출
3. **유사도 계산**: 키워드 매칭 및 문장 구조 분석
4. **점수 산정**: 키워드 70%, 구조 30% 가중치 적용
5. **피드백 생성**: 점수에 따른 개인화된 피드백 제공

## 🔧 개발 가이드

### 새로운 기능 추가

1. **도메인 모델 정의** (`domain/models.py`)
2. **리포지토리 인터페이스 정의** (`domain/repositories.py`)
3. **Supabase 구현체 작성** (`infrastructure/repositories.py`)
4. **서비스 로직 구현** (`application/services.py`)
5. **API 엔드포인트 추가** (`api/` 디렉토리)
6. **의존성 주입 설정** (`api/dependencies.py`)

### 테스트

```bash
# 테스트 실행 (향후 구현 예정)
pytest
```
>>>>>>> f417104b5291f33fd4b76b159ca571ca2b6a48c6

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

<<<<<<< HEAD
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
=======
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
>>>>>>> f417104b5291f33fd4b76b159ca571ca2b6a48c6
``` 