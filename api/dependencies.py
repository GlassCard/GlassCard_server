from fastapi import Depends, HTTPException, status
from typing import Optional
from uuid import UUID

from infrastructure.repositories import (
    SupabaseVocabListRepository, 
    SupabaseVocabItemRepository, 
    SupabaseAnswerRepository
)
from application.services import VocabListService, VocabItemService, AnswerService


# Repository 의존성
def get_vocab_list_repository() -> SupabaseVocabListRepository:
    return SupabaseVocabListRepository()


def get_vocab_item_repository() -> SupabaseVocabItemRepository:
    return SupabaseVocabItemRepository()


def get_answer_repository() -> SupabaseAnswerRepository:
    return SupabaseAnswerRepository()


# Service 의존성
def get_vocab_list_service(
    vocab_list_repo: SupabaseVocabListRepository = Depends(get_vocab_list_repository),
    vocab_item_repo: SupabaseVocabItemRepository = Depends(get_vocab_item_repository)
) -> VocabListService:
    return VocabListService(vocab_list_repo, vocab_item_repo)


def get_vocab_item_service(
    vocab_item_repo: SupabaseVocabItemRepository = Depends(get_vocab_item_repository),
    vocab_list_repo: SupabaseVocabListRepository = Depends(get_vocab_list_repository)
) -> VocabItemService:
    return VocabItemService(vocab_item_repo, vocab_list_repo)


def get_answer_service(
    answer_repo: SupabaseAnswerRepository = Depends(get_answer_repository),
    vocab_item_repo: SupabaseVocabItemRepository = Depends(get_vocab_item_repository)
) -> AnswerService:
    return AnswerService(answer_repo, vocab_item_repo)


# Access Key 검증 의존성
async def verify_access_key(
    vocab_list_id: UUID,
    access_key: str,
    vocab_list_service: VocabListService = Depends(get_vocab_list_service)
) -> bool:
    """Access Key를 검증하여 단어장 수정/삭제 권한을 확인합니다."""
    vocab_list = await vocab_list_service.get_vocab_list(vocab_list_id)
    if not vocab_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="단어장을 찾을 수 없습니다."
        )
    
    if vocab_list.access_key != access_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Key가 올바르지 않습니다."
        )
    
    return True 