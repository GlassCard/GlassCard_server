from typing import List
from .word_database import WordDatabase

class AutoLearningSystem:
    def __init__(self, word_db: WordDatabase):
        self.word_db = word_db
        self.learning_threshold = 0.7  # 학습 임계값
        self.max_auto_words = 1000  # 최대 자동 학습 단어 수
        
    def should_learn_word(self, user_input: str, meaning: str, score: float) -> bool:
        """단어를 자동 학습할지 결정합니다."""
        # 이미 데이터베이스에 있는지 확인
        existing_words = self.word_db.find_best_match(user_input, [user_input], top_k=1)
        if existing_words and existing_words[0]["total_score"] > 0.9:
            return False
        
        # 점수가 임계값을 넘고, 데이터베이스 크기가 제한을 넘지 않았는지 확인
        return (score > self.learning_threshold and 
                len(self.word_db.words) < self.max_auto_words)
    
    def auto_learn_word(self, user_input: str, meaning: str, pos: str = None, keywords: List[str] = None) -> bool:
        """단어를 자동으로 학습합니다."""
        try:
            # 단어 추가
            word_id = self.word_db.add_word(user_input, meaning, pos, keywords)
            print(f"자동 학습: '{user_input}' -> '{meaning}' (ID: {word_id})")
            return True
        except Exception as e:
            print(f"자동 학습 실패: {e}")
            return False 