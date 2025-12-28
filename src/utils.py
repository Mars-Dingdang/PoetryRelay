from pypinyin import pinyin, Style
import re
import zhconv

def to_simplified(text):
    return zhconv.convert(text, 'zh-cn')

def get_keys(char):
    """
    Get the set of keys for a character to be used in matching.
    Keys include:
    1. The character itself.
    2. The pinyin of the character (without tone).
    """
    keys = set()
    keys.add(char)
    
    # Get pinyin without tone, enable heteronym (polyphones)
    pinyins = pinyin(char, style=Style.NORMAL, heteronym=True)[0]
    for p in pinyins:
        keys.add(p)
        
    return keys

def clean_sentence(sentence):
    """
    Remove punctuation and whitespace.
    """
    # Keep only Chinese characters
    return re.sub(r'[^\u4e00-\u9fa5]', '', sentence)

def split_into_sentences(text):
    """
    Split text into sentences by common Chinese punctuation.
    """
    # Split by comma, period, question mark, exclamation mark (Chinese and English)
    return re.split(r'[，。？！,?!;；]', text)

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]
