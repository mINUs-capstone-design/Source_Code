from jamo import h2j, j2hcj
import unicodedata

def decompose_korean_word(word):
    """
    주어진 한국어 단어를 음소 단위로 분해합니다.
    """
    decomposed = []
    for char in word:
        if '가' <= char <= '힣':  # 한글 완성자 범위
            jamos = h2j(char)
            decomposed.append(j2hcj(jamos))
        else:
            decomposed.append(char)
    return ''.join(decomposed)

def remove_spaces(text):
    """
    주어진 텍스트에서 띄어쓰기를 제거합니다.
    """
    return text.replace(" ", "")


def compare_korean_words(word1, word2):
    """
    두 한국어 단어를 음소 단위로 분해한 후 비교합니다.
    """
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

#예제 사용
# word1 = "학 교"
# word2 = "학꾜"
#
# accuracy, decomp_word1, decomp_word2 = compare_korean_words(word1, word2)
#
# print(f"단어 1 ({word1})의 음소 분해: {decomp_word1}")
# print(f"단어 2 ({word2})의 음소 분해: {decomp_word2}")
# print(f"정확도: {accuracy:.2f}")
