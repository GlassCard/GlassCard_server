from typing import List, Optional
from uuid import UUID
from uuid import uuid4
from datetime import datetime

from domain.models import VocabList, VocabItem, Answer
from domain.repositories import VocabListRepository, VocabItemRepository, AnswerRepository
from infrastructure.ai_service import AIService
from infrastructure.utils import process_vocab_item_data
from schemas.requests import CreateVocabListRequest, UpdateVocabListRequest, CreateVocabItemRequest, SubmitAnswerRequest, CreateVocabListWithItemsRequest
from schemas.responses import VocabListResponse, VocabItemResponse, AnswerResponse, AnswerEvaluationResponse


class VocabListService:
    def __init__(self, vocab_list_repository: VocabListRepository, vocab_item_repository: VocabItemRepository):
        self.vocab_list_repository = vocab_list_repository
        self.vocab_item_repository = vocab_item_repository
    
    async def create_vocab_list(self, request: CreateVocabListRequest) -> VocabList:
        """단어장 생성"""
        vocab_list = VocabList.create(
            title=request.title,
            description=request.description,
            expires_at=request.expires_at,
            access_key=request.access_key,
            tags=request.tags
        )
        return await self.vocab_list_repository.save(vocab_list)
    
    async def create_vocab_list_with_items(self, request: CreateVocabListWithItemsRequest) -> VocabList:
        """단어장과 단어들을 한 번에 생성"""
        # 1. 단어장 생성
        vocab_list = VocabList.create(
            title=request.title,
            description=request.description,
            expires_at=request.expires_at,
            access_key=request.access_key,
            tags=request.tags
        )
        saved_vocab_list = await self.vocab_list_repository.save(vocab_list)
        
        # 2. 단어들 생성 (자동 품사 추출 적용)
        vocab_items = []
        for item_data in request.items:
            # 자동 품사 추출 및 의미 정리
            cleaned_word, cleaned_meaning, extracted_pos = process_vocab_item_data(
                item_data.word, 
                item_data.meaning, 
                item_data.part_of_speech
            )
            
            vocab_item = VocabItem.create(
                vocab_list_id=saved_vocab_list.id,
                word=cleaned_word,
                meaning=cleaned_meaning,
                part_of_speech=extracted_pos
            )
            saved_item = await self.vocab_item_repository.save(vocab_item)
            vocab_items.append(saved_item)
        
        # 3. 단어장에 단어 목록 추가
        saved_vocab_list.items = vocab_items
        return saved_vocab_list
    
    async def update_vocab_list(self, vocab_list_id: UUID, request: UpdateVocabListRequest) -> VocabList:
        """단어장 수정"""
        vocab_list = await self.vocab_list_repository.find_by_id(vocab_list_id)
        if not vocab_list:
            raise ValueError(f"단어장을 찾을 수 없습니다: {vocab_list_id}")
        
        # Access Key 검증
        if vocab_list.access_key != request.access_key:
            raise ValueError("Access Key가 올바르지 않습니다.")
        
        # 필드 업데이트
        if request.title is not None:
            vocab_list.title = request.title
        if request.description is not None:
            vocab_list.description = request.description
        if request.expires_at is not None:
            vocab_list.expires_at = request.expires_at
        if request.tags is not None:
            vocab_list.tags = request.tags
        
        return await self.vocab_list_repository.save(vocab_list)
    
    async def get_vocab_list(self, vocab_list_id: UUID) -> Optional[VocabList]:
        """단어장 조회"""
        vocab_list = await self.vocab_list_repository.find_by_id(vocab_list_id)
        if vocab_list:
            # 단어장에 속한 아이템들도 함께 조회
            items = await self.vocab_item_repository.find_by_vocab_list_id(vocab_list_id)
            vocab_list.items = items
        return vocab_list
    
    async def get_all_vocab_lists(self) -> List[VocabList]:
        """모든 단어장 목록 조회 (삭제되지 않은 것만)"""
        return await self.vocab_list_repository.find_all()
    
    async def get_vocab_lists_by_tags(self, tags: List[str]) -> List[VocabList]:
        """태그로 단어장 필터링"""
        return await self.vocab_list_repository.find_by_tags(tags)
    
    async def delete_vocab_list(self, vocab_list_id: UUID, access_key: str) -> bool:
        """단어장 삭제 (소프트 삭제) - Access Key 검증 포함"""
        vocab_list = await self.vocab_list_repository.find_by_id(vocab_list_id)
        if not vocab_list:
            raise ValueError(f"단어장을 찾을 수 없습니다: {vocab_list_id}")
        
        # Access Key 검증
        if vocab_list.access_key != access_key:
            raise ValueError("Access Key가 올바르지 않습니다.")
        
        return await self.vocab_list_repository.delete(vocab_list_id)


class VocabItemService:
    def __init__(self, vocab_item_repository: VocabItemRepository, vocab_list_repository: VocabListRepository):
        self.vocab_item_repository = vocab_item_repository
        self.vocab_list_repository = vocab_list_repository
    
    async def add_vocab_item(self, vocab_list_id: UUID, request: CreateVocabItemRequest, access_key: str) -> VocabItem:
        """단어 추가 - Access Key 검증 포함"""
        # 단어장 존재 확인 및 Access Key 검증
        vocab_list = await self.vocab_list_repository.find_by_id(vocab_list_id)
        if not vocab_list:
            raise ValueError(f"단어장을 찾을 수 없습니다: {vocab_list_id}")
        
        if vocab_list.access_key != access_key:
            raise ValueError("Access Key가 올바르지 않습니다.")
        
        # 자동 품사 추출 및 의미 정리
        cleaned_word, cleaned_meaning, extracted_pos = process_vocab_item_data(
            request.word, 
            request.meaning, 
            request.part_of_speech
        )
        
        vocab_item = VocabItem.create(
            vocab_list_id=vocab_list_id,
            word=cleaned_word,
            meaning=cleaned_meaning,
            part_of_speech=extracted_pos
        )
        return await self.vocab_item_repository.save(vocab_item)
    
    async def get_vocab_item(self, vocab_item_id: UUID) -> Optional[VocabItem]:
        """단어 조회"""
        return await self.vocab_item_repository.find_by_id(vocab_item_id)
    
    async def get_vocab_list_items(self, vocab_list_id: UUID) -> List[VocabItem]:
        """단어장의 단어 목록 조회"""
        return await self.vocab_item_repository.find_by_vocab_list_id(vocab_list_id)
    
    async def delete_vocab_item(self, vocab_item_id: UUID, access_key: str) -> bool:
        """단어 삭제 - Access Key 검증 포함"""
        vocab_item = await self.vocab_item_repository.find_by_id(vocab_item_id)
        if not vocab_item:
            raise ValueError(f"단어를 찾을 수 없습니다: {vocab_item_id}")
        
        # 단어장의 Access Key 검증
        vocab_list = await self.vocab_list_repository.find_by_id(vocab_item.vocab_list_id)
        if not vocab_list:
            raise ValueError(f"단어장을 찾을 수 없습니다: {vocab_item.vocab_list_id}")
        
        if vocab_list.access_key != access_key:
            raise ValueError("Access Key가 올바르지 않습니다.")
        
        return await self.vocab_item_repository.delete(vocab_item_id)


class AnswerService:
    def __init__(self, answer_repository: AnswerRepository, vocab_item_repository: VocabItemRepository):
        self.answer_repository = answer_repository
        self.vocab_item_repository = vocab_item_repository
    
    async def submit_answer(self, request: SubmitAnswerRequest) -> AnswerEvaluationResponse:
        """답변 제출 및 AI 평가 (DB 저장 없이 실시간 평가만)"""
        # 단어 아이템 조회
        vocab_item = await self.vocab_item_repository.find_by_id(request.vocab_item_id)
        if not vocab_item:
            raise ValueError(f"단어를 찾을 수 없습니다: {request.vocab_item_id}")
        
        # AI 평가 수행
        similarity_score, is_correct, feedback, suggestions = AIService.evaluate_similarity(
            correct_meaning=vocab_item.meaning,
            user_meaning=request.user_meaning
        )
        
        # 점수에 따른 평가 결과 결정
        if similarity_score >= 0.8:
            evaluation_result = "Correct"
        elif similarity_score >= 0.6:
            evaluation_result = "Flexible"
        else:
            evaluation_result = "Incorrect"
        
        # 응답 생성 (DB 저장 없이)
        return AnswerEvaluationResponse(
            answer=AnswerResponse(
                id=uuid4(),  # 임시 ID
                vocab_item_id=request.vocab_item_id,
                user_meaning=request.user_meaning,
                similarity_score=similarity_score,
                is_correct=is_correct,
                created_at=datetime.utcnow()
            ),
            feedback=feedback,
            suggestions=suggestions,
            evaluation_result=evaluation_result  # 새로운 필드 추가
        )
    
    async def get_item_answers(self, vocab_item_id: UUID) -> List[Answer]:
        """단어의 답변 목록 조회 (DB 없이 빈 리스트 반환)"""
        # DB 저장을 하지 않으므로 빈 리스트 반환
        return [] 