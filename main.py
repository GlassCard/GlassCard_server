from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.config import settings
from api.vocab_list import router as vocab_list_router
from api.vocab_item import router as vocab_item_router
from api.answer import router as answer_router

# 설정 출력 (디버깅용)
print("=== GlassCard API 설정 ===")
settings.print_config()
print("==========================")

# FastAPI 앱 생성
app = FastAPI(
    title="GlassCard API",
    description="의미 기반 단어 암기 웹 서비스 API",
    version="1.0.0",
    redirect_slashes=False
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(vocab_list_router)
app.include_router(vocab_item_router)
app.include_router(answer_router)

@app.get("/")
async def root():
    return {
        "message": "GlassCard API에 오신 것을 환영합니다!",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    # Supabase 연결 상태 확인
    try:
        from infrastructure.supabase_client import get_supabase_client
        supabase = get_supabase_client()
        if supabase:
            return {
                "status": "healthy", 
                "message": "서비스가 정상적으로 실행 중입니다.",
                "database": "connected"
            }
        else:
            return {
                "status": "healthy", 
                "message": "서비스가 정상적으로 실행 중입니다. (데이터베이스 미연결)",
                "database": "disconnected",
                "note": "환경 변수 SUPABASE_URL과 SUPABASE_KEY를 설정해주세요.",
                "config": {
                    "supabase_url_set": bool(settings.SUPABASE_URL),
                    "supabase_key_set": bool(settings.SUPABASE_KEY)
                }
            }
    except Exception as e:
        return {
            "status": "healthy", 
            "message": "서비스가 정상적으로 실행 중입니다. (데이터베이스 오류)",
            "database": "error",
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
