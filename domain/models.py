from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
from dataclasses import dataclass, field


@dataclass
class VocabList:
    id: UUID
    title: str
    description: Optional[str]
    created_at: datetime
    expires_at: datetime
    access_key: str
    user_id: Optional[UUID] = None  # 로그인 없이 사용하므로 Optional
    is_deleted: bool = False
    tags: List[str] = field(default_factory=list)  # 태그 리스트 추가
    items: List["VocabItem"] = field(default_factory=list)
    
    @classmethod
    def create(cls, title: str, description: Optional[str], expires_at: datetime, access_key: str, tags: Optional[List[str]] = None) -> "VocabList":
        return cls(
            id=uuid4(),
            title=title,
            description=description,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
            access_key=access_key,
            tags=tags or []  # 태그가 없으면 빈 리스트
        )
    
    def add_item(self, word: str, meaning: str, part_of_speech: Optional[str] = None) -> "VocabItem":
        item = VocabItem.create(self.id, word, meaning, part_of_speech)
        self.items.append(item)
        return item
    
    def get_item(self, item_id: UUID) -> Optional["VocabItem"]:
        return next((item for item in self.items if item.id == item_id), None)


@dataclass
class VocabItem:
    id: UUID
    vocab_list_id: UUID
    word: str
    meaning: str
    part_of_speech: Optional[str]
    answers: List["Answer"] = field(default_factory=list)
    
    @classmethod
    def create(cls, vocab_list_id: UUID, word: str, meaning: str, part_of_speech: Optional[str] = None) -> "VocabItem":
        return cls(
            id=uuid4(),
            vocab_list_id=vocab_list_id,
            word=word,
            meaning=meaning,
            part_of_speech=part_of_speech
        )
    
    def add_answer(self, user_meaning: str, similarity_score: float, is_correct: bool) -> "Answer":
        answer = Answer.create(self.id, user_meaning, similarity_score, is_correct)
        self.answers.append(answer)
        return answer


@dataclass
class Answer:
    id: UUID
    vocab_item_id: UUID
    user_meaning: str
    similarity_score: float
    is_correct: bool
    created_at: datetime
    
    @classmethod
    def create(cls, vocab_item_id: UUID, user_meaning: str, similarity_score: float, is_correct: bool) -> "Answer":
        return cls(
            id=uuid4(),
            vocab_item_id=vocab_item_id,
            user_meaning=user_meaning,
            similarity_score=similarity_score,
            is_correct=is_correct,
            created_at=datetime.utcnow()
        ) 