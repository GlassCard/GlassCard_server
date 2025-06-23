from typing import Dict, List
from sentence_transformers import SentenceTransformer, util

class WordDatabase:
    def __init__(self, model: SentenceTransformer):
        self.model = model
        self.words = {}  # {word_id: {"word": "단어", "meaning": "의미", "pos": "품사", "embedding": tensor}}
        self.word_id_counter = 1
        self.meaning_to_ids = {}  # {meaning: [word_ids]}
        self.word_to_ids = {}  # {word: [word_ids]}
        
    def add_word(self, word: str, meaning: str, pos: str = None, keywords: List[str] = None) -> int:
        """단어를 데이터베이스에 추가합니다."""
        word_id = self.word_id_counter
        self.word_id_counter += 1
        
        # 임베딩 계산
        try:
            embedding = self.model.encode(word, convert_to_tensor=True)
        except Exception as e:
            print(f"임베딩 계산 오류: {e}")
            embedding = None
        
        # 단어 정보 저장
        self.words[word_id] = {
            "word": word,
            "meaning": meaning,
            "pos": pos,
            "embedding": embedding,
            "keywords": keywords or []
        }
        
        # 인덱스 업데이트
        if meaning not in self.meaning_to_ids:
            self.meaning_to_ids[meaning] = []
        self.meaning_to_ids[meaning].append(word_id)
        
        if word not in self.word_to_ids:
            self.word_to_ids[word] = []
        self.word_to_ids[word].append(word_id)
        
        return word_id
    
    def find_best_match(self, user_input: str, user_words: List[str], top_k: int = 5) -> List[Dict]:
        """사용자 입력과 가장 잘 매칭되는 단어들을 찾습니다."""
        if not self.words:
            return []
        
        # 사용자 입력 임베딩 계산
        try:
            user_embeddings = self.model.encode(user_words, convert_to_tensor=True, show_progress_bar=False)
        except Exception as e:
            print(f"사용자 입력 임베딩 오류: {e}")
            return []
        
        # 모든 단어와 유사도 계산 (배치 처리)
        all_similarities = []
        
        for word_id, word_info in self.words.items():
            if word_info["embedding"] is None:
                continue
                
            # 각 사용자 단어와의 최대 유사도
            max_similarity = 0.0
            for user_embedding in user_embeddings:
                try:
                    similarity = util.pytorch_cos_sim(user_embedding, word_info["embedding"]).item()
                    max_similarity = max(max_similarity, similarity)
                except Exception as e:
                    continue
            
            # 종합 점수 (동의어, 키워드 등은 외부에서 계산)
            total_score = max_similarity
            
            all_similarities.append({
                "word_id": word_id,
                "word": word_info["word"],
                "meaning": word_info["meaning"],
                "pos": word_info["pos"],
                "similarity": max_similarity,
                "total_score": total_score
            })
        
        # 점수순으로 정렬하고 상위 k개 반환
        all_similarities.sort(key=lambda x: x["total_score"], reverse=True)
        return all_similarities[:top_k]
    
    def get_word_by_id(self, word_id: int) -> Dict:
        """ID로 단어 정보를 가져옵니다."""
        return self.words.get(word_id, {})
    
    def get_stats(self) -> Dict:
        """데이터베이스 통계를 반환합니다."""
        return {
            "total_words": len(self.words),
            "total_meanings": len(self.meaning_to_ids),
            "total_unique_words": len(self.word_to_ids)
        } 