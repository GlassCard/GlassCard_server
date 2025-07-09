import re
from typing import Dict, List, Tuple
from functools import lru_cache
from konlpy.tag import Okt

# konlpy 초기화
okt = Okt()

# 품사 매핑
POS_MAPPING = {
    "Noun": "명사",
    "Verb": "동사", 
    "Adjective": "형용사",
    "Adverb": "부사",
    "Determiner": "관형사",
    "Josa": "조사",
    "Eomi": "어미",
    "Exclamation": "감탄사",
    "감": "Exclamation"
}

def parse_pos_input(text: str) -> Dict[str, List[str]]:
    """품사 정보가 포함된 입력을 파싱합니다."""
    pos_info = {}
    
    # 품사 태그 패턴 매칭
    patterns = [
        r'(\w+)\.\s*([^/\n]+)',  # 동. 사랑하다
        r'(\w+)\.\s*([^/\n]+)\s*/\s*(\w+)\.\s*([^/\n]+)',  # 동. 사랑하다 / 명. 사랑
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if len(match) == 2:  # 단일 품사
                pos, words = match
                pos = POS_MAPPING.get(pos, pos)
                word_list = [word.strip() for word in words.split(',')]
                if pos not in pos_info:
                    pos_info[pos] = []
                pos_info[pos].extend(word_list)
            elif len(match) == 4:  # 다중 품사
                pos1, words1, pos2, words2 = match
                pos1, pos2 = POS_MAPPING.get(pos1, pos1), POS_MAPPING.get(pos2, pos2)
                word_list1 = [word.strip() for word in words1.split(',')]
                word_list2 = [word.strip() for word in words2.split(',')]
                
                if pos1 not in pos_info:
                    pos_info[pos1] = []
                if pos2 not in pos_info:
                    pos_info[pos2] = []
                    
                pos_info[pos1].extend(word_list1)
                pos_info[pos2].extend(word_list2)
    
    return pos_info

def parse_comma_separated_input(text: str) -> List[str]:
    """쉼표로 구분된 입력을 파싱합니다. (콤마 기준 분리, 각 단어의 앞뒤 공백 제거)"""
    if not text:
        return []
    
    # 콤마로 분리하고 각 단어의 앞뒤 공백만 제거
    words = [word.strip() for word in text.split(',')]
    return [word for word in words if word]

def extract_words_from_pos_input(text: str) -> List[str]:
    """품사 정보가 포함된 입력에서 단어만 추출합니다."""
    pos_info = parse_pos_input(text)
    words = []
    for pos_words in pos_info.values():
        words.extend(pos_words)
    return words

def check_incomplete_pos_input(text: str) -> Dict:
    """불완전한 품사 입력인지 확인합니다."""
    incomplete_patterns = [
        r'^\w+\.\s*$',  # 동.
        r'^\w+\.\s*/\s*$',  # 동. /
        r'^\w+\.\s*/\s*\w+\.\s*$',  # 동. / 명.
    ]
    
    for pattern in incomplete_patterns:
        if re.match(pattern, text.strip()):
            pos_tag = re.match(r'^(\w+)\.', text.strip()).group(1)
            return {
                "is_incomplete": True,
                "pos_tag": pos_tag,
                "message": f"품사 태그 '{pos_tag}.' 뒤에 단어를 입력해주세요."
            }
    
    return {"is_incomplete": False}

@lru_cache(maxsize=500)
def analyze_pos_cached(text: str) -> Tuple[Tuple[str, str], ...]:
    """캐시된 품사 분석"""
    try:
        pos_result = okt.pos(text)
        return tuple(pos_result)  # 튜플로 변환하여 캐시 가능하게
    except Exception as e:
        print(f"품사 분석 중 오류 발생: {e}")
        return tuple()

def analyze_pos(text: str) -> List[Tuple[str, str]]:
    """한국어 텍스트의 품사를 분석합니다 (캐시 사용)"""
    return list(analyze_pos_cached(text))

def extract_keywords(text: str) -> List[str]:
    """텍스트에서 키워드를 추출합니다"""
    try:
        pos_result = okt.pos(text)
        keywords = []
        
        for word, pos in pos_result:
            if pos in ['Noun', 'Verb', 'Adjective']:
                keywords.append(word)
        
        return keywords
    except Exception as e:
        print(f"키워드 추출 중 오류 발생: {e}")
        return []

@lru_cache(maxsize=500)
def extract_keywords_cached(text: str) -> Tuple[str, ...]:
    """캐시된 키워드 추출"""
    return tuple(extract_keywords(text)) 