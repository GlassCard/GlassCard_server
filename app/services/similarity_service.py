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
            # 임베딩 계산
            embedding1 = self.model.encode(text1, convert_to_tensor=True)
            embedding2 = self.model.encode(text2, convert_to_tensor=True)
            similarity = util.cos_sim(embedding1, embedding2).item()
            
            # 메모리 정리
            del embedding1, embedding2
            
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
        
        # 종합 점수 계산 (더 엄격한 가중치)
        total_score = (
            semantic_similarity * 0.6 +
            pos_matching_score * 0.2 +
            synonym_score * 0.15 +
            keyword_score * 0.05
        )
        
        # 보너스 점수: 의미 유사도가 매우 높을 때만 추가 점수
        if semantic_similarity > 0.8:
            total_score += 0.05
        elif semantic_similarity > 0.6:
            total_score += 0.02
        
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
            return 0.3  # 품사 정보가 없으면 낮은 점수
        
        matching_count = 0
        total_count = 0
        
        for pos, words in meaning_pos.items():
            if pos in user_pos:
                matching_count += 1
                total_count += 1
            else:
                total_count += 1
        
        base_score = matching_count / total_count if total_count > 0 else 0.0
        
        # 품사가 일치하지 않으면 낮은 점수
        if base_score == 0.0 and (meaning_pos or user_pos):
            return 0.1  # 품사가 다르면 낮은 점수
        
        return base_score
    
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
        # 엄격한 동의어 사전 (정확한 동의어만)
        synonym_dict = {
            "사랑": ["사랑하다", "애정", "연애"],
            "행복": ["행복하다", "기쁘다", "즐겁다"],
            "슬픔": ["슬프다", "우울하다", "비통하다"],
            "기쁨": ["기쁘다", "즐겁다", "환희"],
            "화": ["화나다", "분노", "격분"],
            "걱정": ["걱정하다", "염려", "불안"],
            "희망": ["희망하다", "바라다", "기대"],
            "사과": ["미안하다", "죄송하다"],
            "감사": ["고맙다", "감사하다"],
            "축하": ["축하하다", "경사"],
            "학습": ["공부하다", "배우다"],
            "노력": ["열심히", "부지런히"],
            "성공": ["성취하다", "달성하다"],
            "실패": ["실패하다", "실수하다"]
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
    
    def compare_individual_words(self, meaning_words: List[str], user_words: List[str]) -> List[Dict]:
        """개별 단어들 간의 비교 결과를 반환합니다."""
        comparisons = []
        
        for i, meaning_word in enumerate(meaning_words):
            for j, user_word in enumerate(user_words):
                similarity = self.calculate_similarity(meaning_word, user_word)
                
                comparison = {
                    "meaning_word": meaning_word,
                    "user_word": user_word,
                    "similarity_score": similarity,
                    "meaning_index": i,
                    "user_index": j,
                    "is_exact_match": meaning_word == user_word,
                    "is_high_similarity": similarity > 0.7,
                    "is_medium_similarity": 0.4 <= similarity <= 0.7,
                    "is_low_similarity": similarity < 0.4
                }
                comparisons.append(comparison)
        
        # 유사도 점수 기준으로 정렬 (높은 점수부터)
        comparisons.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        return comparisons 