from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import uvicorn

from app.api.routes import router, init_services

# FastAPI 앱 생성
app = FastAPI(
    title="GlassCard - 한국어 단어 의미 비교 시스템",
    description="한국어 단어 및 구문을 의미론적 유사도와 품사를 고려해 비교하는 시스템",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """앱 시작 시 초기화"""
    print("GlassCard 시스템을 시작합니다...")
    
    # 모델 로드
    print("sentence-transformers 모델을 로드하는 중...")
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    
    # 서비스 초기화
    print("서비스들을 초기화하는 중...")
    init_services(model)
    
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
    uvicorn.run(app, host="127.0.0.1", port=8000)