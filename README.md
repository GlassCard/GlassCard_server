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

```bash
python main.py
```

또는

```bash
uvicorn main:app --reload
```

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

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

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