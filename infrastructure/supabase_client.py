from supabase import create_client, Client
from .config import settings


class SupabaseClient:
    _instance: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            # 환경 변수가 설정되지 않은 경우 None 반환
            if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
                return None
            cls._instance = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        return cls._instance
    
    @classmethod
    def reset_client(cls):
        """테스트용 클라이언트 리셋"""
        cls._instance = None


# 전역 클라이언트 인스턴스 (지연 초기화)
def get_supabase_client() -> Client:
    return SupabaseClient.get_client() 