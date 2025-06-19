from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID

from application.services import VocabListService
from schemas.requests import CreateVocabListRequest, UpdateVocabListRequest, CreateVocabListWithItemsRequest
from schemas.responses import VocabListResponse, VocabListListResponse, ApiResponse
from .dependencies import get_vocab_list_service, verify_access_key

router = APIRouter(prefix="/v1/vocab-list", tags=["vocab-list"])


@router.post("/", response_model=VocabListResponse, status_code=status.HTTP_201_CREATED)
async def create_vocab_list(
    request: CreateVocabListRequest,
    vocab_list_service: VocabListService = Depends(get_vocab_list_service)
):
    """단어장 생성"""
    try:
        vocab_list = await vocab_list_service.create_vocab_list(request)
        return VocabListResponse(
            id=vocab_list.id,
            title=vocab_list.title,
            description=vocab_list.description,
            created_at=vocab_list.created_at,
            expires_at=vocab_list.expires_at,
            access_key=vocab_list.access_key,
            is_deleted=vocab_list.is_deleted,
            tags=vocab_list.tags,
            items=[]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/with-items", response_model=VocabListResponse, status_code=status.HTTP_201_CREATED)
async def create_vocab_list_with_items(
    request: CreateVocabListWithItemsRequest,
    vocab_list_service: VocabListService = Depends(get_vocab_list_service)
):
    """단어장과 단어들을 한 번에 생성 (자동 품사 추출/추측 적용)"""
    try:
        vocab_list = await vocab_list_service.create_vocab_list_with_items(request)
        
        # 단어 목록을 응답에 포함
        from schemas.responses import VocabItemResponse
        items = [VocabItemResponse(
            id=item.id,
            vocab_list_id=item.vocab_list_id,
            word=item.word,
            meaning=item.meaning,
            part_of_speech=item.part_of_speech
        ) for item in vocab_list.items]
        
        return VocabListResponse(
            id=vocab_list.id,
            title=vocab_list.title,
            description=vocab_list.description,
            created_at=vocab_list.created_at,
            expires_at=vocab_list.expires_at,
            access_key=vocab_list.access_key,
            is_deleted=vocab_list.is_deleted,
            tags=vocab_list.tags,
            items=items
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[VocabListListResponse])
async def get_all_vocab_lists(
    tags: Optional[str] = Query(None, description="필터링할 태그들 (쉼표로 구분)"),
    vocab_list_service: VocabListService = Depends(get_vocab_list_service)
):
    """모든 단어장 목록 조회 (삭제되지 않은 것만, 태그 필터링 지원)"""
    try:
        if tags:
            # 쉼표로 구분된 태그를 리스트로 변환
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
            vocab_lists = await vocab_list_service.get_vocab_lists_by_tags(tag_list)
        else:
            vocab_lists = await vocab_list_service.get_all_vocab_lists()
        
        return [
            VocabListListResponse(
                id=vocab_list.id,
                title=vocab_list.title,
                description=vocab_list.description,
                created_at=vocab_list.created_at,
                expires_at=vocab_list.expires_at,
                access_key=vocab_list.access_key,
                is_deleted=vocab_list.is_deleted,
                tags=vocab_list.tags
            )
            for vocab_list in vocab_lists
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{vocab_list_id}", response_model=VocabListResponse)
async def get_vocab_list(
    vocab_list_id: UUID,
    vocab_list_service: VocabListService = Depends(get_vocab_list_service)
):
    """단어장 상세 조회"""
    try:
        vocab_list = await vocab_list_service.get_vocab_list(vocab_list_id)
        if not vocab_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="단어장을 찾을 수 없습니다."
            )
        
        # 단어장에 속한 아이템 목록 포함
        items = []
        if hasattr(vocab_list, "items") and vocab_list.items:
            from schemas.responses import VocabItemResponse
            items = [VocabItemResponse(
                id=item.id,
                vocab_list_id=item.vocab_list_id,
                word=item.word,
                meaning=item.meaning,
                part_of_speech=item.part_of_speech
            ) for item in vocab_list.items]
        return VocabListResponse(
            id=vocab_list.id,
            title=vocab_list.title,
            description=vocab_list.description,
            created_at=vocab_list.created_at,
            expires_at=vocab_list.expires_at,
            access_key=vocab_list.access_key,
            is_deleted=vocab_list.is_deleted,
            tags=vocab_list.tags,
            items=items
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/{vocab_list_id}", response_model=VocabListResponse)
async def update_vocab_list(
    vocab_list_id: UUID,
    request: UpdateVocabListRequest,
    vocab_list_service: VocabListService = Depends(get_vocab_list_service)
):
    """단어장 수정 (Access Key 검증 필요)"""
    try:
        # Access Key 검증
        await verify_access_key(vocab_list_id, request.access_key, vocab_list_service)
        
        vocab_list = await vocab_list_service.update_vocab_list(vocab_list_id, request)
        return VocabListResponse(
            id=vocab_list.id,
            title=vocab_list.title,
            description=vocab_list.description,
            created_at=vocab_list.created_at,
            expires_at=vocab_list.expires_at,
            access_key=vocab_list.access_key,
            is_deleted=vocab_list.is_deleted,
            tags=vocab_list.tags,
            items=[]
        )
    except HTTPException:
        # verify_access_key에서 발생한 HTTPException을 그대로 전달
        raise
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


@router.delete("/{vocab_list_id}", response_model=ApiResponse)
async def delete_vocab_list(
    vocab_list_id: UUID,
    access_key: str = Query(..., description="Access Key"),
    vocab_list_service: VocabListService = Depends(get_vocab_list_service)
):
    """단어장 삭제 (소프트 삭제) - Access Key 검증 필요"""
    try:
        success = await vocab_list_service.delete_vocab_list(vocab_list_id, access_key)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="단어장을 찾을 수 없습니다."
            )
        
        return ApiResponse(
            success=True,
            message="단어장이 성공적으로 삭제되었습니다."
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