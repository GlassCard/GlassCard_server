from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class CreateVocabListRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="단어장 제목")
    description: Optional[str] = Field(None, max_length=500, description="단어장 설명")
    expires_at: datetime = Field(..., description="만료 날짜")
    access_key: str = Field(..., min_length=1, max_length=50, description="Access Key")
    tags: Optional[List[str]] = Field(default_factory=list, description="태그 목록")


class UpdateVocabListRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="단어장 제목")
    description: Optional[str] = Field(None, max_length=500, description="단어장 설명")
    expires_at: Optional[datetime] = Field(None, description="만료 날짜")
    access_key: str = Field(..., min_length=1, max_length=50, description="Access Key")
    tags: Optional[List[str]] = Field(None, description="태그 목록")


class VocabItemData(BaseModel):
    word: str = Field(..., min_length=1, max_length=100, description="단어")
    meaning: str = Field(..., min_length=1, max_length=500, description="정답 의미")
    part_of_speech: Optional[str] = Field(None, max_length=50, description="품사")


class CreateVocabItemRequest(BaseModel):
    word: str = Field(..., min_length=1, max_length=100, description="단어")
    meaning: str = Field(..., min_length=1, max_length=500, description="정답 의미")
    part_of_speech: Optional[str] = Field(None, max_length=50, description="품사")


class CreateVocabListWithItemsRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="단어장 제목")
    description: Optional[str] = Field(None, max_length=500, description="단어장 설명")
    expires_at: datetime = Field(..., description="만료 날짜")
    access_key: str = Field(..., min_length=1, max_length=50, description="Access Key")
    tags: Optional[List[str]] = Field(default_factory=list, description="태그 목록")
    items: List[CreateVocabItemRequest] = Field(..., description="단어 목록")


class SubmitAnswerRequest(BaseModel):
    vocab_item_id: UUID = Field(..., description="단어 아이템 ID")
    user_meaning: str = Field(..., min_length=1, max_length=500, description="사용자가 작성한 의미")


class CreateUserRequest(BaseModel):
    email: str = Field(..., description="사용자 이메일") 