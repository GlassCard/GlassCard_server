from typing import Dict, List
from sentence_transformers import SentenceTransformer, util
import torch
import gc
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
            # 메모리 효율적인 방식으로 임베딩 계산
            with torch.no_grad():  # 그래디언트 계산 비활성화로 메모리 절약
                embedding1 = self.model.encode(text1, convert_to_tensor=True)
                embedding2 = self.model.encode(text2, convert_to_tensor=True)
                similarity = util.pytorch_cos_sim(embedding1, embedding2).item()
                
                # 메모리 정리
                del embedding1, embedding2
                torch.cuda.empty_cache() if torch.cuda.is_available() else None
                
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
        
        # 종합 점수 계산 (더 관대한 가중치)
        total_score = (
            semantic_similarity * 0.5 +
            pos_matching_score * 0.2 +
            synonym_score * 0.2 +
            keyword_score * 0.1
        )
        
        # 보너스 점수: 의미 유사도가 높으면 추가 점수
        if semantic_similarity > 0.6:
            total_score += 0.1
        elif semantic_similarity > 0.4:
            total_score += 0.05
        
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
            return 0.7  # 품사 정보가 없으면 더 높은 점수
        
        matching_count = 0
        total_count = 0
        
        for pos, words in meaning_pos.items():
            if pos in user_pos:
                matching_count += 1
                total_count += 1
            else:
                total_count += 1
        
        base_score = matching_count / total_count if total_count > 0 else 0.0
        
        # 품사가 일치하지 않아도 기본 점수 부여
        if base_score == 0.0 and (meaning_pos or user_pos):
            return 0.3  # 품사가 다르더라도 기본 점수
        
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
        # 확장된 동의어 사전 (더 관대한 매칭)
        synonym_dict = {
            "사랑": ["사랑하다", "좋아하다", "애정", "연애", "사랑스럽다", "귀엽다", "예쁘다"],
            "행복": ["행복하다", "기쁘다", "즐겁다", "만족", "신나다", "좋다", "훌륭하다"],
            "슬픔": ["슬프다", "우울하다", "비통하다", "애도", "속상하다", "마음이 아프다"],
            "기쁨": ["기쁘다", "즐겁다", "행복하다", "환희", "신나다", "좋다", "만족"],
            "화": ["화나다", "분노", "격분", "노여움", "짜증나다", "열받다", "화가 나다"],
            "걱정": ["걱정하다", "염려", "불안", "근심", "불안하다", "걱정스럽다"],
            "희망": ["희망하다", "바라다", "기대", "꿈", "원하다", "원망하다"],
            "사과": ["미안하다", "죄송하다", "사죄", "용서", "죄송합니다", "미안합니다"],
            "감사": ["고맙다", "감사하다", "은혜", "고마움", "감사합니다", "고맙습니다"],
            "축하": ["축하하다", "경사", "기념", "축복", "축하합니다", "축하해"],
            "학습": ["공부하다", "배우다", "익히다", "습득하다", "연습하다"],
            "노력": ["열심히", "부지런히", "성실히", "최선을 다하다"],
            "성공": ["성취하다", "달성하다", "이루다", "해내다", "성공하다"],
            "실패": ["실패하다", "실수하다", "틀리다", "잘못하다", "놓치다"]
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