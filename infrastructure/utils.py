import re
from typing import Optional, List, Tuple


def extract_part_of_speech_from_meaning(meaning: str) -> Optional[str]:
    """
    의미 텍스트에서 품사 정보를 자동으로 추출합니다.
    
    예시:
    - "명. 사랑, 사랑애/동. 사랑하다" → "noun/verb"
    - "N. love/V. love" → "noun/verb"
    - "형. 아름다운" → "adjective"
    - "adj. beautiful" → "adjective"
    - "부. 매우" → "adverb"
    - "adv. very" → "adverb"
    - "동. 달리다" → "verb"
    - "v. run" → "verb"
    - "명. 행복" → "noun"
    - "n. happiness" → "noun"
    """
    if not meaning:
        return None
    
    # 품사 패턴 정의 (한국어 + 영어)
    pos_patterns = {
        # 한국어 품사
        r'명\.': 'noun',
        r'동\.': 'verb', 
        r'형\.': 'adjective',
        r'부\.': 'adverb',
        r'전\.': 'preposition',
        r'접\.': 'conjunction',
        r'감\.': 'interjection',
        r'대\.': 'pronoun',
        r'관\.': 'article',
        r'수\.': 'numeral',
        
        # 영어 품사 (대소문자 구분 없음)
        r'\bN\.': 'noun',
        r'\bn\.': 'noun',
        r'\bV\.': 'verb',
        r'\bv\.': 'verb',
        r'\bADJ\.': 'adjective',
        r'\bAdj\.': 'adjective',
        r'\badj\.': 'adjective',
        r'\bADV\.': 'adverb',
        r'\bAdv\.': 'adverb',
        r'\badv\.': 'adverb',
        r'\bPREP\.': 'preposition',
        r'\bPrep\.': 'preposition',
        r'\bprep\.': 'preposition',
        r'\bCONJ\.': 'conjunction',
        r'\bConj\.': 'conjunction',
        r'\bconj\.': 'conjunction',
        r'\bINT\.': 'interjection',
        r'\bInt\.': 'interjection',
        r'\bint\.': 'interjection',
        r'\bPRON\.': 'pronoun',
        r'\bPron\.': 'pronoun',
        r'\bpron\.': 'pronoun',
        r'\bART\.': 'article',
        r'\bArt\.': 'article',
        r'\bart\.': 'article',
        r'\bNUM\.': 'numeral',
        r'\bNum\.': 'numeral',
        r'\bnum\.': 'numeral'
    }
    
    found_pos = []
    
    # 각 품사 패턴을 검사
    for pattern, pos in pos_patterns.items():
        if re.search(pattern, meaning):
            found_pos.append(pos)
    
    # 중복 제거하고 정렬
    unique_pos = sorted(list(set(found_pos)))
    
    if unique_pos:
        return '/'.join(unique_pos)
    
    return None


def guess_part_of_speech_from_meaning(meaning: str) -> Optional[str]:
    """
    품사 표기가 없는 경우 의미를 분석해서 품사를 추측합니다.
    
    예시:
    - "사랑" → "noun" (명사로 추측)
    - "달리다" → "verb" (동사로 추측)
    - "아름다운" → "adjective" (형용사로 추측)
    - "빠르게" → "adverb" (부사로 추측)
    """
    if not meaning:
        return None
    
    # 한국어 품사 추측 패턴
    korean_patterns = {
        # 동사 패턴 (하다, 되다, 이다, 있다, 없다 등)
        r'하다$|되다$|이다$|있다$|없다$|되다$|하다$|거리다$|스럽다$|롭다$|답다$': 'verb',
        
        # 형용사 패턴 (다로 끝나는 것들 중 동사가 아닌 것)
        r'다$': 'adjective',
        
        # 부사 패턴 (게, 히, 이, 로, 으로 등으로 끝나는 것)
        r'게$|히$|이$|로$|으로$|스럽게$|롭게$|답게$': 'adverb',
        
        # 감탄사 패턴 (와, 오, 어, 아 등)
        r'^와$|^오$|^어$|^아$|^으$|^음$|^응$': 'interjection',
        
        # 수사 패턴 (숫자)
        r'^[0-9]+$|^[일이삼사오육칠팔구십백천만억]+$': 'numeral',
        
        # 대명사 패턴 (나, 너, 그, 이, 저 등)
        r'^나$|^너$|^그$|^이$|^저$|^우리$|^너희$|^그들$|^이것$|^저것$': 'pronoun',
        
        # 전치사/접속사 패턴 (에서, 에, 와, 과, 그리고, 또는 등)
        r'^에서$|^에$|^와$|^과$|^그리고$|^또는$|^하지만$|^만약$': 'preposition'
    }
    
    # 영어 품사 추측 패턴
    english_patterns = {
        # 동사 패턴 (ing, ed, s로 끝나는 것들)
        r'ing$|ed$|s$': 'verb',
        
        # 형용사 패턴 (ful, ous, al, ive, able, ible 등)
        r'ful$|ous$|al$|ive$|able$|ible$|ic$|ical$|ish$|less$': 'adjective',
        
        # 부사 패턴 (ly로 끝나는 것)
        r'ly$': 'adverb',
        
        # 감탄사 패턴 (wow, oh, ah, oops 등)
        r'^wow$|^oh$|^ah$|^oops$|^ouch$|^hmm$|^uh$': 'interjection',
        
        # 수사 패턴 (숫자)
        r'^[0-9]+$|^one$|^two$|^three$|^first$|^second$|^third$': 'numeral',
        
        # 대명사 패턴 (I, you, he, she, it, we, they 등)
        r'^I$|^you$|^he$|^she$|^it$|^we$|^they$|^this$|^that$|^these$|^those$': 'pronoun',
        
        # 전치사/접속사 패턴 (in, on, at, and, or, but 등)
        r'^in$|^on$|^at$|^and$|^or$|^but$|^if$|^when$|^where$|^why$|^how$': 'preposition'
    }
    
    # 한국어 패턴 검사
    for pattern, pos in korean_patterns.items():
        if re.search(pattern, meaning, re.IGNORECASE):
            return pos
    
    # 영어 패턴 검사
    for pattern, pos in english_patterns.items():
        if re.search(pattern, meaning, re.IGNORECASE):
            return pos
    
    # 기본적으로 명사로 추측 (가장 일반적인 품사)
    return 'noun'


def clean_meaning_text(meaning: str) -> str:
    """
    의미 텍스트에서 품사 표시를 제거하고 깔끔하게 정리합니다.
    
    예시:
    - "명. 사랑, 사랑애/동. 사랑하다" → "사랑, 사랑애/사랑하다"
    - "N. love/V. love" → "love/love"
    """
    if not meaning:
        return meaning
    
    # 품사 패턴 제거 (한국어 + 영어)
    pos_patterns = [
        # 한국어 품사
        r'명\.\s*', r'동\.\s*', r'형\.\s*', r'부\.\s*', 
        r'전\.\s*', r'접\.\s*', r'감\.\s*', r'대\.\s*',
        r'관\.\s*', r'수\.\s*',
        
        # 영어 품사 (대소문자 구분 없음)
        r'\bN\.\s*', r'\bn\.\s*',
        r'\bV\.\s*', r'\bv\.\s*',
        r'\bADJ\.\s*', r'\bAdj\.\s*', r'\badj\.\s*',
        r'\bADV\.\s*', r'\bAdv\.\s*', r'\badv\.\s*',
        r'\bPREP\.\s*', r'\bPrep\.\s*', r'\bprep\.\s*',
        r'\bCONJ\.\s*', r'\bConj\.\s*', r'\bconj\.\s*',
        r'\bINT\.\s*', r'\bInt\.\s*', r'\bint\.\s*',
        r'\bPRON\.\s*', r'\bPron\.\s*', r'\bpron\.\s*',
        r'\bART\.\s*', r'\bArt\.\s*', r'\bart\.\s*',
        r'\bNUM\.\s*', r'\bNum\.\s*', r'\bnum\.\s*'
    ]
    
    cleaned_meaning = meaning
    for pattern in pos_patterns:
        cleaned_meaning = re.sub(pattern, '', cleaned_meaning)
    
    return cleaned_meaning.strip()


def process_vocab_item_data(word: str, meaning: str, part_of_speech: Optional[str] = None) -> Tuple[str, str, Optional[str]]:
    """
    단어 데이터를 처리하여 품사를 자동으로 추출하고 의미를 정리합니다.
    
    Returns:
        Tuple[cleaned_word, cleaned_meaning, extracted_part_of_speech]
    """
    # 품사가 이미 제공된 경우 그대로 사용
    if part_of_speech:
        return word.strip(), meaning.strip(), part_of_speech
    
    # 의미에서 품사 추출
    extracted_pos = extract_part_of_speech_from_meaning(meaning)
    
    # 품사 표기가 없는 경우 추측
    if not extracted_pos:
        extracted_pos = guess_part_of_speech_from_meaning(meaning)
    
    # 의미 텍스트 정리 (품사 표시 제거)
    cleaned_meaning = clean_meaning_text(meaning)
    
    return word.strip(), cleaned_meaning, extracted_pos 