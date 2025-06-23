from typing import List, Optional
from uuid import UUID
from datetime import datetime

from domain.repositories import VocabListRepository, VocabItemRepository, AnswerRepository
from domain.models import VocabList, VocabItem, Answer
from .supabase_client import get_supabase_client


class SupabaseVocabListRepository(VocabListRepository):
    async def save(self, vocab_list: VocabList) -> VocabList:
        supabase = get_supabase_client()
        if not supabase:
            raise RuntimeError("Supabase 클라이언트가 초기화되지 않았습니다. 환경 변수를 확인해주세요.")
        
        data = {
            "id": str(vocab_list.id),
            "title": vocab_list.title,
            "description": vocab_list.description,
            "created_at": vocab_list.created_at.isoformat(),
            "expires_at": vocab_list.expires_at.isoformat(),
            "access_key": vocab_list.access_key,
            "is_deleted": vocab_list.is_deleted,
            "tags": vocab_list.tags
        }
        
        result = supabase.table("vocab_lists").upsert(data).execute()
        return vocab_list
    
    async def find_by_id(self, vocab_list_id: UUID) -> Optional[VocabList]:
        supabase = get_supabase_client()
        if not supabase:
            raise RuntimeError("Supabase 클라이언트가 초기화되지 않았습니다. 환경 변수를 확인해주세요.")
        
        result = supabase.table("vocab_lists").select("*").eq("id", str(vocab_list_id)).execute()
        
        if result.data:
            data = result.data[0]
            return VocabList(
                id=UUID(data["id"]),
                title=data["title"],
                description=data["description"],
                created_at=datetime.fromisoformat(data["created_at"]),
                expires_at=datetime.fromisoformat(data["expires_at"]),
                access_key=data["access_key"],
                is_deleted=data["is_deleted"],
                tags=data.get("tags", [])
            )
        return None
    
    async def find_all(self) -> List[VocabList]:
        supabase = get_supabase_client()
        if not supabase:
            raise RuntimeError("Supabase 클라이언트가 초기화되지 않았습니다. 환경 변수를 확인해주세요.")
        
        result = supabase.table("vocab_lists").select("*").eq("is_deleted", False).execute()
        
        vocab_lists = []
        for data in result.data:
            vocab_lists.append(VocabList(
                id=UUID(data["id"]),
                title=data["title"],
                description=data["description"],
                created_at=datetime.fromisoformat(data["created_at"]),
                expires_at=datetime.fromisoformat(data["expires_at"]),
                access_key=data["access_key"],
                is_deleted=data["is_deleted"],
                tags=data.get("tags", [])
            ))
        return vocab_lists
    
    async def find_by_tags(self, tags: List[str]) -> List[VocabList]:
        """태그로 단어장 필터링"""
        supabase = get_supabase_client()
        if not supabase:
            raise RuntimeError("Supabase 클라이언트가 초기화되지 않았습니다. 환경 변수를 확인해주세요.")
        
        # 모든 단어장을 가져온 후 태그로 필터링
        result = supabase.table("vocab_lists").select("*").eq("is_deleted", False).execute()
        
        # 비교를 위해 입력 태그를 소문자/strip 처리
        tags_normalized = [tag.strip().lower() for tag in tags]
        vocab_lists = []
        for data in result.data:
            vocab_list_tags = data.get("tags", [])
            # tags가 문자열로 저장되어 있다면 split
            if isinstance(vocab_list_tags, str):
                vocab_list_tags = [t.strip() for t in vocab_list_tags.split(",") if t.strip()]
            # 태그를 소문자/strip 처리
            vocab_list_tags_normalized = [t.strip().lower() for t in vocab_list_tags]
            # 하나라도 태그가 일치하면 포함
            if any(tag in vocab_list_tags_normalized for tag in tags_normalized):
                vocab_lists.append(VocabList(
                    id=UUID(data["id"]),
                    title=data["title"],
                    description=data["description"],
                    created_at=datetime.fromisoformat(data["created_at"]),
                    expires_at=datetime.fromisoformat(data["expires_at"]),
                    access_key=data["access_key"],
                    is_deleted=data["is_deleted"],
                    tags=vocab_list_tags
                ))
        return vocab_lists
    
    async def delete(self, vocab_list_id: UUID) -> bool:
        supabase = get_supabase_client()
        if not supabase:
            raise RuntimeError("Supabase 클라이언트가 초기화되지 않았습니다. 환경 변수를 확인해주세요.")
        
        # 실제 삭제 대신 is_deleted를 True로 설정
        result = supabase.table("vocab_lists").update({"is_deleted": True}).eq("id", str(vocab_list_id)).execute()
        return len(result.data) > 0


class SupabaseVocabItemRepository(VocabItemRepository):
    async def save(self, vocab_item: VocabItem) -> VocabItem:
        supabase = get_supabase_client()
        if not supabase:
            raise RuntimeError("Supabase 클라이언트가 초기화되지 않았습니다. 환경 변수를 확인해주세요.")
        
        data = {
            "id": str(vocab_item.id),
            "vocab_list_id": str(vocab_item.vocab_list_id),
            "word": vocab_item.word,
            "meaning": vocab_item.meaning,
            "part_of_speech": vocab_item.part_of_speech
        }
        
        result = supabase.table("vocab_items").upsert(data).execute()
        return vocab_item
    
    async def find_by_id(self, vocab_item_id: UUID) -> Optional[VocabItem]:
        supabase = get_supabase_client()
        if not supabase:
            raise RuntimeError("Supabase 클라이언트가 초기화되지 않았습니다. 환경 변수를 확인해주세요.")
        
        result = supabase.table("vocab_items").select("*").eq("id", str(vocab_item_id)).execute()
        
        if result.data:
            data = result.data[0]
            return VocabItem(
                id=UUID(data["id"]),
                vocab_list_id=UUID(data["vocab_list_id"]),
                word=data["word"],
                meaning=data["meaning"],
                part_of_speech=data["part_of_speech"]
            )
        return None
    
    async def find_by_vocab_list_id(self, vocab_list_id: UUID) -> List[VocabItem]:
        supabase = get_supabase_client()
        if not supabase:
            raise RuntimeError("Supabase 클라이언트가 초기화되지 않았습니다. 환경 변수를 확인해주세요.")
        
        result = supabase.table("vocab_items").select("*").eq("vocab_list_id", str(vocab_list_id)).execute()
        
        vocab_items = []
        for data in result.data:
            vocab_items.append(VocabItem(
                id=UUID(data["id"]),
                vocab_list_id=UUID(data["vocab_list_id"]),
                word=data["word"],
                meaning=data["meaning"],
                part_of_speech=data["part_of_speech"]
            ))
        return vocab_items
    
    async def delete(self, vocab_item_id: UUID) -> bool:
        supabase = get_supabase_client()
        if not supabase:
            raise RuntimeError("Supabase 클라이언트가 초기화되지 않았습니다. 환경 변수를 확인해주세요.")
        
        result = supabase.table("vocab_items").delete().eq("id", str(vocab_item_id)).execute()
        return len(result.data) > 0


class SupabaseAnswerRepository(AnswerRepository):
    async def save(self, answer: Answer) -> Answer:
        supabase = get_supabase_client()
        if not supabase:
            raise RuntimeError("Supabase 클라이언트가 초기화되지 않았습니다. 환경 변수를 확인해주세요.")
        
        data = {
            "id": str(answer.id),
            "vocab_item_id": str(answer.vocab_item_id),
            "user_meaning": answer.user_meaning,
            "similarity_score": answer.similarity_score,
            "is_correct": answer.is_correct,
            "created_at": answer.created_at.isoformat()
        }
        
        result = supabase.table("answers").upsert(data).execute()
        return answer
    
    async def find_by_id(self, answer_id: UUID) -> Optional[Answer]:
        supabase = get_supabase_client()
        if not supabase:
            raise RuntimeError("Supabase 클라이언트가 초기화되지 않았습니다. 환경 변수를 확인해주세요.")
        
        result = supabase.table("answers").select("*").eq("id", str(answer_id)).execute()
        
        if result.data:
            data = result.data[0]
            return Answer(
                id=UUID(data["id"]),
                vocab_item_id=UUID(data["vocab_item_id"]),
                user_meaning=data["user_meaning"],
                similarity_score=data["similarity_score"],
                is_correct=data["is_correct"],
                created_at=datetime.fromisoformat(data["created_at"])
            )
        return None
    
    async def find_by_vocab_item_id(self, vocab_item_id: UUID) -> List[Answer]:
        supabase = get_supabase_client()
        if not supabase:
            raise RuntimeError("Supabase 클라이언트가 초기화되지 않았습니다. 환경 변수를 확인해주세요.")
        
        result = supabase.table("answers").select("*").eq("vocab_item_id", str(vocab_item_id)).execute()
        
        answers = []
        for data in result.data:
            answers.append(Answer(
                id=UUID(data["id"]),
                vocab_item_id=UUID(data["vocab_item_id"]),
                user_meaning=data["user_meaning"],
                similarity_score=data["similarity_score"],
                is_correct=data["is_correct"],
                created_at=datetime.fromisoformat(data["created_at"])
            ))
        return answers 