from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from uuid import UUID

from application.services import VocabItemService
from schemas.requests import CreateVocabItemRequest
from schemas.responses import VocabItemResponse, ApiResponse
from .dependencies import get_vocab_item_service

router = APIRouter(prefix="/v1/vocab-list", tags=["vocab-item"])


@router.post("/{vocab_list_id}/items", response_model=VocabItemResponse, status_code=status.HTTP_201_CREATED)
async def add_vocab_item(
    vocab_list_id: UUID,
    request: CreateVocabItemRequest,
    access_key: str = Query(..., description="Access Key"),
    vocab_item_service: VocabItemService = Depends(get_vocab_item_service)
):
    """단어 추가 (Access Key 검증 필요)"""
    try:
        vocab_item = await vocab_item_service.add_vocab_item(vocab_list_id, request, access_key)
        return VocabItemResponse(
            id=vocab_item.id,
            vocab_list_id=vocab_item.vocab_list_id,
            word=vocab_item.word,
            meaning=vocab_item.meaning,
            part_of_speech=vocab_item.part_of_speech
        )
    except ValueError as e:
        if "Access Key가 올바르지 않습니다" in str(e):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{vocab_list_id}/items", response_model=List[VocabItemResponse])
async def get_vocab_list_items(
    vocab_list_id: UUID,
    vocab_item_service: VocabItemService = Depends(get_vocab_item_service)
):
    """단어장의 단어 목록 조회"""
    try:
        vocab_items = await vocab_item_service.get_vocab_list_items(vocab_list_id)
        return [
            VocabItemResponse(
                id=item.id,
                vocab_list_id=item.vocab_list_id,
                word=item.word,
                meaning=item.meaning,
                part_of_speech=item.part_of_speech
            )
            for item in vocab_items
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/items/{vocab_item_id}", response_model=ApiResponse)
async def delete_vocab_item(
    vocab_item_id: UUID,
    access_key: str = Query(..., description="Access Key"),
    vocab_item_service: VocabItemService = Depends(get_vocab_item_service)
):
    """단어 삭제 (Access Key 검증 필요)"""
    try:
        success = await vocab_item_service.delete_vocab_item(vocab_item_id, access_key)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="단어를 찾을 수 없습니다."
            )
        
        return ApiResponse(
            success=True,
            message="단어가 성공적으로 삭제되었습니다."
        )
    except ValueError as e:
        if "Access Key가 올바르지 않습니다" in str(e):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 