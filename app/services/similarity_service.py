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
    
    def calculate_batch_similarity(self, texts1: List[str], texts2: List[str]) -> List[float]:
        """배치로 여러 텍스트 간의 유사도를 계산합니다."""
        try:
            with torch.no_grad():
                embeddings1 = self.model.encode(texts1, convert_to_tensor=True, show_progress_bar=False)
                embeddings2 = self.model.encode(texts2, convert_to_tensor=True, show_progress_bar=False)
                
                similarities = util.pytorch_cos_sim(embeddings1, embeddings2)
                results = [sim.item() for sim in similarities.diagonal()]
                
                # 메모리 정리
                del embeddings1, embeddings2, similarities
                torch.cuda.empty_cache() if torch.cuda.is_available() else None
                
            return results
        except Exception as e:
            print(f"배치 유사도 계산 오류: {e}")
            return [0.0] * len(texts1)

    # ... existing code ...
