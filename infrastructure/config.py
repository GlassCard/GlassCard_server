import os
from typing import Optional
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Settings:
    # Supabase 설정
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # AI 모델 설정 (향후 확장용)
    AI_MODEL_ENDPOINT: Optional[str] = os.getenv("AI_MODEL_ENDPOINT")
    
    # 애플리케이션 설정
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    @classmethod
    def validate(cls) -> bool:
        """필수 설정값 검증"""
        if not cls.SUPABASE_URL:
            raise ValueError("SUPABASE_URL 환경변수가 설정되지 않았습니다.")
        if not cls.SUPABASE_KEY:
            raise ValueError("SUPABASE_KEY 환경변수가 설정되지 않았습니다.")
        return True
    
    @classmethod
    def print_config(cls):
        """설정값 출력 (디버깅용)"""
        print(f"SUPABASE_URL: {'설정됨' if cls.SUPABASE_URL else '설정되지 않음'}")
        print(f"SUPABASE_KEY: {'설정됨' if cls.SUPABASE_KEY else '설정되지 않음'}")
        print(f"DEBUG: {cls.DEBUG}")


settings = Settings() 