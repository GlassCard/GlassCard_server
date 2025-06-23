from typing import Dict, List
from sentence_transformers import SentenceTransformer, util
from ..utils.text_processor import (
    parse_pos_input, parse_comma_separated_input, 
    extract_words_from_pos_input, check_incomplete_pos_input,
    extract_keywords
)

class SimilarityService:
    def __init__(self, model: SentenceTransformer):
        self.model = model
        
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """두 텍스트 간의 의미 유사도를 계산합니다."""
        try:
            embedding1 = self.model.encode(text1, convert_to_tensor=True)
            embedding2 = self.model.encode(text2, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(embedding1, embedding2).item()
            return similarity
        except Exception as e:
            print(f"유사도 계산 오류: {e}")
            return 0.0
    
    def analyze_similarity_with_pos(self, meaning: str, user_input: str) -> Dict:
        """품사를 고려한 의미 유사도를 분석합니다."""
        # 불완전한 품사 입력 확인
        incomplete_check = check_incomplete_pos_input(user_input)
        if incomplete_check["is_incomplete"]:
            return {
                "error": incomplete_check["message"],
                "incomplete_input": True
            }
        
        # 품사 정보 파싱
        meaning_pos_info = parse_pos_input(meaning)
        user_pos_info = parse_pos_input(user_input)
        
        # 품사 정보가 없는 경우 일반 텍스트로 처리
        if not meaning_pos_info:
            meaning_words = parse_comma_separated_input(meaning)
        else:
            meaning_words = extract_words_from_pos_input(meaning)
        
        if not user_pos_info:
            user_words = parse_comma_separated_input(user_input)
        else:
            user_words = extract_words_from_pos_input(user_input)
        
        # 품사 매칭 점수 계산
        pos_matching_score = self._calculate_pos_matching_score(meaning_pos_info, user_pos_info)
        
        # 의미 유사도 계산
        semantic_similarity = self._calculate_semantic_similarity(meaning_words, user_words)
        
        # 동의어 확장 점수
        synonym_score = self._calculate_synonym_score(meaning_words, user_words)
        
        # 키워드 매칭 점수
        keyword_score = self._calculate_keyword_score(meaning, user_input)
        
        # 종합 점수 계산
        total_score = (
            semantic_similarity * 0.4 +
            pos_matching_score * 0.3 +
            synonym_score * 0.2 +
            keyword_score * 0.1
        )
        
        return {
            "semantic_similarity": semantic_similarity,
            "pos_matching_score": pos_matching_score,
            "synonym_score": synonym_score,
            "keyword_score": keyword_score,
            "total_score": total_score,
            "meaning_words": meaning_words,
            "user_words": user_words,
            "meaning_pos_info": meaning_pos_info,
            "user_pos_info": user_pos_info
        }
    
    def _calculate_pos_matching_score(self, meaning_pos: Dict, user_pos: Dict) -> float:
        """품사 매칭 점수를 계산합니다."""
        if not meaning_pos or not user_pos:
            return 0.5  # 품사 정보가 없으면 중간 점수
        
        matching_count = 0
        total_count = 0
        
        for pos, words in meaning_pos.items():
            if pos in user_pos:
                matching_count += 1
                total_count += 1
            else:
                total_count += 1
        
        return matching_count / total_count if total_count > 0 else 0.0
    
    def _calculate_semantic_similarity(self, meaning_words: List[str], user_words: List[str]) -> float:
        """의미 유사도를 계산합니다."""
        if not meaning_words or not user_words:
            return 0.0
        
        max_similarity = 0.0
        
        for meaning_word in meaning_words:
            for user_word in user_words:
                similarity = self.calculate_similarity(meaning_word, user_word)
                max_similarity = max(max_similarity, similarity)
        
        return max_similarity
    
    def _calculate_synonym_score(self, meaning_words: List[str], user_words: List[str]) -> float:
        """동의어 확장 점수를 계산합니다."""
        # 간단한 동의어 사전 (실제로는 더 큰 사전 사용)
        synonym_dict = {
            "사랑": ["사랑하다", "좋아하다", "애정", "연애"],
            "행복": ["행복하다", "기쁘다", "즐겁다", "만족"],
            "슬픔": ["슬프다", "우울하다", "비통하다", "애도"],
            "기쁨": ["기쁘다", "즐겁다", "행복하다", "환희"],
            "화": ["화나다", "분노", "격분", "노여움"],
            "걱정": ["걱정하다", "염려", "불안", "근심"],
            "희망": ["희망하다", "바라다", "기대", "꿈"],
            "사과": ["미안하다", "죄송하다", "사죄", "용서"],
            "감사": ["고맙다", "감사하다", "은혜", "고마움"],
            "축하": ["축하하다", "경사", "기념", "축복"]
        }
        
        matching_count = 0
        total_pairs = len(meaning_words) * len(user_words)
        
        for meaning_word in meaning_words:
            for user_word in user_words:
                # 직접 매칭
                if meaning_word == user_word:
                    matching_count += 1
                    continue
                
                # 동의어 매칭
                for base_word, synonyms in synonym_dict.items():
                    if (meaning_word in synonyms or meaning_word == base_word) and \
                       (user_word in synonyms or user_word == base_word):
                        matching_count += 1
                        break
        
        return matching_count / total_pairs if total_pairs > 0 else 0.0
    
    def _calculate_keyword_score(self, meaning: str, user_input: str) -> float:
        """키워드 매칭 점수를 계산합니다."""
        meaning_keywords = extract_keywords(meaning)
        user_keywords = extract_keywords(user_input)
        
        if not meaning_keywords or not user_keywords:
            return 0.0
        
        matching_count = 0
        for meaning_keyword in meaning_keywords:
            for user_keyword in user_keywords:
                if meaning_keyword == user_keyword:
                    matching_count += 1
        
        return matching_count / (len(meaning_keywords) + len(user_keywords) - matching_count) if (len(meaning_keywords) + len(user_keywords) - matching_count) > 0 else 0.0 