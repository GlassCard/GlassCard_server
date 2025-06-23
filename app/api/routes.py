from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..services.similarity_service import SimilarityService
from ..models.word_database import WordDatabase
from ..models.auto_learner import AutoLearningSystem
from ..utils.text_processor import parse_comma_separated_input, analyze_pos

router = APIRouter()

# 전역 변수로 서비스들을 저장 (실제로는 의존성 주입 사용 권장)
similarity_service = None
word_database = None
auto_learner = None

def init_services(model):
    """서비스들을 초기화합니다."""
    global similarity_service, word_database, auto_learner
    
    similarity_service = SimilarityService(model)
    word_database = WordDatabase(model)
    auto_learner = AutoLearningSystem(word_database)
    
    # 초기 단어장 데이터 추가
    _initialize_word_database()

def _initialize_word_database():
    """초기 단어장 데이터를 추가합니다."""
    initial_words = [
        ("사랑", "사랑, 좋아해, 행복", "명사"),
        ("행복", "행복한, 기쁘다, 만족", "명사"),
        ("슬픔", "슬프다, 우울하다, 비통하다", "명사"),
        ("기쁨", "기쁘다, 즐겁다, 환희", "명사"),
        ("화", "화나다, 분노, 격분", "명사"),
        ("걱정", "걱정하다, 염려, 불안", "명사"),
        ("희망", "희망하다, 바라다, 기대", "명사"),
        ("사과", "미안하다, 죄송하다, 사죄", "명사"),
        ("감사", "고맙다, 감사하다, 은혜", "명사"),
        ("축하", "축하하다, 경사, 기념", "명사")
    ]
    
    for word, meaning, pos in initial_words:
        word_database.add_word(word, meaning, pos)

@router.post("/compare")
async def compare_words(
    meaning: str = Query(..., description="의미 단어들 (쉼표로 구분)"),
    user_input: str = Query(..., description="사용자 입력 단어들 (쉼표로 구분)")
):
    """단어 의미 비교 API"""
    if not similarity_service:
        raise HTTPException(status_code=500, detail="서비스가 초기화되지 않았습니다.")
    
    try:
        # 하이브리드 시스템: 단어장 검색 먼저 시도
        meaning_words = parse_comma_separated_input(meaning)
        user_words = parse_comma_separated_input(user_input)
        
        # 단어장에서 빠른 검색
        db_results = word_database.find_best_match(user_input, user_words, top_k=3)
        
        if db_results and db_results[0]["total_score"] > 0.8:
            # 단어장에서 높은 점수로 찾은 경우
            best_match = db_results[0]
            return {
                "method": "database_search",
                "best_match": best_match,
                "all_matches": db_results,
                "database_stats": word_database.get_stats()
            }
        
        # 단어장에서 찾지 못한 경우 기존 의미 분석 사용
        analysis_result = similarity_service.analyze_similarity_with_pos(meaning, user_input)
        
        if "error" in analysis_result:
            return analysis_result
        
        # 자동 학습 시도
        if analysis_result["total_score"] > 0.7:
            auto_learner.auto_learn_word(user_input, meaning)
        
        return {
            "method": "semantic_analysis",
            "analysis": analysis_result,
            "database_stats": word_database.get_stats()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류 발생: {str(e)}")

@router.post("/add-word")
async def add_word(
    word: str = Query(..., description="추가할 단어"),
    meaning: str = Query(..., description="단어의 의미"),
    pos: Optional[str] = Query(None, description="품사 정보")
):
    """단어장에 단어 추가 API"""
    if not word_database:
        raise HTTPException(status_code=500, detail="서비스가 초기화되지 않았습니다.")
    
    try:
        word_id = word_database.add_word(word, meaning, pos)
        return {
            "success": True,
            "word_id": word_id,
            "message": f"단어 '{word}'이(가) 성공적으로 추가되었습니다.",
            "database_stats": word_database.get_stats()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"단어 추가 중 오류 발생: {str(e)}")

@router.get("/word-stats")
async def get_word_stats():
    """단어장 통계 조회 API"""
    if not word_database:
        raise HTTPException(status_code=500, detail="서비스가 초기화되지 않았습니다.")
    
    return word_database.get_stats()

@router.get("/search")
async def search_words(
    query: str = Query(..., description="검색할 단어"),
    top_k: int = Query(5, description="반환할 최대 결과 수")
):
    """단어장에서 단어 검색 API"""
    if not word_database:
        raise HTTPException(status_code=500, detail="서비스가 초기화되지 않았습니다.")
    
    try:
        query_words = parse_comma_separated_input(query)
        results = word_database.find_best_match(query, query_words, top_k=top_k)
        
        return {
            "query": query,
            "results": results,
            "total_found": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색 중 오류 발생: {str(e)}")

@router.get("/analyze-pos")
async def analyze_pos_endpoint(
    text: str = Query(..., description="품사 분석할 텍스트")
):
    """품사 분석 API"""
    try:
        pos_result = analyze_pos(text)
        return {
            "text": text,
            "pos_analysis": pos_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"품사 분석 중 오류 발생: {str(e)}") 