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