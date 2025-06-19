import re
from typing import Tuple, List
from sentence_transformers import SentenceTransformer, util
import torch

class AIService:
    """의미 기반 평가를 위한 AI 서비스"""
    
    # 모델을 클래스 변수로 초기화 (한 번만 로드)
    _model = None
    
    @classmethod
    def _get_model(cls):
        """모델을 lazy loading으로 가져오기"""
        if cls._model is None:
            cls._model = SentenceTransformer('all-MiniLM-L6-v2')
        return cls._model
    
    @staticmethod
    def evaluate_similarity(correct_meaning: str, user_meaning: str) -> Tuple[float, bool, str, List[str]]:
        """
        사용자의 답변과 정답을 비교하여 의미 기반 평가를 수행
        
        Args:
            correct_meaning: 정답 의미
            user_meaning: 사용자가 작성한 의미
            
        Returns:
            Tuple[similarity_score, is_correct, feedback, suggestions]
        """
        # 1. 기본 전처리
        correct_clean = AIService._preprocess_text(correct_meaning)
        user_clean = AIService._preprocess_text(user_meaning)
        
        # 2. 키워드 추출 및 비교
        correct_keywords = AIService._extract_keywords(correct_clean)
        user_keywords = AIService._extract_keywords(user_clean)
        
        # 3. 임베딩 기반 유사도 계산
        model = AIService._get_model()
        embeddings = model.encode([correct_meaning, user_meaning], convert_to_tensor=True)
        similarity_score = util.cos_sim(embeddings[0], embeddings[1]).item()
        
        # 4. 문장 구조 분석
        structure_score = AIService._analyze_structure_similarity(correct_clean, user_clean)
        
        # 5. 최종 점수 계산 (임베딩 유사도 70%, 구조 30%)
        final_score = (similarity_score * 0.7) + (structure_score * 0.3)
        
        # 6. 정답 여부 판단 (0.6 이상을 정답으로 간주)
        is_correct = final_score >= 0.6
        
        # 7. 피드백 생성
        feedback = AIService._generate_feedback(final_score, correct_keywords, user_keywords)
        
        # 8. 개선 제안 생성
        suggestions = AIService._generate_suggestions(correct_keywords, user_keywords, final_score)
        
        return final_score, is_correct, feedback, suggestions
    
    @staticmethod
    def _preprocess_text(text: str) -> str:
        """텍스트 전처리"""
        # 소문자 변환
        text = text.lower()
        # 특수문자 제거 (마침표, 쉼표 등은 유지)
        text = re.sub(r'[^\w\s\.\,\;\:\!\?]', '', text)
        # 여러 공백을 하나로
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @staticmethod
    def _extract_keywords(text: str) -> List[str]:
        """키워드 추출 (간단한 구현)"""
        # 불용어 목록
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
            'it', 'its', 'they', 'them', 'their', 'we', 'us', 'our', 'you', 'your'
        }
        
        words = text.split()
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return list(set(keywords))  # 중복 제거
    
    @staticmethod
    def _analyze_structure_similarity(correct_text: str, user_text: str) -> float:
        """문장 구조 유사도 분석"""
        # 간단한 구현: 길이와 단어 수 비교
        correct_words = correct_text.split()
        user_words = user_text.split()
        
        if not correct_words or not user_words:
            return 0.0
        
        # 길이 유사도
        length_ratio = min(len(user_words), len(correct_words)) / max(len(user_words), len(correct_words))
        
        # 공통 단어 비율
        common_words = set(correct_words) & set(user_words)
        common_ratio = len(common_words) / max(len(correct_words), len(user_words))
        
        return (length_ratio + common_ratio) / 2
    
    @staticmethod
    def _generate_feedback(score: float, correct_keywords: List[str], user_keywords: List[str]) -> str:
        """피드백 생성"""
        if score >= 0.8:
            return "훌륭합니다! 정답과 거의 일치하는 의미를 작성하셨습니다."
        elif score >= 0.6:
            return "좋습니다! 핵심 의미를 잘 이해하고 표현하셨습니다."
        elif score >= 0.4:
            return "괜찮습니다. 하지만 더 정확한 의미를 위해 노력해보세요."
        else:
            return "의미를 다시 한번 생각해보세요. 정답과 차이가 있습니다."
    
    @staticmethod
    def _generate_suggestions(correct_keywords: List[str], user_keywords: List[str], score: float) -> List[str]:
        """개선 제안 생성"""
        suggestions = []
        
        if score < 0.6:
            missing_keywords = set(correct_keywords) - set(user_keywords)
            if missing_keywords:
                suggestions.append(f"다음 키워드를 포함해보세요: {', '.join(list(missing_keywords)[:3])}")
            
            if len(user_keywords) < len(correct_keywords) * 0.5:
                suggestions.append("더 자세한 설명을 추가해보세요.")
        
        if score >= 0.6:
            suggestions.append("잘하고 있습니다! 계속 연습해보세요.")
        
        return suggestions 