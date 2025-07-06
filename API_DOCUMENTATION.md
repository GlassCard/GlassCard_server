# GlassCard API 문서 (Supabase 연동용)

## 개요
GlassCard는 한국어 단어 및 구문을 의미론적 유사도와 품사를 고려해 비교하는 시스템입니다.
**Supabase와 연동하여 사용하시는 경우를 위한 간소화된 API입니다.**

**Base URL**: `http://127.0.0.1:8000/api/v1`

## 인증
현재 버전에서는 인증이 필요하지 않습니다.

## API 엔드포인트

### 단어 의미 비교
**POST** `/compare`

의미 단어들과 사용자 입력 단어들을 비교하여 유사도를 분석합니다.

#### 요청 파라미터
- `meaning` (string, required): 의미 단어들 (쉼표로 구분)
- `user_input` (string, required): 사용자 입력 단어들 (쉼표로 구분)

#### 요청 예시
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/compare?meaning=사랑,좋아해,행복&user_input=애정,사랑하다,기쁨"
```

#### 응답 형식

**성공 응답**
```json
{
  "success": true,
  "analysis": {
    "meaning_words": ["사랑", "좋아해", "행복"],
    "user_words": ["애정", "사랑하다", "기쁨"],
    "similarity_matrix": [
      [0.85, 0.72, 0.68],
      [0.78, 0.91, 0.65],
      [0.62, 0.58, 0.89]
    ],
    "best_matches": [
      {
        "meaning_word": "사랑",
        "user_word": "애정",
        "similarity": 0.85
      }
    ],
    "total_score": 0.82,
    "pos_analysis": {
      "meaning_pos": ["명사", "동사", "명사"],
      "user_pos": ["명사", "동사", "명사"],
      "pos_match_score": 1.0
    }
  }
}
```

**에러 응답**
```json
{
  "detail": "에러 메시지"
}
```

## JavaScript/TypeScript 사용 예시

### Fetch API 사용
```javascript
// 단어 비교
async function compareWords(meaning, userInput) {
  const response = await fetch(`http://127.0.0.1:8000/api/v1/compare?meaning=${encodeURIComponent(meaning)}&user_input=${encodeURIComponent(userInput)}`, {
    method: 'POST'
  });
  
  if (!response.ok) {
    throw new Error('API 요청 실패');
  }
  
  return await response.json();
}

// 사용 예시
const result = await compareWords("사랑,좋아해,행복", "애정,사랑하다,기쁨");
console.log(result.analysis.total_score); // 0.82
```

### Axios 사용
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1'
});

// 단어 비교
const compareWords = async (meaning, userInput) => {
  const response = await api.post('/compare', null, {
    params: { meaning, user_input: userInput }
  });
  return response.data;
};

// 사용 예시
const result = await compareWords("사랑,좋아해,행복", "애정,사랑하다,기쁨");
console.log(result.analysis.total_score); // 0.82
```

### Supabase와 함께 사용
```javascript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient('YOUR_SUPABASE_URL', 'YOUR_SUPABASE_ANON_KEY');

// 1. 사용자 입력을 받아서 API 호출
async function analyzeUserInput(userInput) {
  // 의미 단어들을 Supabase에서 가져오기
  const { data: meaningWords } = await supabase
    .from('meaning_words')
    .select('word, meaning');
  
  // 의미 단어들을 쉼표로 구분하여 문자열로 만들기
  const meaningString = meaningWords.map(item => item.word).join(',');
  
  // GlassCard API 호출
  const result = await compareWords(meaningString, userInput);
  
  // 결과를 Supabase에 저장
  const { data, error } = await supabase
    .from('analysis_results')
    .insert({
      user_input: userInput,
      meaning_words: meaningString,
      total_score: result.analysis.total_score,
      best_matches: result.analysis.best_matches
    });
  
  return result;
}
```

## 응답 데이터 구조

### analysis 객체
- `meaning_words`: 의미 단어 배열
- `user_words`: 사용자 입력 단어 배열
- `similarity_matrix`: 단어 간 유사도 행렬 (2차원 배열)
- `best_matches`: 가장 유사한 단어 쌍들의 배열
- `total_score`: 전체 유사도 점수 (0~1)
- `pos_analysis`: 품사 분석 결과

### best_matches 배열의 각 항목
- `meaning_word`: 의미 단어
- `user_word`: 사용자 입력 단어
- `similarity`: 두 단어 간 유사도 점수

## 주의사항

1. **URL 인코딩**: 한글 텍스트는 반드시 URL 인코딩을 해야 합니다.
2. **쉼표 구분**: 여러 단어는 쉼표로 구분하여 전달합니다.
3. **서버 상태**: 서버가 시작되지 않은 경우 500 에러가 발생할 수 있습니다.
4. **모델 로딩**: 첫 요청 시 sentence-transformers 모델 로딩으로 인해 지연이 발생할 수 있습니다.

## 테스트

API 테스트는 FastAPI 자동 생성 문서를 사용할 수 있습니다:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Supabase 연동 팁

1. **단어장 관리**: Supabase 테이블에서 의미 단어들을 관리
2. **결과 저장**: 분석 결과를 Supabase에 저장하여 히스토리 관리
3. **실시간 업데이트**: Supabase Realtime을 사용하여 실시간 결과 표시
4. **사용자 인증**: Supabase Auth를 사용하여 사용자별 분석 결과 관리 