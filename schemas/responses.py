from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class VocabItemResponse(BaseModel):
    id: UUID
    vocab_list_id: UUID
    word: str
    meaning: str
    part_of_speech: Optional[str] = None
    
    class Config:
        from_attributes = True


class VocabListResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    user_id: Optional[UUID] = None  # 로그인 없이 사용하므로 Optional
    created_at: datetime
    expires_at: datetime
    access_key: str
    is_deleted: bool
    tags: List[str] = []  # 태그 필드 추가
    items: List[VocabItemResponse] = []
    
    class Config:
        from_attributes = True


class VocabListListResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    user_id: Optional[UUID] = None  # 로그인 없이 사용하므로 Optional
    created_at: datetime
    expires_at: datetime
    access_key: str
    is_deleted: bool
    tags: List[str] = []  # 태그 필드 추가


class AnswerResponse(BaseModel):
    id: UUID
    vocab_item_id: UUID
    user_meaning: str
    similarity_score: float
    is_correct: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class VocabListDetailResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    user_id: Optional[UUID] = None  # 로그인 없이 사용하므로 Optional
    created_at: datetime
    expires_at: datetime
    access_key: str
    is_deleted: bool
    items: List[VocabItemResponse] = []
    answers: List[AnswerResponse] = []
    
    class Config:
        from_attributes = True


class AnswerEvaluationResponse(BaseModel):
    answer: AnswerResponse
    feedback: str = Field(..., description="AI 피드백")
    suggestions: Optional[List[str]] = None
    evaluation_result: str = Field(..., description="평가 결과: Correct, Flexible, Incorrect")
    
    class Config:
        from_attributes = True


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None 