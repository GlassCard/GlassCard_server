from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from ..services.similarity_service import SimilarityService
from ..utils.text_processor import parse_comma_separated_input

router = APIRouter()

# 전역 변수로 서비스들을 저장
similarity_service = None

def init_services(model):
    """서비스들을 초기화합니다."""
    global similarity_service
    similarity_service = SimilarityService(model)

class CompareRequest(BaseModel):
    meaning: str
    user_input: str

@router.post("/compare")
async def compare_words(request: CompareRequest):
    """단어 의미 비교 API - JSON 본문으로 데이터 받기"""
    if not similarity_service:
        raise HTTPException(status_code=500, detail="서비스가 초기화되지 않았습니다.")
    
    try:
        # 의미 분석 수행
        analysis_result = similarity_service.analyze_similarity_with_pos(request.meaning, request.user_input)
        
        if "error" in analysis_result:
            return analysis_result
        
        return {
            "success": True,
            "analysis": analysis_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류 발생: {str(e)}")

# 기존 쿼리 파라미터 방식도 유지 (하위 호환성)
@router.post("/compare-query")
async def compare_words_query(
    meaning: str = Query(..., description="의미 단어들 (쉼표로 구분)"),
    user_input: str = Query(..., description="사용자 입력 단어들 (쉼표로 구분)")
):
    """단어 의미 비교 API - 쿼리 파라미터 방식 (하위 호환성)"""
    if not similarity_service:
        raise HTTPException(status_code=500, detail="서비스가 초기화되지 않았습니다.")
    
    try:
        # 의미 분석 수행
        analysis_result = similarity_service.analyze_similarity_with_pos(meaning, user_input)
        
        if "error" in analysis_result:
            return analysis_result
        
        return {
            "success": True,
            "analysis": analysis_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류 발생: {str(e)}") 