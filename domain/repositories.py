from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from .models import VocabList, VocabItem, Answer


class VocabListRepository(ABC):
    @abstractmethod
    async def save(self, vocab_list: VocabList) -> VocabList:
        pass
    
    @abstractmethod
    async def find_by_id(self, vocab_list_id: UUID) -> Optional[VocabList]:
        pass
    
    @abstractmethod
    async def find_all(self) -> List[VocabList]:
        pass
    
    @abstractmethod
    async def find_by_tags(self, tags: List[str]) -> List[VocabList]:
        """태그로 단어장 필터링"""
        pass
    
    @abstractmethod
    async def delete(self, vocab_list_id: UUID) -> bool:
        pass


class VocabItemRepository(ABC):
    @abstractmethod
    async def save(self, vocab_item: VocabItem) -> VocabItem:
        pass
    
    @abstractmethod
    async def find_by_id(self, vocab_item_id: UUID) -> Optional[VocabItem]:
        pass
    
    @abstractmethod
    async def find_by_vocab_list_id(self, vocab_list_id: UUID) -> List[VocabItem]:
        pass
    
    @abstractmethod
    async def delete(self, vocab_item_id: UUID) -> bool:
        pass


class AnswerRepository(ABC):
    @abstractmethod
    async def save(self, answer: Answer) -> Answer:
        pass
    
    @abstractmethod
    async def find_by_id(self, answer_id: UUID) -> Optional[Answer]:
        pass
    
    @abstractmethod
    async def find_by_vocab_item_id(self, vocab_item_id: UUID) -> List[Answer]:
        pass 