from jamo import h2j, j2hcj
import unicodedata

def decompose_korean_word(word):
    decomposed = []
    for char in word:
        if '가' <= char <= '힣':  # 한글 완성자 범위
            jamos = h2j(char)
            decomposed.append(j2hcj(jamos))
        else:
            decomposed.append(char)
    return ''.join(decomposed)

def remove_spaces(text):
    #주어진 텍스트에서 띄어쓰기,?를 제거합니다.
    text = text.replace("?","")
    return text.replace(" ", "")


def compare_korean_words(word1, word2):
    word1 = remove_spaces(word1)
    word2 = remove_spaces(word2)

    decomposed_word1 = decompose_korean_word(word1)
    decomposed_word2 = decompose_korean_word(word2)

    len1 = len(decomposed_word1)
    len2 = len(decomposed_word2)
    min_len = min(len1, len2)

    match_count = 0
    for i in range(min_len):
        if decomposed_word1[i] == decomposed_word2[i]:
            match_count += 1

    accuracy = match_count / max(len1, len2)
    return accuracy

