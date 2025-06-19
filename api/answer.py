from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from application.services import AnswerService
from schemas.requests import SubmitAnswerRequest
from schemas.responses import AnswerEvaluationResponse, AnswerResponse, ApiResponse
from .dependencies import get_answer_service

router = APIRouter(prefix="/v1", tags=["answer"])


@router.post("/answer", response_model=AnswerEvaluationResponse, status_code=status.HTTP_201_CREATED)
async def submit_answer(
    request: SubmitAnswerRequest,
    answer_service: AnswerService = Depends(get_answer_service)
):
    """답변 제출 및 AI 평가"""
    try:
        evaluation = await answer_service.submit_answer(request)
        return evaluation
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )