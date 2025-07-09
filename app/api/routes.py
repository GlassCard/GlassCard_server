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
        
        # 개별 단어 비교 결과 추가
        individual_comparisons = similarity_service.compare_individual_words(
            analysis_result["meaning_words"], 
            analysis_result["user_words"]
        )
        
        # 유사도 점수 로그 출력
        print(f"🔍 유사도 분석 결과:")
        print(f"   입력: '{request.meaning}' vs '{request.user_input}'")
        print(f"   총 점수: {analysis_result['total_score']:.3f}")
        print(f"   의미 유사도: {analysis_result['semantic_similarity']:.3f}")
        print(f"   품사 매칭: {analysis_result['pos_matching_score']:.3f}")
        print(f"   동의어 점수: {analysis_result['synonym_score']:.3f}")
        print(f"   키워드 점수: {analysis_result['keyword_score']:.3f}")
        
        # 개별 비교 결과 출력 (상위 3개)
        print(f"   개별 비교 (상위 3개):")
        for i, comp in enumerate(individual_comparisons[:3], 1):
            match_type = "🎯 정확한 일치" if comp['is_exact_match'] else \
                        "⭐ 높은 유사도" if comp['is_high_similarity'] else \
                        "🔄 중간 유사도" if comp['is_medium_similarity'] else "📉 낮은 유사도"
            print(f"     {i}. {comp['meaning_word']} ↔ {comp['user_word']}: {comp['similarity_score']:.3f} ({match_type})")
        
        print("-" * 60)
        
        return {
            "success": True,
            "analysis": analysis_result,
            "individual_comparisons": individual_comparisons
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
        
        # 개별 단어 비교 결과 추가
        individual_comparisons = similarity_service.compare_individual_words(
            analysis_result["meaning_words"], 
            analysis_result["user_words"]
        )
        
        # 유사도 점수 로그 출력
        print(f"🔍 유사도 분석 결과 (쿼리 파라미터):")
        print(f"   입력: '{meaning}' vs '{user_input}'")
        print(f"   총 점수: {analysis_result['total_score']:.3f}")
        print(f"   의미 유사도: {analysis_result['semantic_similarity']:.3f}")
        print(f"   품사 매칭: {analysis_result['pos_matching_score']:.3f}")
        print(f"   동의어 점수: {analysis_result['synonym_score']:.3f}")
        print(f"   키워드 점수: {analysis_result['keyword_score']:.3f}")
        
        # 개별 비교 결과 출력 (상위 3개)
        print(f"   개별 비교 (상위 3개):")
        for i, comp in enumerate(individual_comparisons[:3], 1):
            match_type = "🎯 정확한 일치" if comp['is_exact_match'] else \
                        "⭐ 높은 유사도" if comp['is_high_similarity'] else \
                        "🔄 중간 유사도" if comp['is_medium_similarity'] else "📉 낮은 유사도"
            print(f"     {i}. {comp['meaning_word']} ↔ {comp['user_word']}: {comp['similarity_score']:.3f} ({match_type})")
        
        print("-" * 60)
        
        return {
            "success": True,
            "analysis": analysis_result,
            "individual_comparisons": individual_comparisons
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류 발생: {str(e)}") 