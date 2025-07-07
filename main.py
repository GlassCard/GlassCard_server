from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
import uvicorn
import os
import gc

from app.api.routes import router, init_services

# FastAPI 앱 생성
app = FastAPI(
    title="GlassCard - 한국어 단어 의미 비교 시스템",
    description="한국어 단어 및 구문을 의미론적 유사도와 품사를 고려해 비교하는 시스템",
    version="1.0.0"
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.on_event("startup")
async def startup_event():
    """앱 시작 시 초기화"""
    print("GlassCard 시스템을 시작합니다...")
    
    # 메모리 최적화
    gc.collect()
    
    # Hugging Face 토큰 설정 (선택사항)
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    if hf_token:
        print("Hugging Face 토큰이 설정되었습니다.")
        os.environ["HUGGINGFACE_HUB_TOKEN"] = hf_token
    
    # 모델 로드 (메모리 효율적인 모델 사용)
    print("sentence-transformers 모델을 로드하는 중...")
    try:
        # 가장 가벼운 모델부터 시도
        print("가장 가벼운 모델을 로드합니다...")
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print("모델 로드 성공!")
    except Exception as e:
        print(f"기본 모델 로드 실패: {e}")
        print("대체 모델을 시도합니다...")
        try:
            # 더 작은 한국어 모델 사용
            model = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v2')
            print("대체 모델 로드 성공!")
        except Exception as e2:
            print(f"대체 모델 로드도 실패: {e2}")
            print("가장 기본적인 모델을 시도합니다...")
            try:
                # 가장 기본적인 모델
                model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L6-v2')
                print("기본 모델 로드 성공!")
            except Exception as e3:
                print(f"모든 모델 로드 실패: {e3}")
                print("메모리 부족으로 인해 모델 로드에 실패했습니다.")
                print("다음 중 하나를 시도해보세요:")
                print("1. 더 많은 메모리 확보")
                print("2. HUGGINGFACE_TOKEN 환경 변수 설정")
                print("3. 더 작은 모델 사용")
                raise e3
    
    # 서비스 초기화
    print("서비스들을 초기화하는 중...")
    init_services(model)
    
    # 메모리 정리
    gc.collect()
    
    print("GlassCard 시스템이 성공적으로 시작되었습니다!")

# 라우터 등록
app.include_router(router, prefix="/api/v1", tags=["word-analysis"])

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "GlassCard - 한국어 단어 의미 비교 시스템",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy", "service": "GlassCard"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)