from jamo import h2j, j2hcj
import unicodedata


def decompose_korean_word(word):
    def decompose_char(char):
        # 유니코드에서 한글 음절의 시작점
        BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28
        # 초성 리스트. 00 ~ 18
        CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        # 중성 리스트. 00 ~ 20
        JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
        # 종성 리스트. 00 ~ 27 + 1(1개 없음)
        JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

        if '가' <= char <= '힣':  # 한글 음절 여부 확인
            char_code = ord(char) - BASE_CODE
            chosung_index = char_code // CHOSUNG
            jungsung_index = (char_code - (CHOSUNG * chosung_index)) // JUNGSUNG
            jongsung_index = (char_code - (CHOSUNG * chosung_index) - (JUNGSUNG * jungsung_index))
            return CHOSUNG_LIST[chosung_index] + JUNGSUNG_LIST[jungsung_index] + (JONGSUNG_LIST[jongsung_index] if JONGSUNG_LIST[jongsung_index] != ' ' else '')
        else:
            return char
    
    decomposed = []
    for char in word:
        decomposed_char = decompose_char(char)
        if len(decomposed_char) == 2:  # 받침이 없는 경우
            decomposed_char = decomposed_char[0] + decomposed_char[1] + ' '
        decomposed.append(decomposed_char)
    
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

